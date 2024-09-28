import os

import numpy as np
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.distributed import DistributedSampler

from notebooks.models import AutoEncoder
from notebooks.train import CheckPoint, CommonTrainer, EarlyStop, SnapshotManager


def to_train(
    feature_path: str, latent_dim=16, lr=1e-6, rank=0, world_size=1, batch_size=2
):
    features = np.load(feature_path)
    feature_dim = features.shape[1] * features.shape[2]

    print("Feature dim: ", feature_dim)

    X = torch.tensor(features, dtype=torch.float32)
    X = X.view(X.size(0), -1)

    dataset = TensorDataset(X)
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    dataloader = DataLoader(
        dataset, batch_size=batch_size, sampler=sampler, num_workers=os.cpu_count()
    )

    model = DDP(
        AutoEncoder(feature_dim=feature_dim, latent_dim=latent_dim), device_ids=None
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    return model, dataloader, optimizer


def main(rank, features_filename, emb_filename, epochs, latent_dim, lr):
    dist.init_process_group(backend="gloo", init_method="env://")

    world_size = dist.get_world_size()

    print(f"RANK: {rank}, WORLD_SIZE: {world_size}")

    model, dataloader, optimizer = to_train(
        features_filename,
        latent_dim=latent_dim,
        lr=lr,
        rank=rank,
        world_size=world_size,
    )

    snapshot_manager = SnapshotManager(model, n_snapshots=3)
    early_stop = EarlyStop(patience=12)
    checkpoint = CheckPoint(snapshot_manager=snapshot_manager, snapshot_interval=5)

    criterion = torch.nn.MSELoss()

    trainer = CommonTrainer(
        model, dataloader, optimizer, criterion, early_stop, checkpoint, rank=rank
    )

    trainer.train(epochs=epochs)

    snapshot_manager.load_latest()

    embeddings = trainer.extract_embeddings()

    if rank == 0:
        print(f"Embeddings shape: {embeddings.shape}")
        np.save(emb_filename, embeddings)

    dist.destroy_process_group()


def run_training(features_filename, emb_filename, epochs, latent_dim, lr):
    mp.spawn(
        main,
        args=(features_filename, emb_filename, epochs, latent_dim, lr),
        nprocs=1,
        join=True,
    )

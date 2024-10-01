import gc

import torch
from torch.nn.parallel import DistributedDataParallel as DDP

from .trainer import Trainer


class CommonTrainer(Trainer):
    def __init__(self, *args, acc_steps=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.acc_steps = acc_steps

    def train_epoch(self):
        running_loss = 0.0
        self.optimizer.zero_grad()

        for batch_idx, (data,) in enumerate(self.dataloader):
            data = data.to(self.device, non_blocking=True)

            outputs = self.model(data)

            loss = self.criterion(outputs, data) / self.acc_steps
            loss.backward()

            if (batch_idx + 1) % self.acc_steps == 0 or (batch_idx + 1) == len(
                self.dataloader
            ):
                self.optimizer.step()
                self.optimizer.zero_grad()

            running_loss += loss.item()

            del data, outputs, loss

            if (batch_idx + 1) % (self.acc_steps * 5) == 0:
                if torch.backends.mps.is_available():
                    torch.mps.empty_cache()

                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                gc.collect()

        num_batches = len(self.dataloader) // self.acc_steps
        avg_train_loss = running_loss / num_batches if num_batches > 0 else float('inf')

        return avg_train_loss

    def extract_embeddings(self):
        self.model.to(self.device)

        self.model.eval()

        embeddings = []

        with torch.no_grad():
            for _batch_idx, (data,) in enumerate(self.dataloader):
                data = data.to(self.device)

                if isinstance(self.model, DDP):
                    latent = self.model.module.get_latent(data)
                else:
                    latent = self.model.get_latent(data)

                embeddings.append(latent.cpu())

        embeddings = torch.vstack(embeddings)

        return embeddings.numpy()

from abc import ABC, abstractmethod

import torch
from torch.optim.lr_scheduler import StepLR


class Trainer(ABC):
    def __init__(
        self,
        model,
        dataloader,
        optimizer,
        criterion,
        early_stop,
        checkpoint,
        device=None,
        rank=0,
        lr_scheduler_step=5,
        lr_scheduler_gamma=0.1,
    ):

        self.model = model
        self.dataloader = dataloader
        self.device = (
            device
            if device
            else (
                torch.device("cuda")
                if torch.cuda.is_available()
                else (
                    torch.device("mps")
                    if torch.backends.mps.is_available()
                    else torch.device("cpu")
                )
            )
        )
        self.early_stop = early_stop
        self.checkpoint = checkpoint

        self.optimizer = optimizer
        self.criterion = criterion
        self.rank = rank
        self.lr_scheduler = StepLR(
            self.optimizer, step_size=lr_scheduler_step, gamma=lr_scheduler_gamma
        )

        if self.rank == 0:
            self.checkpoint.load_latest()

        self.model.to(self.device)

    @abstractmethod
    def train_epoch(self) -> float:
        pass

    def train(self, epochs=50):
        self.model.to(self.device)
        self.model.train()

        for epoch in range(epochs):
            avg_train_loss = self.train_epoch()

            self.lr_scheduler.step()

            if self.rank == 0:
                print(f"Epoch [{epoch + 1}/{epochs}], Train Loss: {avg_train_loss:.8f}")

                improved = avg_train_loss < self.early_stop.best_loss

                self.checkpoint.check_and_save(epoch, improved)

                if self.early_stop.check(avg_train_loss):
                    break

                self.checkpoint.periodic_save(epoch)

        if self.rank == 0:
            print("Training Complete")

from abc import ABC, abstractmethod

import torch
import torch.nn as nn


class Trainer(ABC):
    def __init__(
        self,
        model,
        dataloader,
        early_stop,
        checkpoint,
        epochs=50,
        lr=1e-4,
        device=None,
        optimizer_class=torch.optim.Adam,
        criterion_class=nn.MSELoss,
        **optimizer_kwargs,
    ):

        self.model = model
        self.model_name = model.__class__.__name__
        self.dataloader = dataloader
        self.epochs = epochs
        self.lr = lr
        self.device = (
            device
            if device
            else (torch.device("mps") if torch.backends.mps.is_available() else "cpu")
        )
        self.early_stop = early_stop
        self.checkpoint = checkpoint

        self.optimizer = optimizer_class(
            self.model.parameters(), lr=self.lr, **optimizer_kwargs
        )
        self.criterion = criterion_class()

        self.checkpoint.load_latest()

        self.model.to(self.device)

    @abstractmethod
    def train_epoch(self) -> float:
        pass

    def train(self):
        self.model.to(self.device)
        self.model.train()

        for epoch in range(self.epochs):
            avg_train_loss = self.train_epoch()

            print(
                f"Epoch [{epoch + 1}/{self.epochs}], Train Loss: {avg_train_loss:.8f}"
            )

            improved = avg_train_loss < self.early_stop.best_loss

            self.checkpoint.check_and_save(epoch, improved)

            if self.early_stop.check(avg_train_loss):
                break

            self.checkpoint.periodic_save(epoch)

        print("Training Complete")

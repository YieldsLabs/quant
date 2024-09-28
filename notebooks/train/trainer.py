from abc import ABC, abstractmethod

import torch


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
    ):

        self.model = model
        self.model_name = model.__class__.__name__
        self.dataloader = dataloader
        self.device = (
            device if device 
            else (torch.device("cuda") if torch.cuda.is_available() 
            else (torch.device("mps") if torch.backends.mps.is_available() 
            else torch.device("cpu")))
        )
        self.early_stop = early_stop
        self.checkpoint = checkpoint

        self.optimizer = optimizer
        self.criterion = criterion
        self.rank = rank

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

            if self.rank == 0:
                print(f"Epoch [{epoch + 1}/{epochs}], Train Loss: {avg_train_loss:.8f}")

                improved = avg_train_loss < self.early_stop.best_loss

                self.checkpoint.check_and_save(epoch, improved)

                if self.early_stop.check(avg_train_loss):
                    break

                self.checkpoint.periodic_save(epoch)

        if self.rank == 0:
            print("Training Complete")

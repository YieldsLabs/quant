from abc import ABC, abstractmethod


class Trainer(ABC):
    def __init__(
        self,
        model,
        dataloader,
        optimizer,
        lr_scheduler,
        criterion,
        early_stop,
        checkpoint,
        device=None,
        rank=0,
    ):

        self.model = model
        self.dataloader = dataloader
        self.device = device
        self.early_stop = early_stop
        self.checkpoint = checkpoint

        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
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

        print(f"Start training with epochs {epochs}")

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

import gc

import torch

from .trainer import Trainer


class CommonTrainer(Trainer):
    def __init__(self, *args, acc_steps=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.acc_steps = acc_steps

    def train_epoch(self):
        running_loss = 0.0
        self.optimizer.zero_grad()

        for batch_idx, (data,) in enumerate(self.dataloader):
            data = data.to(self.device)

            outputs = self.model(data)

            loss = self.criterion(outputs, data)
            loss = loss / self.acc_steps
            loss.backward()

            if (batch_idx + 1) % self.acc_steps == 0:
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

        avg_train_loss = running_loss / len(self.dataloader)

        return avg_train_loss

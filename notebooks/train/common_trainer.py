from .trainer import Trainer


class CommonTrainer(Trainer):
    def train_epoch(self):
        running_loss = 0.0

        for _batch_idx, (data,) in enumerate(self.dataloader):
            data = data.to(self.device)

            self.optimizer.zero_grad()

            outputs = self.model(data)
            loss = self.criterion(outputs, data)

            loss.backward()
            self.optimizer.step()

            running_loss += loss.item()

        avg_train_loss = running_loss / len(self.dataloader)

        return avg_train_loss

class EarlyStop:
    def __init__(self, patience=5):
        self.patience = patience
        self.best_loss = float("inf")
        self.epochs_without_improvement = 0

    def check(self, current_loss: float):
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            self.epochs_without_improvement = 0

            return False
        else:
            self.epochs_without_improvement += 1

            if self.epochs_without_improvement >= self.patience:
                print("Early stopping triggered!")
                return True

            return False

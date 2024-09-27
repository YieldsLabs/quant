class CheckPoint:
    def __init__(self, snapshot_manager, snapshot_interval=5):
        self.snapshot_manager = snapshot_manager
        self.snapshot_interval = snapshot_interval

    def load_latest(self):
        self.snapshot_manager.load_latest()

    def check_and_save(self, epoch: int, improved=False):
        self.snapshot_manager.save(epoch, improved=improved)

    def periodic_save(self, epoch: int):
        if (epoch + 1) % self.snapshot_interval == 0:
            self.snapshot_manager.save(epoch, improved=False)
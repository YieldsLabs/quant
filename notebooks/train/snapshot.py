import os

import torch


class SnapshotManager:
    def __init__(self, model, snapshot_dir='snapshots', n_snapshots=5, remove_threshold=2):
        self.model = model
        self.model_name = model.__class__.__name__
        self.snapshot_dir = snapshot_dir
        self.n_snapshots = n_snapshots
        self.remove_threshold = remove_threshold

        os.makedirs(self.snapshot_dir, exist_ok=True)

    def save(self, epoch, improved=False):
        snapshot_type = "improved" if improved else "periodic"
        snapshot_path = os.path.join(self.snapshot_dir, f'{self.model_name}_epoch_{epoch + 1}_{snapshot_type}.pth')
        torch.save(self.model.state_dict(), snapshot_path)
        print(f"Saved {snapshot_type} snapshot: {snapshot_path}")

        self._manage_snapshots()

    def load_latest(self):
        snapshots = self._get_sorted_snapshots()
        improved_snapshots = [s for s in snapshots if 'improved' in s and s.startswith(self.model_name)]
        periodic_snapshots = [s for s in snapshots if 'periodic' in s and s.startswith(self.model_name)]

        if improved_snapshots:
            self._load_snapshot(improved_snapshots[-1])
        elif periodic_snapshots:
            self._load_snapshot(periodic_snapshots[-1])
        else:
            print("No snapshots found, starting from scratch.")

    def _load_snapshot(self, snapshot_file):
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_file)

        if os.path.exists(snapshot_path):
            self.model.load_state_dict(torch.load(snapshot_path, map_location='cpu', weights_only=True))
            print(f"Loaded snapshot: {snapshot_path}")
        else:
            print(f"Snapshot {snapshot_path} not found.")

    def _manage_snapshots(self):
        all_snapshots = self._get_sorted_snapshots()
        improved_snapshots = [s for s in all_snapshots if 'improved' in s]
        periodic_snapshots = [s for s in all_snapshots if 'periodic' in s]

        if len(all_snapshots) > self.n_snapshots:
            if len(improved_snapshots) > self.remove_threshold:
                snapshots_to_remove = improved_snapshots[:-1]
                for snapshot in snapshots_to_remove:
                    snapshot_path = os.path.join(self.snapshot_dir, snapshot)
                    if os.path.exists(snapshot_path):
                        os.remove(snapshot_path)
                        print(f"Removed old improved snapshot: {snapshot_path}")

            if len(periodic_snapshots) > self.remove_threshold:
                snapshots_to_remove = periodic_snapshots[:-1]
                for snapshot in snapshots_to_remove:
                    snapshot_path = os.path.join(self.snapshot_dir, snapshot)
                    if os.path.exists(snapshot_path):
                        os.remove(snapshot_path)
                        print(f"Removed old periodic snapshot: {snapshot_path}")

            all_snapshots = self._get_sorted_snapshots()
            if len(all_snapshots) > self.n_snapshots:
                excess_snapshots = all_snapshots[:-self.n_snapshots]
                for snapshot in excess_snapshots:
                    snapshot_path = os.path.join(self.snapshot_dir, snapshot)
                    if os.path.exists(snapshot_path):
                        os.remove(snapshot_path)
                        print(f"Removed excess snapshot: {snapshot_path}")

    def _get_sorted_snapshots(self):
        snapshots = [f for f in os.listdir(self.snapshot_dir) if f.startswith(self.model_name)]
        snapshots.sort(key=lambda s: os.path.getctime(os.path.join(self.snapshot_dir, s)))
        return snapshots
import json
import os

from core.event_encoder import Encoder
from core.events.base import Event


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventStore(metaclass=SingletonMeta):
    def __init__(self, base_dir: str, buffer_size: int = 100):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.buffer_size = buffer_size
        self.buffer = []

    async def append(self, event: Event):
        self.buffer.append(event.to_dict())
        
        if len(self.buffer) >= self.buffer_size:
            self._flush_buffer()

    def get_all(self) -> list:
        file_path = self._get_file_path()

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                events_from_file = json.load(f)
        else:
            events_from_file = []

        return events_from_file + self.buffer

    def close(self) -> None:
         self._flush_buffer()

    def _get_file_path(self, date: str = None) -> str:
        if date:
            filename = f"{date}_snapshot.json"
        else:
            filename = "events.json"
        
        return os.path.join(self.base_dir, filename)

    def _flush_buffer(self) -> None:
        self._append_to_file(self.buffer)
        
        self.buffer = []

    def _append_to_file(self, events) -> None:
        file_path = self._get_file_path()
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

        with open(file_path, 'r+') as f:
            existing_events = json.load(f)
            existing_events.extend(events)
            
            f.seek(0)
            
            json.dump(existing_events, f, cls=Encoder)
            
            f.truncate()

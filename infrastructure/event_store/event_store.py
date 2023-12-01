import json
import os
from typing import Optional

from core.events.base import Event
from core.interfaces.abstract_config import AbstractConfig

from .event_encoder import Encoder


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventStore(metaclass=SingletonMeta):
    def __init__(self, config_service: AbstractConfig):
        config = config_service.get("store")

        self.base_dir = config["base_dir"]

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        self.buffer_size = config["buf_size"]
        self.buffer = {}

    def append(self, event: Event):
        group = str(event.meta.group)

        if group not in self.buffer:
            self.buffer[group] = []

        self.buffer[group].append(event)

        if len(self.buffer[group]) >= self.buffer_size:
            self._flush_buffer(group)

    def get(self, group: str) -> list:
        file_path = self._get_file_path(group)

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                events_from_file = json.load(f)
        else:
            events_from_file = []

        events_from_buffer = self.buffer.get(group, [])

        return events_from_file + events_from_buffer

    def close(self) -> None:
        for group in self.buffer:
            self._flush_buffer(group)

    def _get_file_path(self, group: str, date: Optional[str] = None) -> str:
        if date:
            filename = f"{group}_{date}_snapshot.json"
        else:
            filename = f"{group}.json"

        return os.path.join(self.base_dir, filename)

    def _flush_buffer(self, group: str) -> None:
        if group in self.buffer and len(self.buffer[group]) > 0:
            self._append_to_file(group, self.buffer[group])
            self.buffer[group] = []

    def _append_to_file(self, group: str, events: list) -> None:
        file_path = self._get_file_path(group)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")

        with open(file_path, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()

            for event in events:
                if f.tell() > 1:
                    f.write(",".encode("utf-8"))

                event_data = json.dumps(event, cls=Encoder)
                f.write(event_data.encode("utf-8"))

            f.write("]".encode("utf-8"))

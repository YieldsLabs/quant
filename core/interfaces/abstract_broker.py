from abc import abstractmethod

from core.commands.base import Command
from core.queries.base import Query

from .abstract_event_manager import AbstractEventManager


class AbstractBroker(AbstractEventManager):
    @abstractmethod
    def update_symbol_settings(self, command: Command):
        pass

    @abstractmethod
    def open_position(self, command: Command):
        pass

    @abstractmethod
    def close_position(self, command: Command):
        pass

    @abstractmethod
    def get_open_position(self, query: Query):
        pass

    @abstractmethod
    def get_symbols(self, query: Query):
        pass

    @abstractmethod
    def get_symbol(self, query: Query):
        pass

    @abstractmethod
    def get_account_balance(self, query: Query):
        pass

from dataclasses import dataclass

from core.commands.base import Command
from core.interfaces.abstract_datasource_factory import DataSourceType


@dataclass(frozen=True)
class FeedRun(Command):
    datasource: DataSourceType

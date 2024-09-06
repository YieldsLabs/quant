from typing import Any, Callable, Dict, Type


class EventHandlerMixin:
    def __init__(self):
        self._handlers: Dict[Type[Any], Callable] = {}

    def register_handler(self, event_type: Type[Any], handler: Callable):
        self._handlers[event_type] = handler

    async def handle_event(self, event: Any) -> Any:
        handler = self._handlers.get(type(event))
        if handler:
            return await handler(event)
        return None

"""
core/event_bus.py — Thread-safe event bus
"""

import threading
from typing import Callable, Dict, List, Any
from core.logger import LOGGER


class EventBus:
    """Singleton event bus."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._subscribers: Dict[str, List[Callable]] = {}
                cls._instance._lock = threading.Lock()
            return cls._instance

    def subscribe(self, event_type: str, callback: Callable):
        """Bir event'e abone ol."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any = None):
        """Bir event yayınla."""
        with self._lock:
            callbacks = self._subscribers.get(event_type, [])
        for cb in callbacks:
            try:
                cb(data)
            except Exception as e:
                LOGGER.error(f"Event bus callback error: {e}")


EVENT_BUS = EventBus()
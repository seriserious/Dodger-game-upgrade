from abc import ABC, abstractmethod
import pygame
import pyghelpers
from typing import List, Optional, Any

class BaseScene(pyghelpers.Scene, ABC):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self._window = window
        self._scene_key: str = ""
        self._is_active: bool = False

    @property
    def window(self) -> pygame.Surface:
        return self._window

    @property
    def scene_key(self) -> str:
        return self._scene_key

    @scene_key.setter
    def scene_key(self, value: str) -> None:
        self._scene_key = value

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self._is_active = value

    @abstractmethod
    def getSceneKey(self) -> str:
        pass

    @abstractmethod
    def enter(self, data: Optional[Any] = None) -> None:
        pass

    @abstractmethod
    def handleInputs(self, eventsList: List[pygame.event.Event], keyPressedList: List[int]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def leave(self) -> Optional[Any]:
        pass 
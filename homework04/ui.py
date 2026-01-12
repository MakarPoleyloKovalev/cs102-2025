"""Абстрактный базовый класс для пользовательских интерфейсов игры 'Жизнь'"""

import abc

from life import GameOfLife


# Локальный импорт
try:
    from .life import GameOfLife
except ImportError:
    from life import GameOfLife


class UI(abc.ABC):
    """Абстрактный базовый класс для пользовательских интерфейсов игры 'Жизнь'"""

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        """Запустить интерфейс"""

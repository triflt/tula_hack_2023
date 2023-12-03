from enum import Enum
from pathlib import Path
from typing import Literal, TypedDict


class Config(TypedDict):
    device: Literal['cpu', 'cuda', 'mps']
    classifier_path: str | Path
    checkpoint_path: str | Path


class Buildings(Enum):
    GREENHOUSE = 0
    PRIVATE_HOUSE = 1
    PUBLIC_BUILDING = 2
    PUBLIC_HOUSE = 3
    BARN = 4
    POOL = 5
    NOTHING = 6

    def __str__(self):
        return self.verbose_name

    @property
    def verbose_name(self) -> str:
        match self:
            case self.GREENHOUSE: return 'Теплица'
            case self.PRIVATE_HOUSE: return 'Частный дом'
            case self.PUBLIC_BUILDING: return 'Общественное здание'
            case self.PUBLIC_HOUSE: return 'Многоквартирный дом'
            case self.BARN: return 'Сарай'
            case self.POOL: return 'Бассейн'
            case self.NOTHING: return 'Другие объекты'

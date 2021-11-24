from enum import Enum


class Color(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4


class CardType(Enum):
    REGULAR_CARD = 1
    CHANGES_COLOR = 2
    STOP = 3
    CHANGES_DIRECTION = 4
    PLUS_TWO = 5
    PLUS = 6


class PlayerType(Enum):
    SMART_BOT = 1
    RANDOM_BOT = 2
    HUMAN_PLAYER = 3

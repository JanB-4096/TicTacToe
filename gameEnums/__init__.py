from enum import Enum

class GameStatus(Enum):
    RUNNING = 0
    PLAYER_1_WON = 1
    PLAYER_2_WON = 2
    DRAW = 3
    
class FieldState(Enum):
    EMPTY = 0
    X = 1
    O = 2
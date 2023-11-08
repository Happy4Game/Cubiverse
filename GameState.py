from enum import Enum

class GameState(Enum):
    HOMESCREEN = 0
    CHOOSEMENU = 1
    CHOOSEMENU_TYPE = 2
    GAMELAUNCHED = 3
    FIGHT = 4
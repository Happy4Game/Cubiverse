import Player
import GameBoardWindows

class Player():
    def __init__(self, number : int, gameboard_window : GameBoardWindows, typeofclass : str = "UNDEFINED") -> None:
        """Init player

        Args:
            number (int): number of the player
            gameboard_window (GameBoardWindows): GameBoardWindows
            typeofclass (str, optional): Can be UNDEFINED, CHOOSING, MINOR or FIGHTER. Defaults to "UNDEFINED".
        """
        self.init_common_stats()
        self._number : int              = number
        self._gameboard_window          = gameboard_window
        self._pos                       = (0,0)
        if self._number == 1:
            self._pos = (6,1)
        elif self._number == 2:
            self._pos = (6,12)
        elif self._number == 3:
            self._pos = (1,6)
        elif self._number == 4:
            self._pos = (12,6)

        self.setTypeOfClass(typeofclass)

    def init_common_stats(self):
        self._inventory : list          = []
        self._typeofclass : str         = "UNDEFINED" # Can be UNDEFINED, CHOOSING, MINOR, FIGHTER, IA_MINOR or IA_FIGHTER
        self._typeingameboard : str     = ""
        self._health : int              = 30
        self._attack : int              = 10
        self._maxrange : int            = 3
        self._isWinner : bool           = False
        self._canFight : bool           = True


    def setTypeOfClass(self, type : str):
        """Set the type of the class

        Args:
            type (str): Type of the class, see __init__
        """
        self.init_common_stats()
        if type == "MINOR":
            self._typeofclass       = type
            self._inventory.append("res")
            self._typeingameboard   = "_p_minor"
        elif type == "FIGHTER":
            self._attack            = self._attack * 1.5
            self._typeofclass       = type
            self._typeingameboard   = "_p_fighter"
        elif type == "IA_FIGHTER":
            self._attack            = self._attack * 1.5
            self._typeofclass       = type
            self._typeingameboard   = "_p_ia_fighter"
        elif type == "IA_MINOR":
            self._typeofclass       = type
            self._inventory.append("res")
            self._typeingameboard   = "_p_ia_minor"
        elif type == "CHOOSING":
            self._typeofclass = type
        elif type == "UNDEFINED":
            self.init_common_stats()

    def die(self):
        """Reset life and pos of the player
        """
        self._health : int = 30
        if len(self._inventory) > 0:
            self._inventory.pop()
        if self._number == 1:
            self.movePlayer((6,1))
        elif self._number == 2:
            self.movePlayer((6,12))
        elif self._number == 3:
            self.movePlayer((1,6))
        elif self._number == 4:
            self.movePlayer((12,6))

    def attack(self, p : Player) -> None:
        """Self attack the p Player

        Args:
            p (Player): Player attacked
        """
        p._health = p._health - self._attack
        if p._health <= 0:
            p.die()
        self._canFight = True
        p._canFight = True

    def resetMaxMovement(self) -> None:
        """Reset the max_range of the player
        """
        self._maxrange = 3

    def canMovePlayer(self, newPos : tuple) -> bool:
        """See if the player can move or not

        Args:
            newPos (tuple): position to try

        Returns:
            bool: True if the player can, False if not
        """
        if newPos != None:
            
            if self._pos[0] - self._maxrange <= newPos[0] <= self._pos[0] + self._maxrange:
                if self._pos[1] - self._maxrange <= newPos[1] <= self._pos[1] + self._maxrange:
                    
                    nb_movement = abs(self._pos[0] - newPos[0]) + abs(self._pos[1] - newPos[1])
                    if nb_movement <= 3:

                        # Remove typeingameboard of gameboard
                        self._gameboard_window._gameboard[self._pos[0]][self._pos[1]] = self._gameboard_window._gameboard[self._pos[0]][self._pos[1]].replace(self._typeingameboard, "")
                        # Add typeingameboard for the new pos
                        self._gameboard_window._gameboard[newPos[0]][newPos[1]] += self._typeingameboard
                        
                        self._pos = newPos
                        self._maxrange -= nb_movement
                        return True
            return False

    def movePlayer(self, newPos : tuple) -> int:
        """Move the player and return the amount of movement

        Args:
            newPos (tuple): (int,int)

        Returns:
            int: amount of movement
        """
        if newPos != None:
            
            if self._pos[0] - self._maxrange <= newPos[0] <= self._pos[0] + self._maxrange:
                if self._pos[1] - self._maxrange <= newPos[1] <= self._pos[1] + self._maxrange:
                    
                    nb_movement = abs(self._pos[0] - newPos[0]) + abs(self._pos[1] - newPos[1])
                    if nb_movement <= 3:

                        # Remove typeingameboard of gameboard
                        if self._gameboard_window._gameboard[newPos[0]][newPos[1]].startswith("res"):
                            self._inventory.append("res")
                            self._gameboard_window._gameboard[newPos[0]][newPos[1]] = "g"

                        elif self._gameboard_window._gameboard[newPos[0]][newPos[1]].startswith("m"):
                            #TODO Win
                            if len(self._inventory) >= 4:
                                self._isWinner = True
                            return 0

                        self._gameboard_window._gameboard[self._pos[0]][self._pos[1]] = self._gameboard_window._gameboard[self._pos[0]][self._pos[1]].replace(self._typeingameboard, "")
                        # Add typeingameboard for the new pos
                        self._gameboard_window._gameboard[newPos[0]][newPos[1]] += self._typeingameboard
                        
                        self._pos = newPos
                        self._maxrange -= nb_movement
                        return nb_movement
            return 0
        
    def __repr__(self) -> str:
        return "Player : [number : " + str(self._number) + ", inventory : " + str(self._inventory) + ", type : " + self._typeofclass + ", health : " + str(self._health) + ", attack : " + str(self._attack) + ", pos : " + str(self._pos) + ", maxrange : " + str(self._maxrange) + "]"
import pygame
import Player
from random import randint

class GameBoardWindows():
    def __init__(self, gameboard : list) -> None:
        
        self._gameboard = gameboard
        self.putRandomRes()

    def putRandomRes(self):
        numberOfRes : int = 12
        r_one : int
        r_two : int
        while numberOfRes > 0:
            r_one = randint(1, len(self._gameboard) - 1)
            r_two = randint(1, len(self._gameboard) - 1)
            if str(self._gameboard[r_one][r_two]).startswith("g"):
                self._gameboard[r_one][r_two] = "res"
                numberOfRes -= 1

        
    def drawGameboard(self, screen):
        """Draw the gameboard at the screen

        Args:
            gameboard (list): json data that contains the gameboard
        """
        for i in range(len(self._gameboard)):
            for j in range(len(self._gameboard)):
                coordinate : tuple = (1280 / 4.5 + j*50,i*50)
                if str(self._gameboard[i][j]).startswith("g"):
                    screen.blit(pygame.image.load("./assets/png/grass.png").convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("b_one_r"):
                    screen.blit(pygame.transform.rotate(pygame.image.load("./assets/png/bed_part_one.png"), 90).convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("b_two_r"):
                    screen.blit(pygame.transform.rotate(pygame.image.load("./assets/png/bed_part_two.png"), 90).convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("b_one"):
                    screen.blit(pygame.image.load("./assets/png/bed_part_one.png").convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("b_two"):
                    screen.blit(pygame.image.load("./assets/png/bed_part_two.png").convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("m"):
                    screen.blit(pygame.image.load("./assets/png/lugubrious_mine.png").convert_alpha(), coordinate)
                elif str(self._gameboard[i][j]).startswith("res"):
                    screen.blit(pygame.image.load("./assets/png/res.png").convert_alpha(), coordinate)

                # Render player
                if str(self._gameboard[i][j]).endswith("_p_fighter"):
                    screen.blit(pygame.image.load("./assets/png/sword.png").convert_alpha(), coordinate)
                if str(self._gameboard[i][j]).endswith("_p_minor"):
                    screen.blit(pygame.image.load("./assets/png/pickaxe.png").convert_alpha(), coordinate)

                # Render ia player
                if str(self._gameboard[i][j]).endswith("_p_ia_fighter"):
                    screen.blit(pygame.image.load("./assets/png/ia_sword.png").convert_alpha(), coordinate)
                if str(self._gameboard[i][j]).endswith("_p_ia_minor"):
                    screen.blit(pygame.image.load("./assets/png/ia_pickaxe.png").convert_alpha(), coordinate)
                    



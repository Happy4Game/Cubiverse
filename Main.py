# Example file showing a basic pygame "game loop"
import pygame
import json
from random import randint
from GameState import GameState
from GameBoardWindows import GameBoardWindows
from Player import Player
from math import sqrt

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# GameBoard
with open("gameboard.json") as gameboard_data:
    gameboard_json = json.load(gameboard_data)

gameboard = gameboard_json["gameboard"]

round_number = 1

random_dice_value_one : int = 0
random_dice_value_two : int = 0

gameboard_window : GameBoardWindows = GameBoardWindows(gameboard)


GAMESTATUS = GameState.HOMESCREEN
playerOne = Player(1, gameboard_window)
playerTwo = Player(2, gameboard_window)
playerThree = Player(3, gameboard_window)
playerFour = Player(4, gameboard_window)

list_players : list[Player] = [playerOne, playerTwo, playerThree, playerFour]

list_fighting_players : list[Player] = []

playerLeftWinned : bool = False
playerRightWinned : bool = False

def debug(info : str, x : int = 10, y : int = 10):
    font            = pygame.font.Font(None, 30)
    display_surf    = pygame.display.get_surface()
    debug_surf      = font.render(str(info), True, 'white')
    debug_rect      = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)

def drawMenu() -> None:
    """Draw menu
    """
    # render text
    label = myfont.render("Bonjour tout le monde !", 1, (0,0,0))
    screen.blit(label, (SCREEN_WIDTH / 2 - int(label.get_size()[0] / 2), SCREEN_HEIGHT / 2 - 200))

    pygame.draw.rect(screen, (0,0,0), (535,300,200,100))
    screen.blit(myfont_big.render("Jouer", 1, (255,0,0)), (573, 325))

def getButtonPressed(mouse_pos : tuple, origin : tuple, size : tuple) -> bool:
    """Get if btn is pressed

    Args:
        mouse_pos (tuple): Mouse position
        origin (tuple): Origin position of button
        size (tuple): (Width, Height)

    Returns:
        bool: True if it is, False else
    """
    if mouse_pos[0] >= origin[0] and mouse_pos[0] <= origin[0] + size[0]:
        if mouse_pos[1] >= origin[1] and mouse_pos[1] <= origin[1] + size[1]:
            return True
    return False

def drawPlayerImage(typeOfPlayer : str, coordinate : tuple) -> None:
    """Draw the image of the player with coordinate

    Args:
        typeOfPlayer (str): Type of player, can be MINOR or FIGHTER
        coordinate (tuple): position of the player in gameboard
    """
    # Button minor class
    path  = "./assets/png/"
    if typeOfPlayer == "MINOR":
        path = path + "pickaxe.png"
    elif typeOfPlayer == "FIGHTER":
        path = path + "sword.png"
    elif typeOfPlayer == "IA_MINOR":
        path = path + "ia_pickaxe.png"
    elif typeOfPlayer == "IA_FIGHTER":
        path = path + "ia_sword.png"
    else:
        return
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    screen.blit(image, coordinate)

def drawChoosePlayerMenu() -> None:
    """Draw the menu that shows all players
    """
    # render text
    label = myfont.render("Choisissez votre classe", 1, (0,0,0))
    screen.blit(label, (SCREEN_WIDTH / 2 - int(label.get_size()[0] / 2), SCREEN_HEIGHT / 2 - 200))

    # Player 1
    pygame.draw.rect(screen, (0,0,0), (400,250,100,100))
    screen.blit(myfont_big.render("1", 1, (255,0,0)), (440, 275))
    drawPlayerImage(playerOne._typeofclass, (235, 252))


    # Player 2
    pygame.draw.rect(screen, (0,0,0), (800,250,100,100))
    screen.blit(myfont_big.render("2", 1, (255,0,0)), (840, 275))
    drawPlayerImage(playerTwo._typeofclass, (635, 252))

    # Player 3
    pygame.draw.rect(screen, (0,0,0), (400,450,100,100))
    screen.blit(myfont_big.render("3", 1, (255,0,0)), (440, 475))
    drawPlayerImage(playerThree._typeofclass, (235, 452))

    # Player 4
    pygame.draw.rect(screen, (0,0,0), (800,450,100,100))
    screen.blit(myfont_big.render("4", 1, (255,0,0)), (840, 475))
    drawPlayerImage(playerFour._typeofclass, (635, 452))

    # Play button
    pygame.draw.rect(screen, (255,0,0), (527,610,250,50))
    screen.blit(myfont.render("Lancer", 1, (255,255,255)), (610,625))

def getGameBoardPositionByMouse(mouse_pos : tuple, max_gameboard_size : int = 14) -> tuple:
    """Return a tuple that represent the pos of mouse in the gameboard

    Args:
        mouse_pos (tuple): tuple with x and y pos
        max_gameboard_size (int, optional): Size of gameboard. Defaults to 14.

    Returns:
        tuple: (x,y) | None if the pos is invalid
    """
    y : int = int(mouse_pos[1] / 50)
    x : int = int((mouse_pos[0] - 1280 / 4.5) / 50) 
    if x >= 0 and x < max_gameboard_size:
        # x is in gameboard
        if y >= 0 and y < max_gameboard_size:
            return (y, x)
    return None

def getGameBoardPositionByCase(pos : tuple) -> tuple:
    """Return a tuple that represent the pos in the gameboard

    Args:
        pos (tuple): coordinate

    Returns:
        tuple: (x,y)
    """
    y : int = int(pos[1] * 50) + 1280 / 4.5
    x : int = int((pos[0]) * 50)
    return (y,x)

def getCaseByPosition(gameboard_pos : tuple) -> str:
    """Get case by position of the gameboard

    Args:
        gameboard_pos (tuple): Position in the gameboard

    Returns:
        str: letter that represent element in gameboard
    """
    if gameboard_pos != None:
        return(gameboard[gameboard_pos[0]][gameboard_pos[1]])

def drawChooseTypeOfPlayer(nb_player : int):
    """Draw Choose type of player menu

    Args:
        nb_player (int): number of player
    """
    # Background
    pygame.draw.rect(screen, (100,100,100), (400,100,500,500))
    screen.blit(myfont_big.render(str(nb_player), 1, (255,255,255)), (640, 125))

    # Button minor IA
    drawPlayerImage("IA_MINOR", (700, 225))

    # Button sword IA
    drawPlayerImage("IA_FIGHTER", (700, 350))

    # Button minor class
    drawPlayerImage("MINOR", (500, 225))

    # Button sword class
    drawPlayerImage("FIGHTER", (500, 350))

    # Button done
    pygame.draw.rect(screen, (255,0,0), (527,510,250,50))
    screen.blit(myfont.render("Retour", 1, (255,255,255)), (610,525))

def drawUI(player : Player) -> None:
    """Draw UI with player info

    Args:
        player (Player): player
    """
    
    label = myfont.render("Au tour du joueur : " + str(player._number), 1, (0,0,0))
    screen.blit(label, (10, 100))
    
    label = myfont_little.render("Type de joueur : " + player._typeofclass, 1, (0,0,0))
    screen.blit(label, (10, 125))

    label = myfont_little.render("Vie : " + str(player._health), 1, (0,0,0))
    screen.blit(label, (10, 145))

    label = myfont_little.render("Attaque : " + str(player._attack), 1, (0,0,0))
    screen.blit(label, (10, 165))

    label = myfont_little.render("Point de mouvement : " + str(player._maxrange), 1, (0,0,0))
    screen.blit(label, (10, 185))
    
    label = myfont_little.render("Nombre d'items : " + str(len(player._inventory)), 1, (0,0,0))
    screen.blit(label, (10, 205))

    label = myfont_little.render("Items joueur 1 : " + str(len(list_players[0]._inventory)), 1, (0,0,0))
    screen.blit(label, (1000, 100))

    label = myfont_little.render("Items joueur 2 : " + str(len(list_players[1]._inventory)), 1, (0,0,0))
    screen.blit(label, (1000, 125))

    label = myfont_little.render("Items joueur 3 : " + str(len(list_players[2]._inventory)), 1, (0,0,0))
    screen.blit(label, (1000, 150))

    label = myfont_little.render("Items joueur 4 : " + str(len(list_players[3]._inventory)), 1, (0,0,0))
    screen.blit(label, (1000, 175))

    # Draw red box
    screen.blit(pygame.image.load("./assets/png/select.png").convert_alpha(), getGameBoardPositionByCase(player._pos))

    # Draw end of the round btn
    screen.blit(pygame.image.load("./assets/png/end_round.png").convert_alpha(), (993, 630))

def drawFight() -> None:
    """Draw fight
    """
    i = 0
    for player in list_fighting_players:

        drawPlayerImage(player._typeofclass, (80 + i, 250))

        label = myfont_little.render("Numéro : " + str(player._number), 1, (0,0,0))
        screen.blit(label, (10 + i, 350))

        label = myfont_little.render("Type de joueur : " + player._typeofclass, 1, (0,0,0))
        screen.blit(label, (10 + i, 370))

        label = myfont_little.render("Vie : " + str(player._health), 1, (0,0,0))
        screen.blit(label, (10 + i, 390))

        label = myfont_little.render("Attaque : " + str(player._attack), 1, (0,0,0))
        screen.blit(label, (10 + i, 410))

        i += 1030

    pygame.draw.rect(screen, (100,200,100), (30,470,200,30))
    label = myfont_little.render("Lancer le dé", 1, (230,230,230))
    screen.blit(label, (70, 475))
    pygame.draw.rect(screen, (100,200,100), (1060,470,200,30))
    label = myfont_little.render("Lancer le dé", 1, (230,230,230))
    screen.blit(label, (1100, 475))
    screen.blit(myfont_big.render(str(random_dice_value_one), 1, (255,0,0)), (375,230))
    screen.blit(myfont_big.render(str(random_dice_value_two), 1, (255,0,0)), (902,230))

def isCellOccuped(pos : tuple) -> bool:
    """Check if the cell is occuped by a player

    Args:
        pos (tuple): pos

    Returns:
        bool: True if there is a player in, False if not
    """
    for p in list_players:
        if (p._pos == pos):
            return True
    return False

def getCell(pos : tuple) -> str:
    return gameboard[pos[0]][pos[1]]

def getPlayerByPos(pos : tuple) -> Player:
    """Get player by position

    Args:
        pos (tuple): position in gameboard

    Returns:
        Player: player
    """
    for p in list_players:
        if (p._pos == pos):
            return p
    return None

def getPlayerByNum(num : int) -> Player:
    """Get player by his num

    Args:
        num (int): number of player targetes

    Returns:
        Player: Player
    """
    for p in list_players:
        if p._number == num:
            return p
    return None        

def drawDice(pos : tuple, face_to_display : int):
    """Draw dice with the number 'display'

    Args:
        pos (tuple): pos of the dice
        face_to_display (int): 1 -> 6
    """
    screen.blit(pygame.image.load("./assets/png/" + str(face_to_display) + ".png").convert_alpha(), pos)

def drawWinnerFight(playerLeftWinned : bool, playerRightWinned : bool) -> (GameState, bool, bool, list[Player], int, int):
    """Draw the winner of the fight and RESET value to go to gameboard
    """
    if len(list_fighting_players) == 2:
        if playerLeftWinned == True:
            screen.blit(myfont_big.render("Le joueur " + str(list_fighting_players[0]._number) + " a gagné !", 1, (100,100,100)), (400, 125))
            list_fighting_players[0].attack(list_fighting_players[1])
            if len(list_fighting_players[1]._inventory) >= 1:
                # faire en sorte que le joueur perdant perde toutes ses gemmmes et qu'elles soient de nouveau redistribuée sur le plateau.
                list_fighting_players[1]._inventory.pop()
                list_fighting_players[0]._inventory.append("res")
            list_fighting_players[0]._maxrange = 0
            pygame.display.flip()
            pygame.time.delay(4000)
            playerLeftWinned = False
            list_fighting_players.clear()
            return (GameState.GAMELAUNCHED, playerLeftWinned, playerRightWinned, list_fighting_players, 0, 0)

        if playerRightWinned == True:
            screen.blit(myfont_big.render("Le joueur " + str(list_fighting_players[1]._number) + " a gagné !", 1, (100,100,100)), (400, 125))
            list_fighting_players[1].attack(list_fighting_players[0])
            if len(list_fighting_players[0]._inventory) >= 1:
                # faire en sorte que le joueur perdant perde toutes ses gemmmes et qu'elles soient de nouveau redistribuée sur le plateau.
                list_fighting_players[0]._inventory.pop()
                list_fighting_players[1]._inventory.append("res")
            list_fighting_players[1]._maxrange = 0
            pygame.display.flip()
            pygame.time.delay(4000)
            playerRightWinned = False
            list_fighting_players.clear()
            return (GameState.GAMELAUNCHED, playerLeftWinned, playerRightWinned, list_fighting_players, 0, 0)
    
    return (GameState.FIGHT, playerLeftWinned, playerRightWinned, list_fighting_players, random_dice_value_one, random_dice_value_two)

def getPlayerWithMaxedInventory(fromPlayer : Player) -> Player:
    """A function that return the Player who have the most res from different player than specified in

    Args:
        fromPlayer (Player): Player that must be not counted to be the richest player

    Returns:
        Player: The richest player
    """
    richest_player : Player = None
                    
    max_inventory_len : int = 0

    for p in list_players:
        if not fromPlayer.__eq__(p):
            if (len(p._inventory) > max_inventory_len):
                max_inventory_len = len(p._inventory)
                richest_player = p
    
    return richest_player

# pygame setup
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont : pygame.font        = pygame.font.SysFont("monospace", 20)
myfont_little : pygame.font = pygame.font.SysFont("monospace", 16)
myfont_big : pygame.font    = pygame.font.SysFont("monospace", 40)

screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True


while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAMESTATUS == GameState.GAMELAUNCHED:

                # If a player is in mouse pos                
                if isCellOccuped(getGameBoardPositionByMouse(pygame.mouse.get_pos())) and getPlayerByPos(getGameBoardPositionByMouse(pygame.mouse.get_pos()))._number != round_number:
                    #Fight
                    if getCell(getGameBoardPositionByMouse(pygame.mouse.get_pos())).endswith("_p_fighter") or getCell(getGameBoardPositionByMouse(pygame.mouse.get_pos())).endswith("_p_minor"):
                        # If they can fight
                        if getPlayerByNum(round_number)._canFight == True:
                            list_fighting_players.append((getPlayerByPos(getGameBoardPositionByMouse(pygame.mouse.get_pos()))))
                            list_fighting_players.append(getPlayerByNum(round_number))
                            GAMESTATUS = GameState.FIGHT
                else:
                    if getPlayerByNum(round_number).canMovePlayer(getGameBoardPositionByMouse(pygame.mouse.get_pos())):
                        # Move player if it's their round
                        getPlayerByNum(round_number).movePlayer(getGameBoardPositionByMouse(pygame.mouse.get_pos()))
                        # Disable Fight option
                        getPlayerByNum(round_number)._canFight = False
                    
                # If the end turn btn is pressed
                if (getButtonPressed(pygame.mouse.get_pos(), (993, 630), (277,68))):
                    if round_number + 1 > 4:    
                        playerFour.resetMaxMovement()
                        playerFour._canFight = True
                        round_number = 1
                    else:
                        if round_number == 1: 
                            playerOne.resetMaxMovement()
                            playerOne._canFight = True
                        elif round_number == 2:
                            playerTwo.resetMaxMovement()
                            playerTwo._canFight = True
                        elif round_number == 3:
                            playerThree.resetMaxMovement()
                            playerThree._canFight = True
                        round_number += 1      
            elif GAMESTATUS == GameState.CHOOSEMENU:
                # Player 1 button
                if getButtonPressed(pygame.mouse.get_pos(), (400,250), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerOne.setTypeOfClass("CHOOSING")
                
                # Player 2 button
                elif getButtonPressed(pygame.mouse.get_pos(), (800,250), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerTwo.setTypeOfClass("CHOOSING")

                # Player 3 button
                elif getButtonPressed(pygame.mouse.get_pos(), (400,450), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerThree.setTypeOfClass("CHOOSING")

                # Player 4 button
                elif getButtonPressed(pygame.mouse.get_pos(), (800,450), (100,100)):
                    GAMESTATUS = GameState.CHOOSEMENU_TYPE
                    playerFour.setTypeOfClass("CHOOSING")  
                
                # Play button
                elif getButtonPressed(pygame.mouse.get_pos(), (527,610), (250,50)):
                    # Add player in gameboard
                    gameboard_window._gameboard[playerOne._pos[0]][playerOne._pos[1]] += playerOne._typeingameboard
                    gameboard_window._gameboard[playerTwo._pos[0]][playerTwo._pos[1]] += playerTwo._typeingameboard
                    gameboard_window._gameboard[playerThree._pos[0]][playerThree._pos[1]] += playerThree._typeingameboard
                    gameboard_window._gameboard[playerFour._pos[0]][playerFour._pos[1]] += playerFour._typeingameboard
                    GAMESTATUS = GameState.GAMELAUNCHED      
            elif GAMESTATUS == GameState.HOMESCREEN:
                # Play button
                if getButtonPressed(pygame.mouse.get_pos(), (535, 300), (200, 100)):
                    # Launch game
                    GAMESTATUS = GameState.CHOOSEMENU
            elif GAMESTATUS == GameState.CHOOSEMENU_TYPE:
                if getButtonPressed(pygame.mouse.get_pos(), (500, 225), (48*2,48*2)):
                    # The Choosing player is minor
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("MINOR")
                  
                elif getButtonPressed(pygame.mouse.get_pos(), (500, 350), (48*2,48*2)):
                    # The Choosing player is fighter
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("FIGHTER")
                elif getButtonPressed(pygame.mouse.get_pos(), (700, 225), (48*2,48*2)):
                    # The Choosing player is ia_minor
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("IA_MINOR")
                elif getButtonPressed(pygame.mouse.get_pos(), (700, 350), (48*2,48*2)):
                    # The Choosing player is ia_fighter
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("IA_FIGHTER")

                elif getButtonPressed(pygame.mouse.get_pos(), (527,510), (610,525)):
                    for p in list_players:
                        if p._typeofclass == "CHOOSING":
                            p.setTypeOfClass("UNDEFINED")
                    GAMESTATUS = GameState.CHOOSEMENU

            elif GAMESTATUS == GameState.FIGHT:
                # Player left button
                #TODO Check if the 2 players have played and return to the game
                if getButtonPressed(pygame.mouse.get_pos(), (30,470), (200,30)):
                    random_dice_value_one = randint(1,6)
                elif getButtonPressed(pygame.mouse.get_pos(), (1060,470), (200,30)):
                    random_dice_value_two = randint(1,6)
                # If the 2 dices have been rolled
                if random_dice_value_one != 0 and random_dice_value_two != 0:
                    if random_dice_value_two < random_dice_value_one:
                        playerLeftWinned = True
                    else:
                        playerRightWinned = True

    # If player is not defined, pass round automaticaly
    if getPlayerByNum(round_number)._typeofclass == "UNDEFINED":
        if round_number + 1 > 4:    
            playerFour.resetMaxMovement()
            round_number = 1
        else:
            if round_number == 1: playerOne.resetMaxMovement()
            elif round_number == 2: playerTwo.resetMaxMovement()
            elif round_number == 3: playerThree.resetMaxMovement()
            round_number += 1

    if GAMESTATUS == GameState.HOMESCREEN:
        drawMenu()
    elif GAMESTATUS == GameState.CHOOSEMENU:
        drawChoosePlayerMenu()
    elif GAMESTATUS == GameState.CHOOSEMENU_TYPE:
        if playerOne._typeofclass == "CHOOSING":    drawChooseTypeOfPlayer(1)
        elif playerTwo._typeofclass == "CHOOSING":  drawChooseTypeOfPlayer(2)
        elif playerThree._typeofclass == "CHOOSING":drawChooseTypeOfPlayer(3)
        elif playerFour._typeofclass == "CHOOSING": drawChooseTypeOfPlayer(4)
        else:                                       GAMESTATUS = GameState.CHOOSEMENU
    elif GAMESTATUS == GameState.GAMELAUNCHED:
        gameboard_window.drawGameboard(screen)
        debug(getGameBoardPositionByMouse(pygame.mouse.get_pos()))

        # If a player is the winner
        if getPlayerByNum(round_number)._isWinner == True:
            # Winned !
            screen.blit(myfont_big.render("Le joueur " + str(round_number) + " a gagné !", 1, (255,100,100)), (400, 125))
        else:
            # Draw UI for good player
            for p in list_players:
                if p._number == round_number:
                    drawUI(p)
            # TODO Insert code to implement IA here
            if getPlayerByNum(round_number)._typeofclass.startswith("IA"):
                # If inventory is full
                if (len(getPlayerByNum(round_number)._inventory) >= 4):
                        closest_mine_distance : float = 99999999999
                        closest_mine_x = None
                        closest_mine_y = None
                        for i in range(len(gameboard_window._gameboard)):
                            for j in range(len(gameboard_window._gameboard)):
                                if (gameboard_window._gameboard[i][j] == "m"):
                                    # If the calculated distance is closed than before
                                    if sqrt(abs(i - getPlayerByNum(round_number)._pos[0]) + abs(j - getPlayerByNum(round_number)._pos[1])) < closest_mine_distance:
                                        closest_mine_distance = sqrt(abs(i - getPlayerByNum(round_number)._pos[0]) + abs(j - getPlayerByNum(round_number)._pos[1]))
                                        closest_mine_x = i
                                        closest_mine_y = j
                        debug("plus proche: " + str(closest_mine_x) + ", " + str(closest_mine_y), y=300)
                        is_it_right = closest_mine_y > getPlayerByNum(round_number)._pos[1]
                        is_it_left = closest_mine_y < getPlayerByNum(round_number)._pos[1]
                        is_it_up = closest_mine_x < getPlayerByNum(round_number)._pos[0]
                        is_it_bot = closest_mine_x > getPlayerByNum(round_number)._pos[0]
                        is_it_vertical_align = closest_mine_y == getPlayerByNum(round_number)._pos[1]
                        is_it_horizontal_align = closest_mine_x == getPlayerByNum(round_number)._pos[0] == 0

                        debug("droite : " + str(is_it_right), y=325)
                        debug("gauche: " +  str(is_it_left), y=350)
                        debug("haut: " + str(is_it_up), y=375)
                        debug("bas: " + str(is_it_bot), y=400)

                        debug("axe vertical similaire: " +  str(is_it_vertical_align), y=425)
                        debug("axe horizontale similaire: " +  str(is_it_horizontal_align), y=450)

                        if is_it_up:
                            # If can move up
                            if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0] - 1, (getPlayerByNum(round_number)._pos[1]))):
                                getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0] - 1, (getPlayerByNum(round_number)._pos[1])))
                        elif is_it_bot:
                            # If can move bot
                            if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0] + 1, (getPlayerByNum(round_number)._pos[1]))):
                                getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0] + 1, (getPlayerByNum(round_number)._pos[1])))
                        elif is_it_left:
                            # If can move left
                            if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] - 1))):
                                getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] - 1)))
                        elif is_it_right:
                            # If can move right
                            if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] + 1))):
                                getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] + 1)))
                        
                # Inventory is not full
                else:
                    # If inventory of other player is full (and different from the current player)
                    if len(getPlayerWithMaxedInventory(getPlayerByNum(round_number))._inventory) >= 4:
                        # If the player is a fighter
                        if getPlayerByNum(round_number)._typeofclass == "IA_FIGHTER":
                            # If they can fight
                            if getPlayerByNum(round_number)._canFight == True:
                                list_fighting_players.append(getPlayerWithMaxedInventory(getPlayerByNum(round_number)))
                                list_fighting_players.append(getPlayerByNum(round_number))
                                GAMESTATUS = GameState.FIGHT
                
                    closest_res_distance : float = 99999999999
                    closest_res_x = None
                    closest_res_y = None
                    for i in range(len(gameboard_window._gameboard)):
                        for j in range(len(gameboard_window._gameboard)):
                            if (gameboard_window._gameboard[i][j] == "res"):
                                # If the calculated distance is closed than before
                                if sqrt(abs(i - getPlayerByNum(round_number)._pos[0]) + abs(j - getPlayerByNum(round_number)._pos[1])) < closest_res_distance:
                                    closest_res_distance = sqrt(abs(i - getPlayerByNum(round_number)._pos[0]) + abs(j - getPlayerByNum(round_number)._pos[1]))
                                    closest_res_x = i
                                    closest_res_y = j
                    # Closest res founded
                    if closest_res_x != None and closest_res_y != None:
                        # If the ia can move on res, move
                        if getPlayerByNum(round_number).canMovePlayer((closest_res_x, closest_res_y)):
                            getPlayerByNum(round_number).movePlayer((closest_res_x, closest_res_y))
                        # If the ia can't move on res, try to approach
                        else:
                            debug("plus proche: " + str(closest_res_x) + ", " + str(closest_res_y), y=300)
                            is_it_right = closest_res_y > getPlayerByNum(round_number)._pos[1]
                            is_it_left = closest_res_y < getPlayerByNum(round_number)._pos[1]
                            is_it_up = closest_res_x < getPlayerByNum(round_number)._pos[0]
                            is_it_bot = closest_res_x > getPlayerByNum(round_number)._pos[0]
                            is_it_vertical_align = closest_res_y == getPlayerByNum(round_number)._pos[1]
                            is_it_horizontal_align = closest_res_x == getPlayerByNum(round_number)._pos[0] == 0

                            debug("droite : " + str(is_it_right), y=325)
                            debug("gauche: " +  str(is_it_left), y=350)
                            debug("haut: " + str(is_it_up), y=375)
                            debug("bas: " + str(is_it_bot), y=400)

                            debug("axe vertical similaire: " +  str(is_it_vertical_align), y=425)
                            debug("axe horizontale similaire: " +  str(is_it_horizontal_align), y=450)

                            if is_it_up:
                                # If can move up
                                if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0] - 1, (getPlayerByNum(round_number)._pos[1]))):
                                    getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0] - 1, (getPlayerByNum(round_number)._pos[1])))
                            elif is_it_bot:
                                # If can move bot
                                if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0] + 1, (getPlayerByNum(round_number)._pos[1]))):
                                    getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0] + 1, (getPlayerByNum(round_number)._pos[1])))
                            elif is_it_left:
                                # If can move left
                                if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] - 1))):
                                    getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] - 1)))
                            elif is_it_right:
                                # If can move right
                                if getPlayerByNum(round_number).canMovePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] + 1))):
                                    getPlayerByNum(round_number).movePlayer((getPlayerByNum(round_number)._pos[0], (getPlayerByNum(round_number)._pos[1] + 1)))
                            # If the IA can't move, find another  way
                            # TODO Diskjtra or go through the obstacles
                            if not is_it_left and not is_it_right and not is_it_up and not is_it_bot:
                                pass
                            else:
                                if is_it_left:
                                    pass
                                if is_it_right:
                                    pass
                                if is_it_up:
                                    pass
                                if is_it_bot:
                                    pass
                    # If res not founded
                    else:
                        if len(getPlayerWithMaxedInventory(getPlayerByNum(round_number))._inventory) >= 4:
                            # If they can fight
                            if getPlayerByNum(round_number)._canFight == True:
                                list_fighting_players.append(getPlayerWithMaxedInventory(getPlayerByNum(round_number)))
                                list_fighting_players.append(getPlayerByNum(round_number))
                                GAMESTATUS = GameState.FIGHT

    elif GAMESTATUS == GameState.FIGHT:
        drawFight()
        drawDice((350,325), random_dice_value_one)
        drawDice((875,325), random_dice_value_two)
        GAMESTATUS, playerLeftWinned, playerRightWinned, list_fighting_players, random_dice_value_one, random_dice_value_two = drawWinnerFight(playerLeftWinned, playerRightWinned)

    # RENDER YOUR GAME HERE
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(24)

pygame.quit()
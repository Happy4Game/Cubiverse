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

    # Draw show number of players
    screen.blit(pygame.image.load("./assets/png/show_infos.png").convert_alpha(), (993, 550))

    if show_infos:
        for p in list_players:
            if p._typeofclass != "UNDEFINED":
                coordinate : tuple = (1280 / 4.5 + p._pos[1]*50,p._pos[0]*50)
                screen.blit(pygame.image.load("./assets/png/number_" + str(p._number) + ".png").convert_alpha(), coordinate)

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
                last_pos = list_fighting_players[1]._pos
                # Si le personnage est mort
                if list_fighting_players[0].attack(list_fighting_players[1]) == True:
                    gameboard_window._gameboard[list_fighting_players[1]._pos[0]][list_fighting_players[1]._pos[1]] = list_fighting_players[1]._typeingameboard
                    gameboard_window._gameboard[last_pos[0]][last_pos[1]] = "g"
                    list_fighting_players[1]._inventory.clear()
                    gameboard_window.putRandomRes(4)
                else:    
                    list_fighting_players[1]._inventory.pop()
                    gameboard_window.putRandomRes(1)
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
                last_pos = list_fighting_players[0]._pos
                # Si le personnage est mort
                if list_fighting_players[1].attack(list_fighting_players[0]) == True:
                    gameboard_window._gameboard[list_fighting_players[0]._pos[0]][list_fighting_players[0]._pos[1]] = list_fighting_players[0]._typeingameboard
                    gameboard_window._gameboard[last_pos[0]][last_pos[1]] = "g"
                    list_fighting_players[0]._inventory.clear()
                    gameboard_window.putRandomRes(4)
                else:    
                    list_fighting_players[0]._inventory.pop()
                    gameboard_window.putRandomRes(1)
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

def createGraphFromGameboard(accept_m : bool = False):
    """Create graph to be used in Dijkstra
    
    Args:
        accept_m (bool): Do you need to go to "m"

    Returns:
        graph: Graph to be used in Dijkstra
    """
    rows, cols = len(gameboard_window._gameboard), len(gameboard_window._gameboard[0])
    graph = {}

    obstacles = {"b_one", "b_two", "b_one_r", "b_two_r", "_p_minor", "_p_fighter", "_p_ia_fighter", "_p_ia_minor"}

    if not accept_m:
        obstacles.add("m")        

    for row in range(rows):
        for col in range(cols):
            if gameboard_window._gameboard[row][col] in obstacles:
                # Pass obstacles
                continue 
            node = (row, col)
            graph[node] = []
            # Check case up, down, left, right
            for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_row, neighbor_col = row + d_row, col + d_col
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and gameboard_window._gameboard[neighbor_row][neighbor_col] not in obstacles:
                    neighbor_node = (neighbor_row, neighbor_col)
                    # 1 Height for moving
                    graph[node].append((1, neighbor_node))
    return graph

def dijkstraShortestPath(player_position : tuple, accept_m : bool = False):
    """Use Dijkstra algorithm to find the 

    Args:
        player_position (tuple): Pos of the player
        accept_m (bool): Do you need to go to "m"

    Returns:
        (previous, shortest_distances)
    """
    graph = createGraphFromGameboard(accept_m)

    nodes_to_visit = [(0, player_position)]
    shortest_distances = {node: float('infinity') for node in graph}
    shortest_distances[player_position] = 0
    previous_nodes = {node: None for node in graph}

    while nodes_to_visit:
        current_distance, current_node = min(nodes_to_visit, key=lambda x: x[0])
        nodes_to_visit.remove((current_distance, current_node))

        for neighbor_weight, neighbor_node in graph[current_node]:
            distance = current_distance + neighbor_weight

            if distance < shortest_distances[neighbor_node]:
                shortest_distances[neighbor_node] = distance
                previous_nodes[neighbor_node] = current_node
                nodes_to_visit.append((distance, neighbor_node))

    return previous_nodes, shortest_distances

def movePlayerToClosestType(player : Player, type_of_get_close : str):
    """Move player using Disjktra

    Args:
        player (Player): Player who wants to move
        type_of_get_close (str): Type of what we want to get close
    """
    player_position = player._pos
    if type_of_get_close == "m":
        previous_nodes, shortest_distances = dijkstraShortestPath(player_position, accept_m=True)
    else:
        previous_nodes, shortest_distances = dijkstraShortestPath(player_position)

    closest_res_distance = float('inf')
    closest_res_position = None

    # Find all type_of_get_close positions
    gameboard = gameboard_window._gameboard
    res_positions = [(i, j) for i in range(len(gameboard)) for j in range(len(gameboard[i])) if gameboard[i][j] == type_of_get_close]

    # Find the position the most close
    for res_position in res_positions:
        if shortest_distances[res_position] < closest_res_distance:
            closest_res_distance = shortest_distances[res_position]
            closest_res_position = res_position

    # If case founded, move the player
    if closest_res_position is not None:
        path_to_closest_res = []
        current_node = closest_res_position
        while current_node is not None:
            path_to_closest_res.append(current_node)
            current_node = previous_nodes[current_node]
        path_to_closest_res.reverse()

        # Move to player using path
        for step in path_to_closest_res:
            if player.canMovePlayer(step):
                player.movePlayer(step)
            else:
                # If the player can't move then force him to go at max range
                max_movement = player._maxrange
                while max_movement > 0:
                    player.movePlayer(step)
                    max_movement -= 1
                    if player.canMovePlayer(step):
                        break

def endRound(round_number) -> int:
    """End a round, must reassign the real round_number

    Args:
        round_number (int): actual round

    Returns:
        int: new round_number
    """
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
    return round_number
    

# pygame setup
pygame.init()
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont : pygame.font        = pygame.font.SysFont("monospace", 20)
myfont_little : pygame.font = pygame.font.SysFont("monospace", 16)
myfont_big : pygame.font    = pygame.font.SysFont("monospace", 40)

screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True
show_infos : bool = False


while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAMESTATUS == GameState.GAMELAUNCHED:

                # If a player want to show number of each player
                if getButtonPressed(pygame.mouse.get_pos(), (993, 550), (277,68)):
                    show_infos = not show_infos

                # If a player is in mouse pos                
                if isCellOccuped(getGameBoardPositionByMouse(pygame.mouse.get_pos())) and getPlayerByPos(getGameBoardPositionByMouse(pygame.mouse.get_pos()))._number != round_number:
                    #Fight
                    if getCell(getGameBoardPositionByMouse(pygame.mouse.get_pos())).__contains__("_p_"):
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
                    round_number = endRound(round_number)

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
            GAMESTATUS = GameState.WINNED
        else:
            # Draw UI for good player
            for p in list_players:
                if p._number == round_number:
                    drawUI(p)
            # TODO Insert code to implement IA here
            if getPlayerByNum(round_number)._typeofclass.startswith("IA"):
                # If inventory is full
                if (len(getPlayerByNum(round_number)._inventory) >= 4):
                        movePlayerToClosestType(getPlayerByNum(round_number), "m")
                        
                # Inventory is not full
                else:
                    # If inventory of other player is full (and different from the current player)
                    if getPlayerWithMaxedInventory(getPlayerByNum(round_number)) != None and len(getPlayerWithMaxedInventory(getPlayerByNum(round_number))._inventory) >= 4:
                        # If the player is a fighter
                        if getPlayerByNum(round_number)._typeofclass == "IA_FIGHTER":
                            # If they can fight
                            if getPlayerByNum(round_number)._canFight == True:
                                list_fighting_players.append(getPlayerWithMaxedInventory(getPlayerByNum(round_number)))
                                list_fighting_players.append(getPlayerByNum(round_number))
                                GAMESTATUS = GameState.FIGHT

                    # If inventory of other players are not full
                    else:
                        movePlayerToClosestType(getPlayerByNum(round_number), "res")
                round_number = endRound(round_number)
    elif GAMESTATUS == GameState.FIGHT:
        drawFight()
        drawDice((350,325), random_dice_value_one)
        drawDice((875,325), random_dice_value_two)
        GAMESTATUS, playerLeftWinned, playerRightWinned, list_fighting_players, random_dice_value_one, random_dice_value_two = drawWinnerFight(playerLeftWinned, playerRightWinned)

    elif GAMESTATUS == GameState.WINNED:
        screen.blit(myfont_big.render("Le joueur " + str(round_number) + " a gagné !", 1, (255,100,100)), (400, 325))
    # RENDER YOUR GAME HERE
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(24)

pygame.quit()
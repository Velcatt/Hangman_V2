import pygame
from views import GameGraph, MenuGraph, ScoreboardGraph
from models import Game, Menu, Scoreboard

# MAIN CODE ----------------------------------------------------

pygame.init()

screen = pygame.display.set_mode((600, 600))


isRunning = True
isMenu = True
isScoreboard = False
isGame = False

while isRunning:

    if isMenu:
        try:
            menu
        except NameError as e:
            menu = Menu()
            menu_graph = MenuGraph()
        while isMenu:
            pygame_event = pygame.event.poll()
            menu_graph.draw(screen, pygame_event)
            menu.set_name(menu_graph.name_input.text)
            menu_route = menu_graph.menu_route_check(pygame_event)
            isMenu = menu.update(menu_route)

            if menu_route == "Quit":
                isRunning = False
            elif menu_route == "Scoreboard":
                isScoreboard = True
            elif menu_route == "Hard":
                if isMenu:
                    menu_graph.name_input.color = pygame.Color("red")
                else:
                    isGame = True
            elif menu_route == "Easy":
                if isMenu:
                    menu_graph.name_input.color = pygame.Color("red")
                else:
                    isGame = True

            pygame.display.update()

    if isScoreboard:
        try:
            scoreboard
        except NameError as e:
            scoreboard = Scoreboard()
            scoreboard_graph = ScoreboardGraph(
                scoreboard.easy_converted_scorelist, scoreboard.hard_converted_scorelist
            )
        while isScoreboard:
            pygame_event = pygame.event.poll()
            scoreboard_graph.draw(screen)
            isScoreboard = not scoreboard_graph.back_to_menu_check(pygame_event)
            if not isScoreboard:
                isMenu = True

            if pygame_event.type == pygame.QUIT:
                isScoreboard = False
                isRunning = False
            pygame.display.update()

    if isGame:
        game = Game(menu_route, menu.name)
        game_graph = GameGraph(screen)
        while isGame:
            pygame_event = pygame.event.poll()
            isGame = game.update(game_graph.input_box.last_input)
            if isGame or (
                # Check to avoid screen blinking upon restarting a game
                game.current != game.goal
                and game_graph.input_box.last_input != "again"
            ):
                game_graph.draw(game, screen, pygame_event)

            if pygame_event.type == pygame.QUIT:
                isGame = False
                isRunning = False
            pygame.display.update()

        if game.newgame:
            isGame = True
        else:
            isGame = False
            isMenu = True

pygame.display.quit()
pygame.quit()

import pygame
from graphics import Graphics, Scoreboard
from game import Game, Menu

# MAIN CODE ----------------------------------------------------

pygame.init()

isMenu = True
newgame = True
isGame = True
event = pygame.event.Event(pygame.USEREVENT)
game_event = ""
menu_route = ""
name = ""

menu = Menu()

graphics = Graphics(menu)


while newgame:
    while isMenu:
        pygame_event = pygame.event.poll()
        if pygame_event.type == pygame.QUIT:
            game_event = "quit"
        quit_event = menu.quit_menu(game_event)
        newgame = quit_event
        name = graphics.name_input.text
        menu_route = graphics.menu_update(pygame_event) if quit_event else "Quit"
        isMenu = quit_event and (True if menu_route == "" else False)

    isGame = False if menu_route == "Quit" else True

    if menu_route == "Scoreboard":
        scoreboard = Scoreboard()
        isScoreboard = True
        while isScoreboard:
            pygame_event = pygame.event.poll()
            scoreboard.draw(graphics.window)
            pygame.display.update()
            if scoreboard.back_to_menu_check(pygame_event):
                isScoreboard = False
                isMenu = True
                isGame = False
            elif pygame_event.type == pygame.QUIT:
                isScoreboard = False
                isMenu = False
                isGame = False
                newgame = False
    elif name != "":
        graphics.input_box.reset_last_input()
        game = Game(menu_route, name)
        isGame = True
    else:
        isGame = False
        isMenu = True if menu_route != "Quit" else False
        newgame = True if menu_route != "Quit" else False
        graphics.name_input.color = pygame.Color("red")

    while isGame:
        pygame_event = pygame.event.poll()
        if pygame_event.type == pygame.QUIT:
            game_event = "quit"
        isGame = game.run(game_event)
        game.last_input = graphics.input_box.last_input
        newgame = game.newgame
        graphics.update(game, pygame_event)
        if not newgame and not isGame:
            isScoreboard = False
            isMenu = True
            isGame = False
            newgame = True
            graphics.name_input.color = pygame.Color("white")


pygame.display.quit()
pygame.quit()

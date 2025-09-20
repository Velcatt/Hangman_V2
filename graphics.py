import pygame
import ast
from inputbox import InputBox
from button import Button


class Graphics:

    def __init__(self, menu):
        self.easy = Button(200, 200, 200, 32, "Easy", pygame.Color("black"))
        self.hard = Button(200, 250, 200, 32, "Hard", pygame.Color("black"))
        self.scoreboard = Button(200, 300, 200, 32, "Scoreboard", pygame.Color("black"))
        self.quit = Button(200, 350, 200, 32, "Quit", pygame.Color("black"))
        self.title_font = pygame.font.SysFont(None, 40)
        self.title = self.title_font.render("HANGMAN", False, (0, 0, 0))
        self.name_font = pygame.font.SysFont(None, 25)
        self.name = self.name_font.render("Enter your name : ", False, (255, 255, 255))
        self.name_input = InputBox(200, 500, 200, 32, disabled=True)

        self.window = pygame.display.set_mode((600, 600))
        self.bg = pygame.image.load("pixelart.png")
        self.game_font = pygame.font.SysFont(None, 25)
        self.announcement_font = pygame.font.SysFont(None, 40)
        self.info_font = pygame.font.SysFont(None, 25)
        self.score_font = pygame.font.SysFont(None, 32)
        self.announcement = self.announcement_font.render("", False, (0, 0, 0))
        self.info = self.info_font.render("", False, (0, 0, 0))
        self.score = self.score_font.render("", False, (0, 0, 0))
        self.input_box = InputBox(50, 500, 140, 32)
        self.initialized = True

    def update(self, game, event):
        self.text_surface = self.render_word(game.current)
        self.info = self.info_font.render(game.info, False, (255, 255, 255))
        self.announcement = self.announcement_font.render(
            game.announcement, False, (0, 0, 0)
        )
        self.score = self.score_font.render(game.score, False, (0, 0, 0))

        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.announcement, (230, 350))
        self.window.blit(self.text_surface, (50, 460))
        self.window.blit(self.info, (270, 505))
        self.window.blit(self.score, (230, 375))

        self.input_box.update()
        self.input_box.handle_event(event)
        self.input_box.draw(self.window)

        self.hangman_draw(game.penalty)

        pygame.display.update()

    def menu_update(self, event):
        if self.easy.is_pressed(event):
            return "Easy"
        elif self.hard.is_pressed(event):
            return "Hard"
        elif self.scoreboard.is_pressed(event):
            return "Scoreboard"
        elif self.quit.is_pressed(event):
            return "Quit"
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.title, (200, 150))
        self.window.blit(self.name, (200, 450))
        self.easy.draw(self.window)
        self.hard.draw(self.window)
        self.scoreboard.draw(self.window)
        self.quit.draw(self.window)
        self.name_input.update()
        self.name_input.handle_event(event)
        self.name_input.draw(self.window)
        pygame.display.update()
        return ""

    def render_word(self, current):
        return self.game_font.render(self.step(current), False, (255, 255, 255))

    def step(self, current):
        result = ""
        for i in current:
            if i == "*":
                result += "_ "
            else:
                result += i + " "
        return result

    # HANGMAN DRAW FUNCTIONS ------------------------------------

    def draw_gallows_1(self):
        pygame.draw.line(self.window, (0, 0, 0), (150, 430), (150, 40), width=10)

    def draw_gallows_2(self):
        pygame.draw.line(self.window, (0, 0, 0), (150, 40), (300, 40), width=10)

    def draw_gallows_3(self):
        pygame.draw.line(self.window, (0, 0, 0), (150, 100), (250, 40), width=10)

    def draw_gallows_4(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 40), (300, 100), width=10)

    def draw_head(self):
        pygame.draw.circle(self.window, (0, 0, 0), (300, 100), 30)

    def draw_body(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 130), (300, 250), width=10)

    def draw_left_arm(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 130), (250, 210), width=10)

    def draw_right_arm(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 130), (350, 210), width=10)

    def draw_left_leg(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 250), (250, 330), width=10)

    def draw_right_leg(self):
        pygame.draw.line(self.window, (0, 0, 0), (300, 250), (350, 330), width=10)

    HANGMAN_DRAW_FUNCTIONS = [
        draw_gallows_1,
        draw_gallows_2,
        draw_gallows_3,
        draw_gallows_4,
        draw_head,
        draw_body,
        draw_left_arm,
        draw_right_arm,
        draw_left_leg,
        draw_right_leg,
    ]

    def hangman_draw(self, penalty):
        for i in range(min(penalty, 10)):

            self.HANGMAN_DRAW_FUNCTIONS[i](self)


class Scoreboard:

    def __init__(self):
        self.bg = pygame.image.load("pixelart_scoreboard.png")
        self.easy_scoreboard = [
            line.strip().lower() for line in open("best_scores_easy")
        ]
        self.hard_scoreboard = [
            line.strip().lower() for line in open("best_scores_hard")
        ]
        self.button_back_to_menu = Button(
            200, 500, 200, 32, "Back to menu", pygame.Color("white")
        )
        self.scoreboard_font = pygame.font.SysFont(None, 25)

        self.title_font = pygame.font.SysFont(None, 32)
        self.title_easy = self.title_font.render("Easy Mode", False, (255, 255, 255))
        self.title_hard = self.title_font.render("Hard Mode", False, (255, 255, 255))

        self.easy_converted_scorelist = []
        self.easy_scoreboard_display = []
        self.hard_converted_scorelist = []
        self.hard_scoreboard_display = []
        for element in self.easy_scoreboard:
            self.easy_converted_scorelist.append(ast.literal_eval(element))

        for i in range(len(self.easy_converted_scorelist)):
            self.easy_scoreboard_display.append(
                self.scoreboard_font.render(
                    str(i + 1)
                    + ". "
                    + self.easy_converted_scorelist[i][1]
                    + " - "
                    + self.easy_converted_scorelist[i][2]
                    + " attempts",
                    False,
                    (255, 255, 255),
                )
            )
        for element in self.hard_scoreboard:
            self.hard_converted_scorelist.append(ast.literal_eval(element))

        for i in range(len(self.hard_converted_scorelist)):
            self.hard_scoreboard_display.append(
                self.scoreboard_font.render(
                    str(i + 1)
                    + ". "
                    + self.hard_converted_scorelist[i][1]
                    + " - "
                    + self.hard_converted_scorelist[i][2]
                    + " attempts",
                    False,
                    (255, 255, 255),
                )
            )

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.title_easy, (25, 40))
        screen.blit(self.title_hard, (300, 40))
        self.button_back_to_menu.draw(screen)

        for i in range(len(self.easy_scoreboard_display)):
            screen.blit(self.easy_scoreboard_display[i], (25, 70 + i * 26))

        for i in range(len(self.hard_scoreboard_display)):
            screen.blit(self.hard_scoreboard_display[i], (300, 70 + i * 26))

    def back_to_menu_check(self, event):
        if self.button_back_to_menu.is_pressed(event):
            return True
        else:
            return False

import pygame
import random
import datetime
import ast
import string

EASY_ENGLISH_WORDS_SET = set(
    line.strip().lower() for line in open("word_list_easy.txt")
)

HARD_ENGLISH_WORDS_SET = set(
    line.strip().lower() for line in open("word_list_hard.txt")
)

ALPHABET_LIST = list(string.ascii_lowercase)


class Game:

    def __init__(self, menu_route, name):
        if menu_route == "Easy":
            self.menu_route = menu_route
            self.goal = self.randomset(EASY_ENGLISH_WORDS_SET)
        elif menu_route == "Hard":
            self.menu_route = menu_route
            self.goal = self.randomset(HARD_ENGLISH_WORDS_SET)
        self.penalty = 0
        self.attempts = 0
        self.best_score = []
        self.current = self.initcurrent(self.goal)
        self.guess = ""
        self.guessed_letters = []
        self.announcement = ""
        self.info = ""
        self.score = ""
        self.last_input = ""
        self.name = name
        self.newgame = True

    def randomset(self, s):
        return random.sample(sorted(s), 1)[0]

    def initcurrent(self, goal):
        current = ""
        for i in goal:
            current += "*"
        return current

    def lettercheck(self, letter, goal):
        return letter in goal

    def occurences(self, letter, goal):
        li = []
        for i in range(len(goal)):
            if goal[i] == letter:
                li.append(i)
        return li

    def step(self, current):
        result = ""
        for i in current:
            if i == "*":
                result += "_ "
            else:
                result += i + " "
        return result

    def save_score(self, best_score):
        converted_scorelist = []
        score_index = -1
        if self.menu_route == "Hard":
            file = "best_scores_hard"
            with open(file) as f:
                scorelist = f.read().splitlines()
        else:
            file = "best_scores_easy"
            with open(file) as f:
                scorelist = f.read().splitlines()
        for element in scorelist:
            converted_scorelist.append(ast.literal_eval(element))
        i = len(converted_scorelist) - 1
        while i >= 0:
            if int(best_score[2]) < int(converted_scorelist[0][2]):
                score_index = 0
                i = 0
            elif int(best_score[2]) < int(converted_scorelist[i][2]) and int(
                best_score[2]
            ) >= int(converted_scorelist[i - 1][2]):
                score_index = i
            i -= 1
        if score_index != -1:
            converted_scorelist.insert(score_index, best_score)
            if len(converted_scorelist) > 10:
                converted_scorelist.pop(10)
            with open(file, "w") as f:
                for element in converted_scorelist:
                    f.write(str(element) + "\n")

    def win(self):
        self.announcement = "YOU WIN!"
        self.score = "Score : " + str(self.attempts)
        self.best_score.append(datetime.date.today().isoformat())
        self.best_score.append(self.name)
        self.best_score.append(str(self.attempts))
        self.save_score(self.best_score)
        self.info = "Type 'again' to try again, 'quit' to quit"

    def lose(self):
        self.announcement = "YOU LOSE!"
        self.current = self.goal
        self.info = "Type 'again' to try again, 'quit' to quit"

    def replace_in_current(self, current, li, letter):
        newcurrent = ""
        for i in range(len(current)):
            if i in li:
                newcurrent += letter
            else:
                newcurrent += current[i]
        return newcurrent

    def update(self, last_input):
        if self.current == self.goal:
            if self.guess == "again":
                self.newgame = True
                return False
            elif self.guess == "quit":
                self.newgame = False
                return False
        if self.guess != last_input:
            self.guess = last_input
            if len(self.guess) > 1:
                self.attempts += 1
                if self.guess == self.goal:
                    self.current = self.goal
                    self.win()
                else:
                    self.info = "Incorrect guess!"
                    self.penalty += 3
            else:
                if self.guess in self.guessed_letters:
                    self.info = "You already tried '" + self.guess + "'"
                elif self.guess not in ALPHABET_LIST:
                    self.info = "Not a lowercase letter, try again !"
                else:
                    self.attempts += 1
                    self.guessed_letters.append(self.guess)
                    if self.lettercheck(self.guess, self.goal):
                        occ = self.occurences(self.guess, self.goal)
                        self.info = "Found " + str(len(occ)) + " '" + self.guess + "'"
                        self.current = self.replace_in_current(
                            self.current, occ, self.guess
                        )
                        if self.current == self.goal:
                            self.win()
                    else:
                        self.info = "No '" + self.guess + "' found"
                        self.penalty += 1
        if self.penalty >= 10:
            self.lose()
        return True


class Menu:

    def __init__(self):
        self.menu_route = ""
        self.name = ""

    def update(self, menu_route):
        self.menu_route = menu_route
        if menu_route in ["Quit", "Scoreboard"]:
            return False
        elif menu_route in ["Hard", "Easy"]:
            if self.name == "":
                return True
            else:
                return False
        else:
            return True

    def set_name(self, name):
        self.name = name


class Scoreboard:

    def __init__(self):
        self.easy_scoreboard = [line.strip() for line in open("best_scores_easy")]
        self.hard_scoreboard = [line.strip() for line in open("best_scores_hard")]
        self.easy_converted_scorelist = []
        self.easy_scoreboard_display = []
        self.hard_converted_scorelist = []
        self.hard_scoreboard_display = []
        for element in self.easy_scoreboard:
            self.easy_converted_scorelist.append(ast.literal_eval(element))

        for element in self.hard_scoreboard:
            self.hard_converted_scorelist.append(ast.literal_eval(element))

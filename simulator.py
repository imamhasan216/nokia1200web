import json
import os
from config import *
from display import Display
from snake import Snake
from rapid_roll import RapidRoll

SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscores.json")


def icon_snake(d):
    for x, y in [(30, 26), (34, 26), (38, 26), (42, 26), (42, 22), (42, 18)]:
        d.rect(x, y, 3, 3)
    d.rect(52, 27, 2, 2)                  # food


def icon_roll(d):
    d.rect(34, 30, 28, 3)                 # platform
    d.circle(48, 26, 3)                   # ball


MENU_ITEMS = [("GAMES", GAME_SELECT), ("HIGH SCORES", HIGH_SCORES)]
GAMES = [("SNAKE II", SNAKE, icon_snake), ("RAPID ROLL", RAPID_ROLL, icon_roll)]


class Simulator:
    def __init__(self):
        self.d = Display()
        self.state = MAIN_MENU
        self.menu_sel = 0
        self.game_sel = 0
        self.game = None
        self.last_game = SNAKE
        self.best = self.load_best()

    # ---------- high scores (saved in a file) ----------
    def load_best(self):
        best = {SNAKE: 0, RAPID_ROLL: 0}
        try:
            with open(SCORE_FILE) as f:
                best.update(json.load(f))
        except (OSError, ValueError):
            pass
        return best

    def save_best(self):
        try:
            with open(SCORE_FILE, "w") as f:
                json.dump(self.best, f)
        except OSError:
            pass

    def start(self, which):
        return Snake() if which == SNAKE else RapidRoll()

    # ---------- one key press ----------
    def press(self, key):
        s = self.state

        if s == MAIN_MENU:
            if key == "ArrowRight":
                self.menu_sel = (self.menu_sel + 1) % len(MENU_ITEMS)
            elif key == "ArrowLeft":
                self.menu_sel = (self.menu_sel - 1) % len(MENU_ITEMS)
            elif key == "Enter":
                self.state = MENU_ITEMS[self.menu_sel][1]

        elif s == GAME_SELECT:
            if key == "ArrowRight":
                self.game_sel = (self.game_sel + 1) % len(GAMES)
            elif key == "ArrowLeft":
                self.game_sel = (self.game_sel - 1) % len(GAMES)
            elif key == "Enter":
                self.last_game = GAMES[self.game_sel][1]
                self.game = self.start(self.last_game)
                self.state = self.last_game
            elif key == "Escape":
                self.state = MAIN_MENU

        elif s in (SNAKE, RAPID_ROLL):
            if key == "Escape":
                self.state = GAME_SELECT
            else:
                self.game.handle_key(key)

        elif s == GAME_OVER:
            if key == "Enter":
                self.game = self.start(self.last_game)
                self.state = self.last_game
            elif key == "Escape":
                self.state = GAME_SELECT

        elif s == HIGH_SCORES:
            if key in ("Escape", "Enter"):
                self.state = MAIN_MENU

    # ---------- update ----------
    def update(self, dt, held):
        if self.state in (SNAKE, RAPID_ROLL):
            self.game.update(dt, held)
            if self.game.game_over:
                self.best[self.state] = max(self.best[self.state], self.game.score)
                self.save_best()
                self.state = GAME_OVER

    # ---------- draw ----------
    def softkeys(self, left="", right=""):
        d = self.d
        d.rect(0, 59, SCREEN_W, 1)
        if left:
            d.text(left, 2, 62)
        if right:
            d.text(right, 2, 62, right=True)

    def draw(self):
        d = self.d
        s = self.state

        if s == MAIN_MENU:
            d.clear()
            d.text("MENU", 0, 1, center=True)
            d.rect(0, 8, SCREEN_W, 1)
            d.text(MENU_ITEMS[self.menu_sel][0], 0, 24, center=True, scale=2)
            d.text("<", 3, 27)
            d.text(">", 3, 27, right=True)
            d.text(f"{self.menu_sel + 1}/{len(MENU_ITEMS)}", 0, 44, center=True)
            self.softkeys("SELECT")

        elif s == GAME_SELECT:
            title, _, icon = GAMES[self.game_sel]
            d.clear()
            d.text("GAMES", 0, 1, center=True)
            d.rect(0, 8, SCREEN_W, 1)
            icon(d)
            d.text("<", 3, 40)
            d.text(">", 3, 40, right=True)
            d.text(title, 0, 40, center=True)
            d.text(f"{self.game_sel + 1}/{len(GAMES)}", 0, 49, center=True)
            self.softkeys("SELECT", "BACK")

        elif s in (SNAKE, RAPID_ROLL):
            self.game.draw(d)

        elif s == GAME_OVER:
            d.clear()
            d.text("GAME OVER", 0, 10, center=True, scale=2)
            d.text(f"SCORE: {self.game.score}", 0, 32, center=True)
            d.text(f"BEST: {self.best[self.last_game]}", 0, 42, center=True)
            self.softkeys("RETRY", "BACK")

        elif s == HIGH_SCORES:
            d.clear()
            d.text("HIGH SCORES", 0, 1, center=True)
            d.rect(0, 8, SCREEN_W, 1)
            d.text(f"SNAKE II: {self.best[SNAKE]}", 6, 18)
            d.text(f"RAPID ROLL: {self.best[RAPID_ROLL]}", 6, 30)
            self.softkeys("", "BACK")

    # ---------- one full frame ----------
    def step(self, pressed, held, dt):
        for key in pressed:
            self.press(key)
        self.update(dt, held)
        self.draw()
        return self.d.to_string()
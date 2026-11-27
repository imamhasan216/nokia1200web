import random
from config import SCREEN_W, SCREEN_H

CELL = 4
TOP = 12
COLS = SCREEN_W // CELL
ROWS = (SCREEN_H - TOP) // CELL

DIRS = {
    "ArrowUp": (0, -1), "ArrowDown": (0, 1),
    "ArrowLeft": (-1, 0), "ArrowRight": (1, 0),
}


class Snake:
    def __init__(self):
        self.body = [(5, 7), (4, 7), (3, 7)]
        self.dir = (1, 0)
        self.next_dir = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.timer = 0.0
        self.step = 0.14          # seconds per move
        self.game_over = False

    def spawn_food(self):
        while True:
            p = (random.randrange(COLS), random.randrange(ROWS))
            if p not in self.body:
                return p

    def handle_key(self, key):
        d = DIRS.get(key)
        if d and (d[0] != -self.dir[0] or d[1] != -self.dir[1]):
            self.next_dir = d

    def update(self, dt, held):
        self.timer += dt
        if self.timer < self.step:
            return
        self.timer = 0
        self.dir = self.next_dir
        head = (self.body[0][0] + self.dir[0], self.body[0][1] + self.dir[1])

        hit_wall = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        if hit_wall or head in self.body:
            self.game_over = True
            return

        self.body.insert(0, head)
        if head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.body.pop()

    def draw(self, d):
        d.clear()
        d.text(self.score, 2, 1)
        d.rect(0, TOP - 2, SCREEN_W, 1)
        for x, y in self.body:
            d.rect(x * CELL, TOP + y * CELL, CELL - 1, CELL - 1)
        fx, fy = self.food
        d.rect(fx * CELL + 1, TOP + fy * CELL + 1, 2, 2)
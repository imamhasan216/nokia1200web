import random
from config import SCREEN_W, SCREEN_H

R = 3
TOP = 10
PLAT_W = 24


class RapidRoll:
    def __init__(self):
        self.x = 48.0
        self.y = 20.0
        self.vy = 0.0
        self.speed = 22.0         # how fast platforms rise (pixels/second)
        self.platforms = [[random.randint(0, SCREEN_W - PLAT_W), y, PLAT_W]
                          for y in range(30, SCREEN_H + 20, 16)]
        self.platforms[0][0] = SCREEN_W // 2 - PLAT_W // 2   # first one under the ball
        self.score = 0
        self.game_over = False

    def handle_key(self, key):
        pass                      # movement is read continuously in update()

    def update(self, dt, held):
        move = (1 if "ArrowRight" in held else 0) - (1 if "ArrowLeft" in held else 0)
        self.x = max(R, min(SCREEN_W - R, self.x + move * 45 * dt))

        for p in self.platforms:
            p[1] -= self.speed * dt
        if self.platforms[0][1] < TOP:
            self.platforms.pop(0)
            self.score += 1
        if self.platforms[-1][1] < SCREEN_H - 16:
            self.platforms.append([random.randint(0, SCREEN_W - PLAT_W), SCREEN_H, PLAT_W])

        self.vy += 120 * dt
        self.y += self.vy * dt

        for px, py, pw in self.platforms:
            bottom = self.y + R
            if px - R <= self.x <= px + pw + R and py <= bottom <= py + 5 and self.vy >= 0:
                self.y = py - R
                self.vy = 0

        if self.y - R < TOP or self.y - R > SCREEN_H:
            self.game_over = True

    def draw(self, d):
        d.clear()
        d.text(self.score, 2, 1)
        d.rect(0, TOP - 1, SCREEN_W, 1)
        for px, py, pw in self.platforms:
            d.rect(px, py, pw, 3)
        d.circle(self.x, self.y, R)
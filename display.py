import math
from config import SCREEN_W, SCREEN_H, LETTER_SPACING

GLYPH_W = 3

GLYPHS = {
    " ": ("...", "...", "...", "...", "..."),
    "A": (".#.", "#.#", "###", "#.#", "#.#"),
    "B": ("##.", "#.#", "##.", "#.#", "##."),
    "C": (".##", "#..", "#..", "#..", ".##"),
    "D": ("##.", "#.#", "#.#", "#.#", "##."),
    "E": ("###", "#..", "##.", "#..", "###"),
    "F": ("###", "#..", "##.", "#..", "#.."),
    "G": (".##", "#..", "#.#", "#.#", ".##"),
    "H": ("#.#", "#.#", "###", "#.#", "#.#"),
    "I": ("###", ".#.", ".#.", ".#.", "###"),
    "J": ("..#", "..#", "..#", "#.#", ".#."),
    "K": ("#.#", "#.#", "##.", "#.#", "#.#"),
    "L": ("#..", "#..", "#..", "#..", "###"),
    "M": ("#.#", "###", "###", "#.#", "#.#"),
    "N": ("##.", "#.#", "#.#", "#.#", "#.#"),
    "O": (".#.", "#.#", "#.#", "#.#", ".#."),
    "P": ("##.", "#.#", "##.", "#..", "#.."),
    "Q": (".#.", "#.#", "#.#", "###", "..#"),
    "R": ("##.", "#.#", "##.", "#.#", "#.#"),
    "S": (".##", "#..", ".#.", "..#", "##."),
    "T": ("###", ".#.", ".#.", ".#.", ".#."),
    "U": ("#.#", "#.#", "#.#", "#.#", "###"),
    "V": ("#.#", "#.#", "#.#", "#.#", ".#."),
    "W": ("#.#", "#.#", "###", "###", "#.#"),
    "X": ("#.#", "#.#", ".#.", "#.#", "#.#"),
    "Y": ("#.#", "#.#", ".#.", ".#.", ".#."),
    "Z": ("###", "..#", ".#.", "#..", "###"),
    "0": ("###", "#.#", "#.#", "#.#", "###"),
    "1": (".#.", "##.", ".#.", ".#.", "###"),
    "2": ("##.", "..#", ".#.", "#..", "###"),
    "3": ("##.", "..#", ".#.", "..#", "##."),
    "4": ("#.#", "#.#", "###", "..#", "..#"),
    "5": ("###", "#..", "##.", "..#", "##."),
    "6": (".##", "#..", "###", "#.#", "###"),
    "7": ("###", "..#", ".#.", ".#.", ".#."),
    "8": ("###", "#.#", "###", "#.#", "###"),
    "9": ("###", "#.#", "###", "..#", "##."),
    ":": ("...", ".#.", "...", ".#.", "..."),
    ".": ("...", "...", "...", "...", ".#."),
    "-": ("...", "...", "###", "...", "..."),
    "/": ("..#", "..#", ".#.", "#..", "#.."),
    "!": (".#.", ".#.", ".#.", "...", ".#."),
    "<": ("..#", ".#.", "#..", ".#.", "..#"),
    ">": ("#..", ".#.", "..#", ".#.", "#.."),
}

# turns bytes 0/1 into the characters "0"/"1"
_TO_TEXT = bytes.maketrans(b"\x00\x01", b"01")


class Display:
    """A 96 x 68 monochrome screen. 1 = dark pixel, 0 = light pixel."""

    def __init__(self):
        self.pixels = bytearray(SCREEN_W * SCREEN_H)

    def clear(self):
        self.pixels[:] = bytes(SCREEN_W * SCREEN_H)

    def pixel(self, x, y, color=1):
        if 0 <= x < SCREEN_W and 0 <= y < SCREEN_H:
            self.pixels[y * SCREEN_W + x] = color

    def rect(self, x, y, w, h, color=1):
        x0 = max(0, math.floor(x))
        x1 = min(SCREEN_W, math.floor(x) + int(w))
        y0 = max(0, math.floor(y))
        y1 = min(SCREEN_H, math.floor(y) + int(h))
        if x1 <= x0:
            return
        row = bytes([color]) * (x1 - x0)
        for yy in range(y0, y1):
            self.pixels[yy * SCREEN_W + x0: yy * SCREEN_W + x1] = row

    def circle(self, cx, cy, r, color=1):
        cx, cy = round(cx), round(cy)
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r + 1:
                    self.pixel(cx + dx, cy + dy, color)

    def text_width(self, s, scale=1):
        s = str(s)
        if not s:
            return 0
        return (len(s) * (GLYPH_W + LETTER_SPACING) - LETTER_SPACING) * scale

    def text(self, s, x, y, color=1, center=False, right=False, scale=1):
        s = str(s).upper()
        w = self.text_width(s, scale)
        if center:
            x = (SCREEN_W - w) // 2
        elif right:
            x = SCREEN_W - w - x
        for ch in s:
            rows = GLYPHS.get(ch, GLYPHS[" "])
            for ry, row in enumerate(rows):
                for rx, c in enumerate(row):
                    if c == "#":
                        self.rect(x + rx * scale, y + ry * scale, scale, scale, color)
            x += (GLYPH_W + LETTER_SPACING) * scale

    def to_string(self):
        """The whole frame as a string of 0s and 1s (sent to the browser)."""
        return bytes(self.pixels).translate(_TO_TEXT).decode("ascii")
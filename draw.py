#!/usr/bin/env python3
"""Draw the ai-happy-01 v7 picture: a medal ceremony in a sunny garden.

A crowned robot judge stands on a red-carpet stage wearing a big gold
medal, while a child waves a bouquet on the left and a dog sits under
a heart balloon on the right. A banner reads "BEST JUDGE EVER" and
"thank you!" runs along the bottom. Crayon style: bright flat colours,
thick dark outlines, wobbly confetti.

Standard library only. Run: python3 draw.py  ->  writes happy.png
(1024x1024, deterministic: same bytes every run).
"""
import math
import random
import struct
import zlib

W, H = 1024, 1024
OUT = "happy.png"

# palette
SKY_TOP = (159, 216, 255)
SKY_BOT = (232, 247, 255)
SUN = (255, 217, 59)
SUN_OUT = (244, 164, 41)
CLOUD = (255, 255, 255)
LAWN = (126, 200, 80)
HILL = (104, 184, 66)
CARPET = (225, 75, 75)
CARPET_EDGE = (178, 44, 44)
GOLD = (255, 209, 60)
GOLD_DARK = (214, 154, 20)
ROBOT = (188, 214, 232)
ROBOT_LIGHT = (215, 233, 247)
RIBBON = (214, 48, 49)
SKIN = (255, 217, 179)
HAIR = (122, 72, 32)
SHIRT = (235, 84, 84)
DOG = (176, 122, 69)
DOG_DARK = (128, 84, 40)
HEART = (232, 48, 84)
INK = (34, 48, 74)
BANNER_BG = (255, 255, 255)
RED_TXT = (214, 48, 49)
BLUE_TXT = (31, 58, 147)
PINK_TXT = (232, 80, 160)

# 5x7 bitmap font, only the glyphs we need.
FONT = {
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    't': ("..#..", "..#..", "#####", "..#..", "..#..", "..#..", "..#.."),
    'h': ("#....", "#....", "#....", "####.", "#...#", "#...#", "#...#"),
    'a': (".....", ".....", ".###.", "....#", ".####", "#...#", ".###."),
    'n': (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'k': ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    'y': (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    'o': (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    'u': (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1)):
            base = y * self.w
            for x in range(max(0, x0), min(self.w, x1)):
                i = (base + x) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect_outline(self, x0, y0, x1, y1, c, t=4):
        self.fill_rect(x0, y0, x1, y0 + t, c)
        self.fill_rect(x0, y1 - t, x1, y1, c)
        self.fill_rect(x0, y0, x0 + t, y1, c)
        self.fill_rect(x1 - t, y0, x1, y1, c)

    def fill_circle(self, cx, cy, r, c):
        for y in range(cy - r, cy + r + 1):
            dx = int(math.sqrt(max(0, r * r - (y - cy) ** 2)))
            for x in range(cx - dx, cx + dx + 1):
                self.set(x, y, c)

    def circle_outline(self, cx, cy, r, c, t=4):
        for k in range(t):
            rr = r - k
            for y in range(cy - rr, cy + rr + 1):
                dx = int(math.sqrt(max(0, rr * rr - (y - cy) ** 2)))
                self.set(cx - dx, y, c)
                self.set(cx + dx, y, c)

    def fill_ellipse(self, cx, cy, rx, ry, c):
        for y in range(cy - ry, cy + ry + 1):
            t = (y - cy) / ry
            dx = int(rx * math.sqrt(max(0.0, 1.0 - t * t)))
            for x in range(cx - dx, cx + dx + 1):
                self.set(x, y, c)

    def ellipse_outline(self, cx, cy, rx, ry, c, t=4):
        for k in range(t):
            self._ellipse_ring(cx, cy, rx - k, ry - k, c)

    def _ellipse_ring(self, cx, cy, rx, ry, c):
        steps = max(8, int(2 * math.pi * max(rx, ry)))
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.set(int(cx + rx * math.cos(a)), int(cy + ry * math.sin(a)), c)

    def thick_line(self, x0, y0, x1, y1, c, t=6):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1) * 2
        for i in range(steps + 1):
            x = int(x0 + (x1 - x0) * i / steps)
            y = int(y0 + (y1 - y0) * i / steps)
            self.fill_circle(x, y, t // 2, c)

    def fill_polygon(self, pts, c):
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(int(math.ceil(a)), int(b) + 1):
                    self.set(x, y, c)

    def draw_star(self, cx, cy, r, c):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        self.fill_polygon([(int(x), int(y)) for x, y in pts], c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '#':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       cx + (col + 1) * scale,
                                       y + (row + 1) * scale, c)
            cx += 6 * scale

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def vgrad(self, y0, y1, top, bot):
        for y in range(y0, y1):
            f = (y - y0) / max(1, y1 - y0 - 1)
            c = tuple(int(top[i] + (bot[i] - top[i]) * f) for i in range(3))
            self.fill_rect(0, y, self.w, y + 1, c)

    def to_png(self):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * stride:(y + 1) * stride]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(kind, data):
            out = struct.pack(">I", len(data)) + kind + data
            return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def draw_background(cv):
    """Sky, sun, clouds, lawn and the red-carpet stage."""
    cv.vgrad(0, 660, SKY_TOP, SKY_BOT)
    # sun, top right
    cv.fill_circle(878, 112, 66, SUN)
    cv.circle_outline(878, 112, 66, SUN_OUT, 5)
    for i in range(8):
        a = math.pi * i / 4 + 0.2
        cv.thick_line(int(878 + 84 * math.cos(a)), int(112 + 84 * math.sin(a)),
                      int(878 + 112 * math.cos(a)), int(112 + 112 * math.sin(a)),
                      SUN_OUT, 7)
    cv.fill_circle(878, 112, 66, SUN)
    cv.circle_outline(878, 112, 66, SUN_OUT, 5)
    # clouds
    for (cx, cy, s) in ((170, 130, 1.0), (700, 60, 0.7), (120, 300, 0.6)):
        cv.fill_ellipse(cx, cy, int(70 * s), int(26 * s), CLOUD)
        cv.fill_ellipse(cx - int(40 * s), cy + int(8 * s), int(44 * s),
                        int(20 * s), CLOUD)
        cv.fill_ellipse(cx + int(42 * s), cy + int(8 * s), int(46 * s),
                        int(20 * s), CLOUD)
    # lawn + hill
    cv.fill_rect(0, 640, W, H, LAWN)
    cv.fill_ellipse(512, 1060, 720, 150, HILL)
    cv.fill_rect(0, 960, W, H, LAWN)
    # flowers on the lawn
    for (fx, fy, petal) in ((90, 900, (232, 80, 160)), (180, 960, (255, 209, 60)),
                            (930, 890, (150, 120, 220)), (850, 960, (232, 80, 160)),
                            (60, 780, (255, 255, 255)), (970, 770, (255, 209, 60))):
        cv.thick_line(fx, fy, fx, fy - 34, (46, 125, 50), 5)
        for a in range(6):
            ang = math.pi * a / 3
            cv.fill_circle(int(fx + 13 * math.cos(ang)),
                           int(fy - 40 + 13 * math.sin(ang)), 9, petal)
        cv.fill_circle(fx, fy - 40, 9, GOLD)
    # red carpet stage
    cv.fill_ellipse(512, 850, 330, 78, CARPET)
    cv.ellipse_outline(512, 850, 330, 78, CARPET_EDGE, 5)
    cv.ellipse_outline(512, 850, 300, 60, GOLD, 4)


def draw_banner(cv):
    """White ribbon banner with the big thank-you words."""
    cv.fill_rect(112, 34, 912, 126, BANNER_BG)
    cv.rect_outline(112, 34, 912, 126, INK, 5)
    # folded ribbon ends
    cv.fill_polygon([(112, 34), (152, 80), (112, 126)], RED_TXT)
    cv.fill_polygon([(912, 34), (872, 80), (912, 126)], RED_TXT)
    words = [("BEST", RED_TXT), ("JUDGE", BLUE_TXT), ("EVER", RED_TXT)]
    total = sum(cv.text_width(w, 7) for w, _ in words) + 2 * 24
    x = 512 - total // 2
    y = 34 + (126 - 34 - 7 * 7) // 2
    for w, col in words:
        cv.text(x, y, w, 7, col)
        x += cv.text_width(w, 7) + 24


def draw_confetti(cv):
    """Fixed-seed confetti and stars, deterministic."""
    rng = random.Random(7)
    cols = [(232, 80, 160), (255, 209, 60), (31, 58, 147),
            (46, 160, 220), (150, 120, 220), (235, 84, 84)]
    for _ in range(64):
        x = rng.randint(30, 994)
        y = rng.randint(150, 980)
        if 380 < y < 900 and 380 < x < 650:
            continue  # keep the judge clear
        c = cols[rng.randrange(len(cols))]
        if rng.random() < 0.5:
            cv.fill_rect(x, y, x + 12, y + 7, c)
        else:
            cv.fill_circle(x, y, 6, c)
    for (sx, sy) in ((70, 200), (950, 350), (330, 180), (690, 220), (60, 560)):
        cv.draw_star(sx, sy, 16, GOLD)


def draw_judge(cv):
    """The crowned robot judge on the stage, arms raised, big gold medal."""
    # arms first (behind body)
    cv.thick_line(452, 620, 386, 516, ROBOT, 22)
    cv.thick_line(572, 620, 638, 516, ROBOT, 22)
    cv.thick_line(452, 620, 386, 516, INK, 26)
    cv.thick_line(452, 620, 386, 516, ROBOT, 18)
    cv.thick_line(572, 620, 638, 516, ROBOT, 18)
    cv.fill_circle(382, 510, 20, ROBOT)
    cv.circle_outline(382, 510, 20, INK, 4)
    cv.fill_circle(642, 510, 20, ROBOT)
    cv.circle_outline(642, 510, 20, INK, 4)
    # legs
    cv.fill_rect(472, 756, 496, 812, INK)
    cv.fill_rect(528, 756, 552, 812, INK)
    # body
    cv.fill_rect(442, 560, 582, 762, ROBOT)
    cv.rect_outline(442, 560, 582, 762, INK, 5)
    cv.fill_rect(452, 570, 572, 600, ROBOT_LIGHT)
    # head
    cv.fill_rect(452, 428, 572, 562, ROBOT_LIGHT)
    cv.rect_outline(452, 428, 572, 562, INK, 5)
    # crown
    cv.fill_polygon([(462, 428), (462, 392), (487, 414), (512, 384),
                     (537, 414), (562, 392), (562, 428)], GOLD)
    cv.fill_polygon([(462, 428), (462, 392), (487, 414), (512, 384),
                     (537, 414), (562, 392), (562, 428)], GOLD)
    for (jx, jy) in ((487, 404), (512, 394), (537, 404)):
        cv.fill_circle(jx, jy, 5, RIBBON)
    # face
    cv.fill_circle(487, 492, 13, INK)
    cv.fill_circle(537, 492, 13, INK)
    cv.fill_circle(491, 488, 4, (255, 255, 255))
    cv.fill_circle(541, 488, 4, (255, 255, 255))
    cv.fill_circle(462, 522, 11, (255, 150, 170))
    cv.fill_circle(562, 522, 11, (255, 150, 170))
    # smile: thick arc
    for i in range(21):
        a = math.pi * (0.15 + 0.7 * i / 20)
        cv.fill_circle(int(512 + 34 * math.cos(a)),
                       int(512 + 22 * math.sin(a)), 4, INK)
    # medal ribbon + medal
    cv.fill_polygon([(492, 562), (522, 562), (512, 648)], RIBBON)
    cv.fill_polygon([(492, 562), (536, 562), (512, 648)], RIBBON)
    cv.fill_circle(512, 662, 56, GOLD)
    cv.circle_outline(512, 662, 56, GOLD_DARK, 5)
    cv.circle_outline(512, 662, 44, GOLD_DARK, 3)
    cv.draw_star(512, 662, 26, RIBBON)


def draw_child(cv):
    """Crayon child on the left, holding up a flower bouquet."""
    # legs
    cv.fill_rect(232, 862, 252, 946, (31, 58, 147))
    cv.fill_rect(268, 862, 288, 946, (31, 58, 147))
    # striped shirt
    cv.fill_rect(214, 748, 306, 866, SHIRT)
    cv.rect_outline(214, 748, 306, 866, INK, 5)
    cv.fill_rect(214, 772, 306, 788, (255, 255, 255))
    cv.fill_rect(214, 812, 306, 828, (255, 255, 255))
    # arms up to the bouquet
    cv.thick_line(222, 770, 176, 690, SKIN, 16)
    cv.thick_line(298, 770, 344, 690, SKIN, 16)
    # bouquet: three flowers
    for (fx, fy, petal) in ((176, 676, (232, 80, 160)),
                            (260, 660, (255, 209, 60)),
                            (344, 676, (150, 120, 220))):
        cv.thick_line(fx, fy + 10, 260, 700, (46, 125, 50), 4)
        for a in range(6):
            ang = math.pi * a / 3
            cv.fill_circle(int(fx + 14 * math.cos(ang)),
                           int(fy + 14 * math.sin(ang)), 10, petal)
        cv.fill_circle(fx, fy, 9, GOLD)
    # head + hair + face
    cv.fill_circle(260, 700, 46, SKIN)
    cv.circle_outline(260, 700, 46, INK, 5)
    cv.fill_ellipse(260, 672, 46, 26, HAIR)
    cv.fill_circle(244, 692, 8, INK)
    cv.fill_circle(276, 692, 8, INK)
    for i in range(13):
        a = math.pi * (0.2 + 0.6 * i / 12)
        cv.fill_circle(int(260 + 20 * math.cos(a)),
                       int(706 + 14 * math.sin(a)), 3, INK)


def draw_dog(cv):
    """Cheerful sitting dog on the right, heart balloon above."""
    # tail
    cv.thick_line(700, 830, 656, 748, DOG_DARK, 14)
    cv.fill_circle(652, 742, 14, DOG_DARK)
    # body + legs
    cv.fill_ellipse(786, 852, 92, 66, DOG)
    cv.ellipse_outline(786, 852, 92, 66, INK, 5)
    cv.fill_rect(716, 890, 742, 946, DOG)
    cv.fill_rect(806, 890, 832, 946, DOG)
    # head + ear + snout
    cv.fill_circle(836, 762, 52, DOG)
    cv.circle_outline(836, 762, 52, INK, 5)
    cv.fill_ellipse(792, 736, 20, 34, DOG_DARK)
    cv.fill_ellipse(848, 792, 26, 18, (232, 200, 160))
    cv.fill_circle(866, 786, 10, INK)
    cv.fill_circle(822, 748, 9, INK)
    cv.fill_circle(825, 745, 3, (255, 255, 255))
    # balloon string + heart
    cv.thick_line(836, 700, 836, 590, INK, 3)
    hx, hy = 836, 560
    cv.fill_circle(hx - 24, hy, 26, HEART)
    cv.fill_circle(hx + 24, hy, 26, HEART)
    cv.fill_polygon([(hx - 48, hy + 6), (hx + 48, hy + 6), (hx, hy + 62)],
                    HEART)
    cv.fill_circle(hx - 24, hy, 26, HEART)
    cv.fill_circle(hx + 24, hy, 26, HEART)
    cv.fill_polygon([(hx - 48, hy + 6), (hx + 48, hy + 6), (hx, hy + 62)],
                    HEART)
    cv.draw_star(hx, hy + 4, 12, (255, 255, 255))


def main():
    cv = Canvas(W, H, SKY_BOT)
    draw_background(cv)
    draw_banner(cv)
    draw_judge(cv)
    draw_child(cv)
    draw_dog(cv)
    draw_confetti(cv)
    # bottom words
    s = "thank you!"
    x = 512 - cv.text_width(s, 6) // 2
    cv.text(x, 952, s, 6, BLUE_TXT)
    data = cv.to_png()
    with open(OUT, "wb") as f:
        f.write(data)
    print(f"wrote {OUT} {len(data)} bytes, (1024, 1024)")


if __name__ == "__main__":
    main()

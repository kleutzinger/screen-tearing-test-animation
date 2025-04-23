import numpy as np
from PIL import Image, ImageDraw

HEIGHT = 1080
WIDTH = 1920

WHITE = 255
BLACK = 0

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2

CENTER = (MID_X, MID_Y)


def rot_cross_image(radians: float, filename="out.png") -> None:
    im = Image.new("L", (WIDTH, HEIGHT), WHITE)
    # modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

    draw = ImageDraw.Draw(im)
    # draw.line((0, 0) + im.size, fill=128, width=100)
    r = WIDTH * 2

    x = np.cos(radians) * r
    x += MID_X
    y = np.sin(radians) * r
    y += MID_Y
    draw.line((WIDTH - x, HEIGHT - y, x, y), fill=BLACK, width=50)

    im.save(filename)


def main():
    i = 0
    for p in np.linspace(0, np.pi, 60):
        fname = f"img/{i:05}.png"
        rot_cross_image(p, fname)
        print(i)
        i += 1


if __name__ == "__main__":
    main()

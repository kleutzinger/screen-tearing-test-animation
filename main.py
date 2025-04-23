#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "pillow",
# ]
# ///

import subprocess
import shlex

import numpy as np
from PIL import Image, ImageDraw

HEIGHT = 1080
WIDTH = 1920

WHITE = 255
BLACK = 0

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2

CENTER = (MID_X, MID_Y)


def generate_frame(radians: float, filename="out.png") -> None:
    im = Image.new("L", (WIDTH, HEIGHT), WHITE)
    # modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

    draw = ImageDraw.Draw(im)
    # draw.line((0, 0) + im.size, fill=128, width=100)
    # for rot_offset in [0, np.pi/2]:
    for rot_offset in np.linspace(0, np.pi, 6):
        r = WIDTH * 2
        nu_radians = radians + rot_offset

        x = np.cos(nu_radians) * r
        x += MID_X
        y = np.sin(nu_radians) * r
        y += MID_Y
        draw.line((WIDTH - x, HEIGHT - y, x, y), fill=BLACK, width=80)

    im.save(filename)


def main():
    frame_number = 0
    for rotation_radians in np.linspace(0, np.pi, 60):  # off by one? to loop perfectly we might need 59 frames
        filename = f"img/{frame_number:05}.png"
        generate_frame(rotation_radians, filename)
        print(f"{frame_number=} rendered")
        frame_number += 1

    subprocess.run(
        shlex.split(
            """ffmpeg -y -f image2 -r 60 -pattern_type glob -i 'img/*.png' -vcodec libx264 -crf 22 video.mp4"""
        )
    )
    subprocess.run(["vlc", "video.mp4"])


if __name__ == "__main__":
    main()

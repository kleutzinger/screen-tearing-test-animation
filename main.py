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

# Output resolution (4k)
OUTPUT_HEIGHT = 2160
OUTPUT_WIDTH = 3840

# Supersampled resolution (8K)
SUPER_HEIGHT = 4320
SUPER_WIDTH = 7680

WHITE = 255
BLACK = 0

# Center points for both resolutions
OUTPUT_MID_X = OUTPUT_WIDTH // 2
OUTPUT_MID_Y = OUTPUT_HEIGHT // 2
SUPER_MID_X = SUPER_WIDTH // 2
SUPER_MID_Y = SUPER_HEIGHT // 2

OUTPUT_CENTER = (OUTPUT_MID_X, OUTPUT_MID_Y)
SUPER_CENTER = (SUPER_MID_X, SUPER_MID_Y)


def generate_frame(radians: float, filename="out.png") -> None:
    # Create supersampled image
    super_im = Image.new("L", (SUPER_WIDTH, SUPER_HEIGHT), WHITE)
    draw = ImageDraw.Draw(super_im)

    for rot_offset in np.linspace(0, np.pi, 6):
        r = SUPER_WIDTH * 2
        nu_radians = radians + rot_offset

        x = np.cos(nu_radians) * r
        x += SUPER_MID_X
        y = np.sin(nu_radians) * r
        y += SUPER_MID_Y
        draw.line(
            (SUPER_WIDTH - x, SUPER_HEIGHT - y, x, y), fill=BLACK, width=320
        )  # Scaled width for 8K

    # Downsample to 1080p using Lanczos resampling
    im = super_im.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS)
    im.save(filename)


def main():
    frame_number = 0
    for rotation_radians in np.linspace(0, np.pi, 60)[:-1]:
        filename = f"img/{frame_number:05}.png"
        generate_frame(rotation_radians, filename)
        print(f"{frame_number=} rendered")
        frame_number += 1

    subprocess.run(
        shlex.split(
            """ffmpeg -y -stream_loop 29 -f image2 -r 60 -pattern_type glob -i 'img/*.png' -vcodec libx264 -crf 22 video.mp4"""
        )
    )
    subprocess.run(["vlc", "video.mp4"])


if __name__ == "__main__":
    main()

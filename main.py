from PIL import Image, ImageDraw

HEIGHT = 1080
WIDTH = 1920

WHITE = 255
BLACK = 0

MID_X = WIDTH//2
MID_Y = HEIGHT//2

def main():
    im = Image.new('L', (WIDTH,HEIGHT), WHITE)
    # modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

    draw = ImageDraw.Draw(im)
    #draw.line((0, 0) + im.size, fill=128, width=100)
    draw.line((MID_X, 0, MID_X, HEIGHT), fill=BLACK, width=50)
    draw.line((0, MID_Y, WIDTH, MID_Y), fill=BLACK, width=50)
    #draw.line((0, im.size[1], im.size[0], 0), fill=128)

    im.save('img.png')
    import subprocess
    subprocess.run(['feh', 'img.png'])


if __name__ == "__main__":
    main()





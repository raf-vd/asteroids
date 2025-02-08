from enum import Enum
from resources import *
import pygame

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT =   "Bold text"
    ITALIC_TEXT = "Italic text"
    CODE_TEXT =   "Code text"
    LINKS =       "Links"
    IMAGES =      "Images"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

def factorial(x):
    if x ==1:
        return 1
    return x * factorial(x-1)
     

def main():
    # i=5
    # print(f"factorial({i}) = {factorial(i)}")
    # pygame.font.init()

    # font32 = pygame.font.Font(None,32)
    print(font20_fsb.get_linesize())

    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # font = pygame.font.Font(None, 36)
    # text = u"\u2193 Use the arrow keys: ↑ ↓ ← →"
    # text_surface = font32_fs.render(text, True, (255, 255, 255))
    # screen.blit(text_surface, (50, 50))
    # pygame.display.flip()

    # # Keep the window open for a few seconds
    # pygame.time.wait(3000)
    # pygame.quit()


main()
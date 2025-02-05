from enum import Enum

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
    i=5
    print(f"factorial({i}) = {factorial(i)}")



main()
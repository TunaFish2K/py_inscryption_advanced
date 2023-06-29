import os
import json

from PIL import ImageFont

CURRENT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

class Font:
    def __init__(self,font_location:str) -> None:
        with open(os.path.realpath(font_location),"r") as f:
            font = json.load(f)

        self.location = os.path.dirname(
            os.path.realpath(font_location)
        )
        self.ids = font["ids"]
        self.file = os.path.join(self.location,font["file"])
        self.license = font.get("license") or None

        self.font = None
        
    def loadFont(self,size:int):
        return ImageFont.truetype(self.file,size)

    def setIds(self, fontGroup:dict) -> None:
        for i in self.ids:
            fontGroup[i] = self

def loadFonts(target:str="./builtin_resources/fonts/"):
    fontGroup = {}

    target = os.path.realpath(
        os.path.join(CURRENT_PATH,target)
        )
    fonts = os.listdir(target)

    for i in fonts:
        Font(os.path.join(
            target, i, "font.json"
        )).setIds(fontGroup=fontGroup)
    
    return fontGroup

class DrawableText:
    def __init__(self,text:str,size:int,font:ImageFont.FreeTypeFont) -> None:
        self.text = text
        self.size = size
        self.font = font
import os
import re
import math

from PIL import Image, ImageFont, ImageDraw

from .fonts import DrawableText

CURRENT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)
# misc

def keep_zh_cn(data:str):
    pattern = re.compile(r"[^\u4e00-\u9fa5！？]")
    return re.sub(pattern,"",data)

def keep_en_us(data:str):
    pattern = re.compile(r"[^a-zA-Z!?]")
    return re.sub(pattern,"",data)

def keep_number(data:str):
    pattern = re.compile(r"0-9")
    return re.sub(pattern,"",data)

def generate_proper_text_image(name:str,font_zh,font_en,default_size=20, max_width = 104):
    zh, en ,n = keep_zh_cn(name), keep_en_us(name), keep_number(name)
    if zh:
        font_size = default_size if len(zh) * default_size <= max_width else math.floor(max_width / len(zh)) 
        font = font_zh.loadFont(font_size)
        image = DrawableText(zh,font_size,font)
    elif en:
        font_size = default_size if len(en) * default_size <= max_width else math.floor(max_width / len(en))
        font = font_en.loadFont(font_size)
        image = DrawableText(en,font_size,font)
    elif n:
        font_size = default_size if len(n) * default_size <= max_width else math.floor(max_width / len(n))
        font = font_en.loadFont(font_size)
        image = DrawableText(n,font_size,font)
    else: raise ValueError("unsupported language, only zh-cn and en-us are supported")
    return image
    
# parts

def loadImage(type:str,name:str,target:str="./builtin_resources/textures/"):
    target = os.path.realpath(
        os.path.join(CURRENT_PATH,target)
    )
    name = name + ".png"
    image_path = os.path.join(target,type,name)
    return Image.open(image_path).convert("RGBA")

def getFront(name:str=""):
    return loadImage(type=os.path.join("cards","front"),name="card_front"+ ("_" if name else "") +name)

def getBack(name:str=""):
    return loadImage(type=os.path.join("cards","back"),name="card_back"+("_" if name else "") +name)

def getAbility(name:str):
    return loadImage(type="abilities",name="ability_"+name)

def getBeast(target:str):
    return Image.open(
        os.path.realpath(target)
    )

def getCost(type:str,count:int):
    """
    type: bone/blood
    count has a limit
    """
    if count <=0: return None
    if type == "blood" and count > 4: count = 4
    if type == "bone" and count > 10: count = 10
    name = str(count)+type
    if name: return loadImage(type="costs",name="cost_"+name)
    else: return None

# full card
class Card:
    width = 125
    height = 190
    def __init__(
        self,
        front:Image.Image,
        back:Image.Image,
        beast:Image.Image,
        name:str,
        damage:int, # -1 = no show
        health:int,  # -1 = no show
        abilities:list,
        cost:Image.Image, # can be None
        font_zh_cn:ImageFont.FreeTypeFont,
        font_en_us:ImageFont.FreeTypeFont
    ) -> None:
        self.front = front
        self.back = back
        self.name = name
        self.damage = damage
        self.health = health
        self.abilities = abilities
        self.cost = cost
        self.beast = beast
        self.font_zh_cn=font_zh_cn
        self.font_en_us=font_en_us

    def create(self):
        """
        what will we do:
        for front:
            render front texture
            render name on it
            render damage and health if necessary
            render abilities if necessary
            render cost if necessary
            combine them into a picture
        for back:
            just render the back
        """
        # we shouldn't change the front and the back , so we copy it
        front = self.front.copy()
        back = self.back.copy()
        # damage & health
        show_damage = (self.damage != -1)
        show_health = (self.health != -1)
        
        if show_damage: damage = generate_proper_text_image(str(self.damage), self.font_zh_cn, self.font_en_us,40,40)
        else: damage = None

        if show_health: health = generate_proper_text_image(str(self.health), self.font_zh_cn, self.font_en_us,40,40)
        else: health = None
        
        # name
        name = generate_proper_text_image(self.name, self.font_zh_cn, self.font_en_us)

        """
        for abilities:
            we have 2 abilities (not included sacrisfied abilities, i wont include this. but maybe stickers generator?) on one card at most
            the abilites tend to take as much space as they can
            so basically if there is 1 ability,
            the ability texture will fill the space between damage and health, and its size remains 49x49, it perfectly fits.
            but if there are 2, they will act like this:
            0b
            a0
            there size will be halved.
            what if we have more than 2 ability? well, we just slice it.
        """
        if len(self.abilities) > 2: abilities = self.abilities[:2]
        
        if len(self.abilities) == 2:
            ab_count = 2
            ab_0 = self.abilities[0].resize((round(self.abilities[0].size[0]*0.70), round(self.abilities[0].size[0]*0.70)))
            ab_1 = self.abilities[1].resize((round(self.abilities[1].size[1]*0.70), round(self.abilities[1].size[1]*0.70)))
        
        elif len(self.abilities) == 1:
            ab_count = 1
            ab_0 = self.abilities[0]
            ab_1 = None
        
        else:
            ab_count = 0
            ab_0 = None
            ab_1 = None
        
        # oh, seems that everything for the front is ready
        # lets generate the final image for the front
        # first we copy the texture directly to the image

        # beast
        front.paste(self.beast,(7,32),self.beast)

        # abilities
        if ab_count == 1:
            front.paste(ab_0,(36,135),ab_0)
        elif ab_count == 2:
            front.paste(ab_0,(36,152),ab_0)
            front.paste(ab_1,(61,134),ab_1)
        
        # cost
        if self.cost:
            x, y = 119 - self.cost.size[0], 18
            front.paste(self.cost,(x,y),self.cost)
        
        # then we need to turn front into a image draw thing to put text on it
        draw_front = ImageDraw.Draw(front)
        # name
        draw_front.text(xy=(62,16),text=name.text,fill=(0,0,0),font=name.font,anchor="mm")
        # damage & health
        if show_damage:
            draw_front.text(xy=(18,145),text=damage.text,fill=(0,0,0),font=damage.font,anchor="mm")
        if show_health:
            draw_front.text(xy=(105,165),text=health.text,fill=(0,0,0),font=health.font,anchor="mm")
        
        return front, back
        
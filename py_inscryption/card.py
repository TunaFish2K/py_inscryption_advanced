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

def coolAbility(ability:Image.Image,size=(40,40)):
    # ahh cool
    ability = ability.copy().resize(size)
    img_array = ability.load()
    width, height = ability.size
    for x in range(width):
        for y in range(height):
            color = img_array[x,y]
            if (
                color[0] == 0 and
                color[1] == 0 and
                color[2] == 0
            ):
                img_array[x,y] = (170,238,170,0)
    return ability
# parts

def loadImage(type:str,name:str,target:str="./builtin_resources/textures/"):
    target = os.path.realpath(
        os.path.join(CURRENT_PATH,target)
    )
    name = name + ".png"
    image_path = os.path.join(target,type,name)
    return Image.open(image_path).convert("RGBA")

# cool abilities xd
sacrisfied_abilitiy = loadImage(type=os.path.join("abilities","special"),name="card_added_ability").resize((60,60))

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

def getDecal(name:str):
    return loadImage(type=os.path.join("cards","decal"),name="decal_"+name)

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
        sacrisfied_abilities:list,
        cost:Image.Image, # can be None
        decals:list,
        font_zh_cn:ImageFont.FreeTypeFont,
        font_en_us:ImageFont.FreeTypeFont
    ) -> None:
        self.front = front
        self.back = back
        self.name = name
        self.damage = damage
        self.health = health
        self.abilities = abilities
        self.sacrisfied_abilities = sacrisfied_abilities
        self.cost = cost
        self.beast = beast
        self.decals = decals
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
        
        if show_damage: damage = generate_proper_text_image(str(self.damage), self.font_zh_cn, self.font_en_us,40,60)
        else: damage = None

        if show_health: health = generate_proper_text_image(str(self.health), self.font_zh_cn, self.font_en_us,40,60)
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
            front.paste(ab_0,(40,133),ab_0)
        elif ab_count == 2:
            front.paste(ab_0,(32,150),ab_0)
            front.paste(ab_1,(57,132),ab_1)

        if len(self.sacrisfied_abilities):
            # cool abilities! xd
            if len(self.abilities) <= 0:
                front.paste(sacrisfied_abilitiy,(35,125),sacrisfied_abilitiy)
                front.paste(coolAbility(self.sacrisfied_abilities[0]),(45,135),self.sacrisfied_abilities[0].resize((40,40)))
                self.sacrisfied_abilities.pop(0)
            if len(self.sacrisfied_abilities) > 0:
                # 1 => 14 38
                front.paste(sacrisfied_abilitiy.resize((50,50)),(5,31),sacrisfied_abilitiy.resize((50,50)))
                front.paste(coolAbility(self.sacrisfied_abilities[0],(30,30)),(15,41),self.sacrisfied_abilities[0].resize((30,30)))
            if len(self.sacrisfied_abilities) >= 2:
                # 2 => 99 38
                front.paste(sacrisfied_abilitiy.resize((50,50)),(5,76),sacrisfied_abilitiy.resize((50,50)))
                front.paste(coolAbility(self.sacrisfied_abilities[1],(30,30)),(15,86),self.sacrisfied_abilities[1].resize((30,30)))
        
        # cost
        if self.cost:
            cost = self.cost.resize((math.floor(self.cost.size[0]*0.75),math.floor(self.cost.size[1]*0.75)))
            x, y = 119 - cost.size[0], 23
            front.paste(cost,(x,y),cost)

        # then decals
        for i in self.decals:
            front.paste(i,(0,0),i)
        
        # then we need to turn front into a image draw thing to put text on it
        draw_front = ImageDraw.Draw(front)
        # name
        draw_front.text(xy=(62,16),text=name.text,fill=(0,0,0),font=name.font,anchor="mm")
        # damage & health
        if show_damage:
            draw_front.text(xy=(19,150),text=damage.text,fill=(0,0,0),font=damage.font,anchor="mm")
        if show_health:
            draw_front.text(xy=(106,165),text=health.text,fill=(0,0,0),font=health.font,anchor="mm")
        
        return front, back
        
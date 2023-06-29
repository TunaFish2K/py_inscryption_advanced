import os

import json

from py_inscryption.card import *
from py_inscryption.fonts import *

fonts = loadFonts()

class StaticCard:
    def __init__(
        self,front:str,back:str,beast:str,
        name:str,
        damage:int, # -1 = no show
        health:int,  # -1 = no show
        abilities:list, # of string
        cost_type:str, # blood or bone
        cost:int
        ) -> None:
        self.front = front
        self.back = back
        self.beast = beast
        self.name = name
        self.damage = damage
        self.health = health
        self.abilities = abilities
        self.cost_type = cost_type
        self.cost = cost
    
    def serialize(self):
        return {
            "front": self.front,
            "back": self.back,
            "beast": self.beast,
            "name": self.name,
            "damage": self.damage,
            "health": self.health,
            "abilities": self.abilities,
            "cost_type": self.cost_type,
            "cost": self.cost
        }
    
    @classmethod
    def deSerialize(cls,data):
        return cls(
            data["front"],
            data["back"],
            data["beast"],
            data["name"],
            data["damage"],
            data["health"],
            data["abilities"],
            data["cost_type"],
            data["cost"]
        )

    def toCard(self,card_location:str) -> Card:
        ab = []
        for i in self.abilities:
            ab.append(getAbility(i))
        return Card(
            getFront(self.front),getBack(self.back),getBeast(os.path.realpath(
                os.path.join(card_location,"textures",self.beast)
            )),
            self.name,
            self.damage, self.health,
            ab,
            getCost(self.cost_type,self.cost),
            fonts["chapter1_zh_cn"], fonts["chapter1"]
        )

class CardManager:
    def __init__(self,target:str) -> None:
        self.target = os.path.realpath(target)

    def get(self,name:str) -> StaticCard:
        with open(os.path.join(self.target,name+".json"),"r",encoding="utf-8") as f:
            return StaticCard.deSerialize(json.load(f))
    
    def set(self,name:str,data:StaticCard) -> None:
        with open(os.path.join(self.target,name+".json"),"w",encoding="utf-8") as f:
            f.write(json.dumps(data.serialize(),ensure_ascii=False,indent=4))
    
    def list_cards(self) -> list:
        l = []
        for f in os.listdir(self.target):
            if not f.endswith('.json'): continue
            l.append(os.path.splitext(f)[0])
        return l

class Deck:
    def __init__(self,content:list) -> None:
        self.content = content
    def getCards(self):
        for i in self.content:
            for j in range(i[1]):
                yield i[0]

class DeckManager:
    def __init__(self,target:str) -> None:
        self.target = target
    def get(self,name:str) -> Deck:
        with open(os.path.join(self.target,name+".json"),"r",encoding="utf-8") as f:
            return Deck(json.load(f)["deck"])
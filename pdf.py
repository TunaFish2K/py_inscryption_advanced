from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from pprint import pprint as print

CAN_WIDTH = A4[0]
CAN_HEIGHT = A4[1]
DRAWABLE_WIDTH = CAN_WIDTH - 20
DRAWABLE_HEIGHT = CAN_HEIGHT - 20
CARD_WIDTH = DRAWABLE_WIDTH / 3
CARD_HEIGHT = DRAWABLE_HEIGHT / 3

def n2t(l:list):
    return [
        l[0:3],
        l[3:6],
        l[6:]
    ]

def reverse_cards(cards:list) -> list:
    return [cards[2],cards[1],cards[0]]

def card_page(can,cards:list) -> None:
    """
    target is where ur pdf will come
    cards is a [
        [],[],[]
    ]
    """
    # 3x3 card realpath location
    for y, card_line in enumerate(cards):
        for x, card in enumerate(card_line):
            if not card: continue
            pos_x = (CAN_WIDTH - DRAWABLE_WIDTH) /2 + CARD_WIDTH * x
            pos_y = (CAN_HEIGHT - DRAWABLE_HEIGHT) /2 + CARD_HEIGHT * y
            can.drawImage(card,pos_x,pos_y,CARD_WIDTH,CARD_HEIGHT)
    can.showPage()

    
    
            
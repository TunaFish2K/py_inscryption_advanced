from py_inscryption import card

import card_manager,pdf

from reportlab.pdfgen import canvas
import os

"""
what i want:
- fetch the card data(chapter 1) from fandom wiki
- show a gui that allow the user to select the amount of every kind of card
- put every card in pdf (front and back, on the opposite sides)
 then i can print the pdf and cut down the card
"""
import os

def mkdir(path:str):
    path = os.path.realpath(path=path)
    if not os.path.exists(path=path):
        os.makedirs(path)

def init():
    """
    yeah, without this u cant run the program
    """
    mkdir("./cards")
    mkdir("./cards/textures")
    mkdir("./decks")
    mkdir("./output")
    mkdir("./generated_cards")
    mkdir("./generated_cards/back")
    

def deck_pdf(name:str):
    c = card_manager.CardManager("./cards/")
    d = card_manager.DeckManager("./decks/")
    can = canvas.Canvas(os.path.realpath(
        os.path.join("./output/",name+".pdf")
    ))
    page = []
    back_page = []
    beast_name = ""
    beast = None
    counter = 0
    for i in d.get(name).getCards():
        counter += 1
        # cache

        if beast_name != i:
            beast = c.get(i).toCard("./cards/").create()
            beast_name = i

            beast[0].save(
                os.path.realpath(
                    os.path.join("./generated_cards/",beast_name+".png")
                )
            )
            beast[1].save(
                os.path.realpath(
                    os.path.join("./generated_cards/back/",beast_name+".png")
                )
            )

        page.append(
            os.path.realpath(
                os.path.join("./generated_cards/",beast_name+".png")
                )
        )
        back_page.append(
            os.path.realpath(
                os.path.join("./generated_cards/back/",beast_name+".png")
                )
        )
        if counter % 9 == 0 and counter != 0:
            pdf.card_page(can,pdf.n2t(page))
            pdf.card_page(can,pdf.n2t(back_page))
            page.clear()
            back_page.clear()

       
    if counter % 9 > 0:
        pdf.card_page(can,pdf.n2t(page))
        pdf.card_page(can,pdf.reverse_cards(pdf.n2t(back_page)))
    can.save()

if __name__ == "__main__":
    init()
    deck_pdf(input("Deck Name:"))
            

import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def test():
    import card_manager
    man = card_manager.CardManager("./test_cards/")

    man.set("stoat",
        card_manager.StaticCard("","","stoat.png","白鼬",1,2,[],"blood",1)
    )
    man.set("stoat_advanced",
        card_manager.StaticCard("","","stoat.png","白鼬",2,3,["allstrike"],"blood",2)
    )
    stoat, _ = man.get("stoat").toCard(man.target).create()
    stoat.save(os.path.realpath(
        os.path.join("./generated_cards/","stoat.png")
    ))
    _.save(os.path.realpath(
        os.path.join("./generated_cards/back/","stoat.png")
    ))

    stoat_advanced, _ = man.get("stoat_advanced").toCard(man.target).create()
    stoat_advanced.save(os.path.realpath(
        os.path.join("./generated_cards/","stoat_advanced.png")
    ))
    _.save(os.path.realpath(
        os.path.join("./generated_cards/back/","stoat_advanced.png")
    ))

    import pdf
    c = canvas.Canvas(os.path.realpath("./test_pdf/test.pdf"),pagesize=A4)
    pdf.card_page(c,[
        [os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat.png")],
        [os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat.png")],
        [os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat.png"),
        os.path.realpath("./generated_cards/stoat_advanced.png")]
    ])

    pdf.card_page(c,[
        [os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat.png")],
        [os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat.png")],
        [os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat.png"),
        os.path.realpath("./generated_cards/back/stoat_advanced.png")]
    ])

    c.save()

if __name__ == "__main__":
    test()
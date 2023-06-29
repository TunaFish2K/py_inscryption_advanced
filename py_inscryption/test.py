"""
test the functions of the modules to make sure they work in different situations
"""
import os

CURRENT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

def test():
    from .fonts import loadFonts
    f = loadFonts()

    from .card import generate_proper_text_image, Card, getFront, getBack, getBeast, getAbility, getCost
    a=generate_proper_text_image("哈喽！",f["chapter1"],f["chapter1_zh_cn"])
    print(a.text,a.size,a.font)

    b=generate_proper_text_image("weee!",f["chapter1"],f["chapter1_zh_cn"])
    print(b.text,b.size,b.font)

    # lets try if it works when big text appears
    c=generate_proper_text_image("炙热地狱三头犬",f["chapter1"],f["chapter1_zh_cn"])
    print(c.text,c.size,c.font)

    # then we try different size settings
    d=generate_proper_text_image("114514",f["chapter1"],f["chapter1_zh_cn"],25,30)
    print(d.text,d.size,d.font)
    
    # finally we test to generate a real card
    front, back = Card(
        getFront(), getBack(),
        getBeast(os.path.join(CURRENT_PATH,"./test/icy_trap.png")),
        "冰霜陷阱",
        1,5,
        [getAbility("steeltrap"),getAbility("sniper")],
        getCost("bone",10),
        font_zh_cn=f["chapter1_zh_cn"],
        font_en_us=f["chapter1"]
    ).create()
    front.show()
    back.show()

if __name__ == "__main__":
    test()
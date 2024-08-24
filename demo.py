from pathlib import Path

from denpy import ImageResource, VisualNovel, VnNode


def main():
    generate_english_demo()
    generate_spanish_demo()


def generate_english_demo():
    vn = VisualNovel()

    vn.register_images(
        ImageResource("Background1", "assets/bg.jpg", scale=1.5),
        ImageResource("Background2", "assets/bg2.jpg"),
        ImageResource("CharaAnnoyed", "assets/annoyed.png", 250, -26, scale=0.7),
        ImageResource("CharaDelighted", "assets/delighted.png", 250, -26, scale=0.7),
        ImageResource("CharaNormal", "assets/normal.png", 250, -26, scale=0.7),
        ImageResource("CharaSmile", "assets/smile.png", 250, -26, scale=0.7),
        ImageResource("CharaSmile2", "assets/smile2.png", 250, -26, scale=0.7),
    )

    vn.register_nodes(
        VnNode(
            background="Background1",
            speaker=None,
            text="...",
        ),
        VnNode(
            character="CharaNormal",
            speaker="???",
            text="Hmm?",
        ),
        VnNode(
            character="CharaDelighted",
            text="Oh, you're finally awake!",
        ),
        VnNode(
            character="CharaSmile",
            speaker=None,
            text="Huh?",
        ),
        VnNode(
            text="Who are you?",
        ),
        VnNode(
            text="W-where am I!?",
        ),
        VnNode(
            character="CharaDelighted",
            speaker="PDF-chan",
            text="Welcome to the DenPy demo!",
        ),
        VnNode(
            speaker=None,
            text="Demo? What are you talking about?",
        ),
        VnNode(
            speaker="PDF-chan",
            text="With this library, you can create visual novels inside .pdf files!",
        ),
        VnNode(
            speaker=None,
            text="I don't understand what's going on...",
        ),
        VnNode(
            character="CharaSmile2",
            speaker="PDF-chan",
            text="Don't worry, I'll show you!",
        ),
        VnNode(
            background="Background2",
            speaker=None,
            text="...",
        ),
        VnNode(
            text="Aaaah!!",
        ),
        VnNode(
            character="CharaAnnoyed",
            speaker="PDF-chan",
            text="As you can see, we don't have smooth transitions yet...",
        ),
        VnNode(
            speaker=None,
            text="STOP MOVING ME AROUND!",
        ),
        VnNode(
            character="CharaSmile",
            speaker="PDF-chan",
            text="...or sounds... but we're working on that.",
        ),
        VnNode(
            speaker=None,
            text="Can I go now?",
        ),
        VnNode(
            character="CharaSmile2",
            speaker="PDF-chan",
            text="Sure, see you soon!",
        ),
        VnNode(
            background="Background1",
            character=None,
            speaker=None,
            text="Great... now, how do I get out of here...?",
        ),
    )

    vn.write_to(Path("out/demo_en.pdf"))


def generate_spanish_demo():
    vn = VisualNovel()

    vn.register_images(
        ImageResource("Background1", "assets/bg.jpg", scale=1.5),
        ImageResource("Background2", "assets/bg2.jpg"),
        ImageResource("CharaAnnoyed", "assets/annoyed.png", 250, -26, scale=0.7),
        ImageResource("CharaDelighted", "assets/delighted.png", 250, -26, scale=0.7),
        ImageResource("CharaNormal", "assets/normal.png", 250, -26, scale=0.7),
        ImageResource("CharaSmile", "assets/smile.png", 250, -26, scale=0.7),
        ImageResource("CharaSmile2", "assets/smile2.png", 250, -26, scale=0.7),
    )

    vn.register_nodes(
        VnNode(
            background="Background1",
            speaker=None,
            text="...",
        ),
        VnNode(
            character="CharaNormal",
            speaker="???",
            text="¿Hmm?",
        ),
        VnNode(
            character="CharaDelighted",
            text="¡Oh, has despertado!",
        ),
        VnNode(
            character="CharaSmile",
            speaker=None,
            text="¿Eh?",
        ),
        VnNode(
            text="¿Quién eres?",
        ),
        VnNode(
            text="¿¡D-dónde estoy!?",
        ),
        VnNode(
            character="CharaDelighted",
            speaker="PDF-chan",
            text="¡Te doy la bienvenida a la demo de DenPy!",
        ),
        VnNode(
            speaker=None,
            text="¿Demo? ¿Qué dices?",
        ),
        VnNode(
            speaker="PDF-chan",
            text="¡Con esta librería, podrás crear novelas visuales dentro de archivos .pdf!",
        ),
        VnNode(
            speaker=None,
            text="No entiendo nada...",
        ),
        VnNode(
            character="CharaSmile2",
            speaker="PDF-chan",
            text="No te preocupes, ¡te lo enseñaré!",
        ),
        VnNode(
            background="Background2",
            speaker=None,
            text="...",
        ),
        VnNode(
            text="¡¡Aaaah!!",
        ),
        VnNode(
            character="CharaAnnoyed",
            speaker="PDF-chan",
            text="Como podrás notar, aún no tenemos transiciones suaves...",
        ),
        VnNode(
            speaker=None,
            text="¡DEJA DE MOVERME!",
        ),
        VnNode(
            character="CharaSmile",
            speaker="PDF-chan",
            text="...ni sonidos... pero estamos trabajando en ello.",
        ),
        VnNode(
            speaker=None,
            text="¿Puedo irme ya?",
        ),
        VnNode(
            character="CharaSmile2",
            speaker="PDF-chan",
            text="¡Seguro, hasta pronto!",
        ),
        VnNode(
            background="Background1",
            character=None,
            speaker=None,
            text="Genial... ahora, ¿cómo salgo de aquí...?",
        ),
    )

    vn.write_to(Path("out/demo_es.pdf"))


if __name__ == "__main__":
    main()

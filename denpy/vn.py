from pathlib import Path

from denpy.image import ImageResource
from denpy.mapper import map_object
from denpy.models import IndirectRef, Name, Stream, VnNode

PAGE_SCALE = 0.7
PAGE_WIDTH = 1280 * PAGE_SCALE
PAGE_HEIGHT = 720 * PAGE_SCALE

FLAG_READONLY = 1
FLAG_MULTILINE = 1 << 12


class VisualNovel:
    def __init__(self):
        self.__images: list[ImageResource] = []
        self.__nodes: list[VnNode] = []

    def register_images(self, *images: ImageResource):
        self.__images.extend(images)

    def register_nodes(self, *nodes: VnNode):
        self.__nodes.extend(nodes)

    def write_to(self, path: Path):
        objects = self.__get_pdf_base()
        img_index = len(objects) + 1  # 6
        for image in self.__images:
            # add img xobjects to object list
            streams = image.to_streams(img_index)
            objects.extend(streams)

            # register page resources
            objects[3]["Resources"]["XObject"][image.name] = IndirectRef(img_index)

            # register annotation
            objects[3]["Annots"].append(
                {
                    "Type": Name("Annot"),
                    "Subtype": Name("Widget"),
                    "T": f"_{image.name}",
                    "V": b"",
                    "FT": Name("Tx"),
                    "Ff": FLAG_READONLY,
                    "AP": {
                        "N": IndirectRef(img_index + len(streams) - 1),
                    },
                }
            )
            img_index += len(streams)

        # add UI
        objects[3]["Annots"].extend(self.__get_ui_annotations())

        # add on-start js
        objects[3]["AA"]["O"]["JS"] = self.__get_js_engine()

        # add on-click js
        textbox_index = len(objects[3]["Annots"]) - 2
        objects[3]["Annots"][textbox_index]["AA"]["Fo"]["JS"] = "onTextboxClick()"

        trailer = {
            "Size": len(objects) + 1,
            "Root": IndirectRef(1),
        }

        object_ptrs = []

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            f.write(b"%PDF-1.7\n\n")

            for i, obj in enumerate(objects):
                f.write(f"{i + 1} 0 obj\n".encode())
                object_ptrs.append(f.tell())
                f.write(map_object(obj))
                f.write(b"endobj\n\n")

            # write xref
            xref_ptr = f.tell()
            f.write(b"xref\n")

            ## subsection 0 of n+1 entries
            f.write(f"0 {len(object_ptrs) + 1}\n".encode())

            ## first free entry (pointing to itself)
            f.write(f"{0:010d} 35565 f\n".encode())
            for ptr in object_ptrs:
                f.write(f"{ptr:010d} {0:05d} n\n".encode())

            # write trailer
            f.write(b"trailer\n")
            f.write(map_object(trailer))

            f.write(b"startxref\n")
            f.write(f"{xref_ptr}\n".encode())
            f.write(b"%%EOF")

    def __get_js_engine(self) -> str:
        with (Path(__file__).parent / "engine.js").open("r") as f:
            js_images = ",".join(map(lambda i: f'"{i.name}"', self.__images))
            js_nodes = ",".join(map(lambda n: n.to_json(), self.__nodes))
            return f"""
            global.vnimages = [{js_images}];
            global.vnnodes = [{js_nodes}];
            {f.read()}
            """

    @staticmethod
    def __get_pdf_base() -> list:
        return [
            {
                "Type": Name("Catalog"),
                "Pages": IndirectRef(2),
            },
            {
                "Type": Name("Pages"),
                "Kids": [IndirectRef(4)],
                "Count": 1,
            },
            {
                "Type": Name("Font"),
                "Subtype": Name("Type1"),
                "BaseFont": Name("Helvetica"),
            },
            {
                "MediaBox": [0, 0, PAGE_WIDTH, PAGE_HEIGHT],
                "Resources": {
                    "Font": {"FontHelvetica": IndirectRef(3)},
                    "ProcSet": [
                        Name("PDF"),
                        Name("Text"),
                        Name("ImageB"),  # grayscale
                        Name("ImageC"),  # color
                        Name("ImageI"),  # indexed
                    ],
                    "XObject": {},
                },
                "AA": {"O": {"S": Name("JavaScript"), "JS": ""}},
                "Annots": [
                    {
                        "Type": Name("Annot"),
                        "Subtype": Name("Widget"),
                        "T": "_focus_restart",
                        "V": "",
                        "FT": Name("Tx"),
                        "Ff": FLAG_READONLY,
                        "Rect": [0, 0, PAGE_WIDTH, PAGE_HEIGHT],
                    },
                ],
            },
            Stream({}, b""),
        ]

    @staticmethod
    def __get_ui_annotations() -> list[dict]:
        return [
            {
                "Type": Name("Annot"),
                "Subtype": Name("Widget"),
                "T": "_textbox",
                "V": b"",
                "FT": Name("Tx"),
                "Ff": FLAG_MULTILINE,
                "MK": {"BG": [0.1, 0.1, 0.1]},
                "DA": "/FontHelvetica 24 Tf 1 1 1 rg",
                "Rect": [20, 10, PAGE_WIDTH - 20, PAGE_HEIGHT / 4],
                "AA": {
                    "Fo": {
                        "S": Name("JavaScript"),
                        "JS": "",
                    },
                },
            },
            {
                "Type": Name("Annot"),
                "Subtype": Name("Widget"),
                "T": "_speakerbox",
                "V": b"",
                "FT": Name("Tx"),
                "Ff": FLAG_READONLY,
                "MK": {"BG": [0.1, 0.1, 0.1]},
                "DA": "/FontHelvetica 24 Tf 1 1 1 rg",
                "Rect": [20, 5 + PAGE_HEIGHT / 4, 200, 5 + PAGE_HEIGHT / 4 + 30],
            },
        ]

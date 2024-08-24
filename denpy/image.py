import zlib
from dataclasses import dataclass, field

from PIL import Image

from denpy.models import IndirectRef, Name, Stream


@dataclass
class ImageResource:
    name: str
    path: str

    x: int = 0
    y: int = 0
    scale: float = 1

    width: int = 0
    height: int = 0
    rgb: bytearray = field(default_factory=bytearray)
    alpha: bytearray = field(default_factory=bytearray)

    def __post_init__(self):
        with Image.open(self.path) as img:
            assert img.mode in ("RGB", "RGBA")
            has_alpha = "A" in img.mode

            self.width = img.size[0]
            self.height = img.size[1]
            self.rgb = bytearray(self.width * self.height * 3)
            if has_alpha:
                self.alpha = bytearray(img.size[0] * img.size[1])

            i = 0
            for z in range(self.height):
                for x in range(self.width):
                    pixel: tuple = img.getpixel((x, z))  # type: ignore

                    self.rgb[i] = pixel[0]
                    self.rgb[i + 1] = pixel[1]
                    self.rgb[i + 2] = pixel[2]

                    if has_alpha:
                        self.alpha[int(i / 3)] = pixel[3]

                    i += 3

            self.rgb = bytearray(zlib.compress(self.rgb))
            if self.alpha:
                self.alpha = bytearray(zlib.compress(self.alpha))

    def to_streams(self, ref_index: int) -> list[Stream]:
        out = [
            Stream(
                {
                    "Type": Name("XObject"),
                    "Subtype": Name("Image"),
                    "Width": self.width,
                    "Height": self.height,
                    "ColorSpace": Name("DeviceRGB"),
                    "BitsPerComponent": 8,
                    "Filter": Name("FlateDecode"),
                    "DecodeParams": {
                        "Predictor": 15,
                        "Colors": 3,
                        "BitsPerComponent": 8,
                        "Columns": self.width,
                    },
                },
                self.rgb,
            ),
        ]
        if self.alpha:
            out[0].metadata["SMask"] = IndirectRef(ref_index + 1)
            out.append(
                Stream(
                    {
                        "Type": Name("XObject"),
                        "Subtype": Name("Image"),
                        "Width": self.width,
                        "Height": self.height,
                        "ColorSpace": Name("DeviceGray"),
                        "BitsPerComponent": 8,
                        "Filter": Name("FlateDecode"),
                        "DecodeParams": {
                            "Predictor": 15,
                            "Colors": 1,
                            "BitsPerComponent": 8,
                            "Columns": self.width,
                        },
                    },
                    self.alpha,
                ),
            )

        out.append(
            Stream(
                {},
                b"q %.2f 0 0 %.2f %.2f %.2f cm /%s Do Q"
                % (
                    self.width * self.scale,
                    self.height * self.scale,
                    self.x,
                    self.y,
                    self.name.encode(),
                ),
            ),
        )
        return out

import string

from denpy.models import IndirectRef, Name, Stream

__STD_DATATYPES = int | float | str | bytes | list | dict | None
__PDF_DATATYPES = Name | IndirectRef | Stream


def map_object(value: __STD_DATATYPES | __PDF_DATATYPES) -> bytes:
    match value:
        case Stream():
            length_dict = map_object({**value.metadata, "Length": len(value.data)})
            if value.data:
                return length_dict + b"stream\n" + value.data + b"\nendstream\n"
            return length_dict + b"stream\nendstream\n"

        case IndirectRef():
            return f"{value.object_n} {value.generation_n} R\n".encode()

        case Name():
            return f"/{value}\n".encode()

        case int() | float():
            return f"{value}\n".encode()

        case str():
            return b"(" + __escape_string(value).encode("latin1") + b")\n"

        case bytes():
            return f"<{''.join(f'{b:02X}' for b in value)}>\n".encode()

        case list():
            return (
                b"[\n" + b"".join(b"\t" + map_object(item) for item in value) + b"]\n"
            )

        case dict():
            return (
                b"<<\n"
                + b"".join(
                    b"\t/" + k.encode() + b" " + map_object(v) for k, v in value.items()
                )
                + b">>\n"
            )

        case None:
            return b"null\n"

        case _:
            print(f"ERROR: Invalid object type: {type(value)} - {repr(value)}")
            return f"{value}\n".encode()


def __escape_string(v: str) -> str:
    trans = v.translate(
        {
            0x0A: r"\n",
            0x0D: r"\r",
            0x09: r"\t",
            0x08: r"\b",
            0x28: r"\(",
            0x29: r"\)",
            0x5C: r"\\",
        }
    )
    result = []
    for c in trans:
        if c in string.printable:
            result.append(c)
        else:
            result.append(f"\\{ord(c):03o}")
    return "".join(result)


def __wrap_stream(data: bytes, metadata: dict | None = None) -> bytes:
    length_dict = map_object({**(metadata or {}), "Length": len(data)})
    if data:
        return length_dict + b"stream\n" + data + b"\nendstream\n"
    return length_dict + b"stream\nendstream\n"

import json
from dataclasses import asdict, dataclass
from typing import Literal

# PDF models


class Name(str):
    pass


@dataclass
class Stream:
    metadata: dict
    data: bytes


@dataclass
class IndirectRef:
    object_n: int
    generation_n: int = 0


# VN models


@dataclass
class VnNode:
    background: str | Literal[0] = 0
    character: str | None | Literal[0] = 0
    speaker: str | None | Literal[0] = 0
    text: str = ""

    def to_json(self) -> str:
        return json.dumps(
            {k: v for k, v in asdict(self).items() if v != 0}, ensure_ascii=False
        )

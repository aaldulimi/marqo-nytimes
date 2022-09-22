import dataclasses


@dataclasses.dataclass
class Document:
    id: int 
    title: str
    author: str
    body: str
    url: str

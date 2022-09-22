import dataclasses


@dataclasses.dataclass
class Document:
    _id: str 
    title: str
    author: str
    body: str
    url: str

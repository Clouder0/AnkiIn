from .Cloze import get as cget
from ..config import notetype_settings as settings


notetype_name = "ListCloze"
if notetype_name not in settings:
    settings[notetype_name] = {}
priority = settings[notetype_name].get("priority", 15)


def check(lines: list) -> bool:
    if len(lines) < 3:
        return False
    return "|" in lines[0] and "|" in lines[1] and "-" in lines[1] and "|" in lines[2]


def get(text: str, deck: str = "Export", tags: list = []):
    return cget(text=text, deck=deck, tags=tags)

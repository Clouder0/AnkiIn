from .Cloze import get as cget
from ..config import notetype_settings as settings


notetype_name = "ListCloze"
if notetype_name not in settings:
    settings[notetype_name] = {}
priority = settings[notetype_name].get("priority", 10)


def check(lines: list) -> bool:
    return lines[0].startswith("- ")


def get(text: str, tags: list = []):
    return cget(text, tags)

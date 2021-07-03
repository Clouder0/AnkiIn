from .Cloze import get as cget


priority = 10


def check(lines: list) -> bool:
    return lines[0].startswith("- ")


def get(text: str, tags: list = []):
    return cget(text, tags)

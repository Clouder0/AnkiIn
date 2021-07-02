from . import config, note, model
from . import notetype_loader

notetype_loader.load_notetypes()
__all__ = ["config", "note", "model"]

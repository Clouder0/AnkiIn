import sys
import os
import pkgutil
import importlib
from notetypes import Choices, Cloze, ListCloze, QA, TableCloze
from .log import importer_logger as log

discovered_notetypes = []


def get_notetypes():
    global discovered_notetypes
    if discovered_notetypes is not None:
        return discovered_notetypes
    discovered_notetypes = [Choices, Cloze, ListCloze, QA, TableCloze]
    sys.path.append("." + os.sep + "notetypes" + os.sep)
    sys.path.append("." + os.sep + "importer" + os.sep + "notetypes" + os.sep)
    discovered_notetypes.extend(
        importlib.import_module(name) for finder, name, ispkg in pkgutil.iter_modules() if name.startswith("notetype_"))
    discovered_notetypes.sort(key=lambda x: x.priority, reverse=True)
    log.info("Loaded notetypes:\n%s", discovered_notetypes)
    return discovered_notetypes

import sys
import os
import pkgutil
import importlib
from .notetypes import Choices, Cloze, ListCloze, QA, TableCloze, MQA
from .log import main_logger as log
from .config import config_updater

discovered_notetypes = [Choices, Cloze, ListCloze, QA, TableCloze, MQA]
sys.path.append("." + os.sep + "notetypes" + os.sep)
sys.path.append("." + os.sep + "importer" + os.sep + "notetypes" + os.sep)
discovered_notetypes.extend(
    importlib.import_module(name) for finder, name, ispkg in pkgutil.iter_modules() if name.startswith("notetype_"))
log.info("Loaded notetypes:\n%s", discovered_notetypes.__str__())


def sort_notetypes():
    discovered_notetypes.sort(key=lambda x: x.priority, reverse=True)
    log.debug("Sorted notetypes:\n%s", discovered_notetypes.__str__())


config_updater.append((sort_notetypes, 20))

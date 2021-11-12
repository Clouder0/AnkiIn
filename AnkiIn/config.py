import collections
from typing import Dict
from . import log
from .log import main_logger as logger
import toml

dict = {
    "deck_name": "Export",
    "skip": False,
    "mathjax": True,
    "tags": [],
    "log_config": {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "main": {
                "level": "DEBUG",
                "handlers": ["console"]
            },
            "notetype": {
                "level": "DEBUG",
                "handlers": ["console"]
            },
            "parser": {
                "level": "DEBUG",
                "handlers": ["console"]
            },
            "helper": {
                "level": "DEBUG",
                "handlers": ["console"]
            },
        },
        "handlers": {
            "console": {
                "level": "WARNING",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
        },
        "formatters": {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
    },
    "notetype": {
        "Cloze": {
            "clozePrefix": r"\*\*",
            "clozeSuffix": r"\*\*",
            "clozeNumberPrefix": r"\[",
            "clozeNumberSuffix": r"\]",
        },
        "MQA": {
            "prefix": r"!",
        },
    }
}


def load_logging_config():
    log.logging.config.dictConfig(dict["log_config"])


config_updater = [(load_logging_config, 0), ]


def update_config():
    config_updater.sort(key=lambda x: x[1])
    for x in config_updater:
        x[0]()


def merge_dictionary(d1: Dict, d2: Dict) -> Dict:
    backup = {}
    for key, val in d2.items():
        if key in d1 and isinstance(d1[key], collections.Mapping) \
                and isinstance(val, collections.Mapping):
            backup[key] = merge_dictionary(d1[key], val)
        else:
            backup[key] = d1[key] if key in d1 else None
            d1[key] = val
    return backup


def parse_config(text: str) -> Dict:
    logger.info("Executing config:\n%s", text)
    ret = execute_config(toml.loads(text))
    logger.debug("Config updated:\n%s", toml.dumps(dict))
    return ret


def execute_config(conf: Dict) -> Dict:
    ret = merge_dictionary(dict, conf)
    update_config()
    return ret


update_config()  # load the default config
logger.debug("Config loaded:\n%s", toml.dumps(dict))

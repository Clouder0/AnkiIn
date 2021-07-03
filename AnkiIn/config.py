from . import config, log
from .log import importer_logger as logger
import regex


deck_name = "Export"
skip = False
mathjax = True
tags = []
file_list = []
output = False
output_path = ""
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "": {
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
}
notetype_settings = {}


def complete_config():
    log.logging.config.dictConfig(log_config)


def parse_config(text: str):
    logger.debug("Parsing config:\n%s", text)
    matches = regex.finditer(r"^(.+)=(.+)$", text, regex.M)
    if matches is None:
        return
    for x in matches:
        key = x.group(1).strip()
        value = x.group(2).strip()
        value = str(value)
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.startswith("[") and value.endswith("]"):
            value = value[1:-1]
            if "," in value:
                value = value.split(",")
            elif "，" in value:
                value = value.split("，")
            else:
                value = [value]
        yield [key, value]


def execute_config(config_list: list, keep_backup=True):
    config_history = []
    for x in config_list:
        if not hasattr(config, x[0]):
            logger.warning("Invalid config:\n%s", x.__str__())
            continue
        # backup the old value
        if keep_backup:
            config_history.append([x[0], getattr(config, x[0])])
        logger.info("Set Config %s to %s", x[0], x[1])
        setattr(config, x[0], x[1])
    return config_history

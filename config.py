from . import log


deck_name = "Export"
tags = []
file_list = []
output = False  # output to file
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


def complete_config():
    log.logging.config.dictConfig(log_config)

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
            "level": "INFO",
            "handlers": ["console"]
        },
        "notetype": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "parser": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "helper": {
            "level": "INFO",
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

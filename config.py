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
            "level": "INFO"
        },
        "notetype": {
            "level": "INFO"
        },
        "parser": {
            "level": "INFO"
        },
        "helper": {
            "level": "INFO"
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "formatter": "standard",
            "class": "logging.StreamHanlder",
            "stream": "ext://sys.stdout"
        },
    },
    "formatters": {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
}

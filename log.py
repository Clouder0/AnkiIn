import logging
import logging.config
from .config import log_config

logging.config.dictConfig(log_config)

notetype_logger = logging.getLogger("notetype")
importer_logger = logging.getLogger("importer")
parser_logger = logging.getLogger("parser")
helper_logger = logging.getLogger("helper")

import logging.config
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Папка, где лежит logging_config.py
LOG_FILE = os.path.join(BASE_DIR, "logs.log")  # Абсолютный путь

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "default",
        },
    },
    'loggers': {
        'logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

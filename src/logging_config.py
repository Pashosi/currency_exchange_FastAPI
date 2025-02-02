import logging.config

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
            "filename": "src/logs.log",
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

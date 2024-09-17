import logging
from logging.config import dictConfig
from api.config import settings

def setup_logging():
    log_level = logging.getLevelName(settings.LOG_LEVEL)
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": settings.LOG_FILE,
                "formatter": "default",
                "level": log_level,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "root": {"level": log_level, "handlers": ["console", "file"]},
    }

    dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
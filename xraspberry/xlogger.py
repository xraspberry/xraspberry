# coding=utf8
import os
import sys
import logging


logger = logging.getLogger("xraspberry")
logger.setLevel(getattr(logging, os.getenv("X_LOG_LEVEL", "DEBUG"), logging.INFO))
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(name)s %(process)s %(levelname)s %(message)s"))
logger.addHandler(handler)

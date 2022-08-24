"""
Shared code

Handles logging setup
"""
import sys
import logging

from api.config import settings

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)
logger.addHandler(logging.StreamHandler(sys.stdout))

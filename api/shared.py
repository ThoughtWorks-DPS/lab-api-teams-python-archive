import json_logging, logging
import sys

logger = logging.getLogger("teams-logger")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

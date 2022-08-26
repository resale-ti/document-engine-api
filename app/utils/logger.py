import logging
from rollbar.logger import RollbarHandler


# Set root logger to log DEBUG and above
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Report ERROR and above to Rollbar
rollbar_handler = RollbarHandler()
rollbar_handler.setLevel(logging.ERROR)

# Attach Rollbar handler to the root logger
logger.addHandler(rollbar_handler)

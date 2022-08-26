from utils.logger import logger
from fastapi import status
import traceback


def response_rollbar_handler(err, response):
    traceback.print_exc()

    logger.critical(err)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {
        'error': str(err)
    }

import logging
import time
import requests
import os
import pandas as pd
from dv_utils import default_settings, Client, audit_log

logger = logging.getLogger(__name__)

# let the log go to stdout, as it will be captured by the cage operator
logging.basicConfig(
    level=default_settings.log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# define an event processing function
def event_processor(evt: dict):
    """
    Process an incoming event
    Exception raised by this function are handled by the default event listener and reported in the logs.
    """
    start = time.time()
    logger.info(f"Processing event {evt}")
    SECRET_API_HOST = os.environ.get("SECRET_API_HOST", "")
    SECRET_ACCESS_TOKEN = os.environ.get("SECRET_ACCESS_TOKEN", "")
    HMRC_HOST= os.environ.get("HMRC_HOST", "")

    if(not SECRET_API_HOST):
        raise RuntimeError("SECRET_API environment variable is not defined")
    if(not SECRET_ACCESS_TOKEN):
        raise RuntimeError("SECRET_ACCESS_TOKEN environment variable is not defined")
    if(not HMRC_HOST):
        raise RuntimeError("HMRC_HOST environment variable is not defined")

    try:
        logger.info(f"Processing event {evt}")

        secret = requests.get(f'https://{SECRET_API_HOST}/secret/hmrc', headers={'Authorization': f'Bearer {SECRET_ACCESS_TOKEN}'})
        logger.info(f'gor secret {secret.json().get("secret")}')
        response = requests.get(f'https://{HMRC_HOST}/organisations/vat/181607759/obligations?from=2021-01-25&to=2022-01-25', headers={
            'Authorization': f'Bearer {secret.json().get("secret")}',
            'Gov-Test-Scenario':'MONTHLY_THREE_MET',
             'Accept':'application/vnd.hmrc.1.0+json'
        })
        logger.error(f'got response {response.json()}')
    except Exception as err:
        logger.error(f"Failed processing event: {err}")
    finally:
        logger.info(f"Processed event in {time.time() - start:.{3}f}s")






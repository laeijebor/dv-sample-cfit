import logging
import time
import requests
import os
import json
from dv_utils import default_settings, Client, audit_log

logger = logging.getLogger(__name__)

# let the log go to stdout, as it will be captured by the cage operator
logging.basicConfig(
    level=default_settings.log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# define an event processing function
def event_processor(evt: dict):
    start = time.time()
    logger.info(f"Processing event {evt}")
    SECRET_API_HOST = os.environ.get("SECRET_API_HOST", "")
    SECRET_ACCESS_TOKEN = os.environ.get("SECRET_ACCESS_TOKEN", "")
    HMRC_HOST = os.environ.get("HMRC_HOST", "")
    DIRECT_ID_HOST = os.environ.get("DIRECT_ID_HOST", "")

    if not SECRET_API_HOST:
        raise RuntimeError("SECRET_API environment variable is not defined")
    if not SECRET_ACCESS_TOKEN:
        raise RuntimeError("SECRET_ACCESS_TOKEN environment variable is not defined")
    if not HMRC_HOST:
        raise RuntimeError("HMRC_HOST environment variable is not defined")
    if not DIRECT_ID_HOST:
        raise RuntimeError("HMRC_HOST environment variable is not defined")

    try:
        secretHMRC = requests.get(f'https://{SECRET_API_HOST}/secret/hmrc',
                                  headers={'Authorization': f'Bearer {SECRET_ACCESS_TOKEN}'})
        secretDirectId = requests.get(f'https://{SECRET_API_HOST}/secret/directId',
                                      headers={'Authorization': f'Bearer {SECRET_ACCESS_TOKEN}'})
        response = requests.get(
            f'https://{HMRC_HOST}/organisations/vat/181607759/obligations?from=2021-01-25&to=2022-01-25', headers={
                'Authorization': f'Bearer {secretHMRC.json().get("secret")}',
                'Gov-Test-Scenario': 'MONTHLY_THREE_MET',
                'Accept': 'application/vnd.hmrc.1.0+json'
            })
        logger.info(f'got response {response.json()}')
        with open("obligations.json", "w") as f:
            f.write(json.dumps(response.json()))

        response = requests.get(
            f'https://{DIRECT_ID_HOST}/data/v2/consents/d5aaf6fa-373a-44e0-f8d4-08dbf8c0132e/accounts/c7cc5181-d427-453d-88de-3d3a824ee96f/transactions',
            headers={
                'Authorization': f'Bearer {secretDirectId.json().get("secret")}',
            })
        with open("transactions.json", "w") as f:
            f.write(json.dumps(response.json()))
        logger.info(f'got response {response.json()}')
    except Exception as err:
        logger.error(f"Failed processing event: {err}")
    finally:
        logger.info(f"Processed event in {time.time() - start:.{3}f}s")

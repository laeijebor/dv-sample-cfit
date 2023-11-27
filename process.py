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

TOP_ARTISTS_QUERY = """
SELECT DISTINCT ?name 
WHERE {
    ?action <https://schema.org/additionalType> <https://schema.org/FollowAction> .
    ?action <https://schema.org/object> ?artist .
    ?artist <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/MusicGroup>; <https://schema.org/name> ?name .
}"""

# define an event processing function
def event_processor(evt: dict):
    """
    Process an incoming event
    Exception raised by this function are handled by the default event listener and reported in the logs.
    """
    
    logger.info(f"Processing event {evt}")

    # dispatch events according to their type
    evt_type =evt.get("type", "")
    if(evt_type == "ARTISTS"):
        # use the ARTISTS event processor dedicated function
        logger.info(f"use the update artists event processor")
        update_artists_event_processor(evt)
    else:
        # use the GENERIC event processor function, that basicaly does nothing
        logger.info(f"Unhandled message type, use the generic event processor")
        generic_event_processor(evt)


def generic_event_processor(evt: dict):
    pass


def update_artists_event_processor(evt: dict):
     try:
        logger.info(f"Processing event {evt}")

        client = Client()

        # push an audit log to reccord for a long duration (6months) that a artists event has been received and processed
        audit_log("received a artists event", evt=evt_type)

        # Use userIds provided in the event, or get all active users for this application
        user_ids = evt.get("userIds") if "userIds" in evt else client.get_users()

        logger.info(f"Processing {len(user_ids)} users")

        top_artists = []

        for user_id in user_ids:
            try:
                 # retrieve data graph for user
                user_data = client.get_data(user_id)

                # get top artists from user data
                top_artists_names = user_data.query(TOP_ARTISTS_QUERY)
                 for artist_name_row in top_artists_names :
                     top_artists.append( artist_name_row.get(0) )

            # pylint: disable=broad-except
            except Exception as err:
                logger.warning(f"Failed to process user {user_id} : {err}")
                try:
        # store the output file in /resources/outputs directory, to make it available for download later through the collaboration space APIs
        df = pd.DataFrame(array) 
        df.to_csv("/resources/outputs/artists.csv", index=False)
        except:
            pass
        
    except Exception as err:
        logger.error(f"Failed processing event: {err}")
        traceback.print_exc()
    finally:
        logger.info(f"Processed event in {time.time() - start:.{3}f}s")


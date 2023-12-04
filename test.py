# this code can be tested in a local environment
# for this, start a local redis server and set the appropriate variables in .env.test

# Read env variables from a local .env file, to fake the variables normally provided by the cage container
import dotenv
dotenv.load_dotenv('.env.test')
import os
import unittest
import process
import logging

DEBUG = os.environ.get('DEBUG', '').lower() == 'true'
logging.basicConfig(filename='events.log', level=logging.DEBUG if DEBUG else logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

class Test(unittest.TestCase):

    def test_process(self):
        """
        Try the process on a single user configured in the test .env file, without going through the redis queue
        """
        test_event = {
            'type': 'TEST_EVENT',
        }

        process.event_processor(test_event)

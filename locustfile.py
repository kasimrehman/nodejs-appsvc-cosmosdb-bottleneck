# Python
import os
import logging
import uuid
from locust import HttpUser, task, between
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    host = "ltestkr762.azurewebsites.net"
    timeout_duration = 90  # seconds

    def on_start(self):
        # Set debug mode from environment variable
        self.ENABLE_LOGGING = os.getenv('ENABLE_LOGGING', 'True') == 'True'
        # Set up logging
        if self.ENABLE_LOGGING:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)
        # No authentication required as per HTTP Request File



    @task
    def run_scenario(self):
        self.get_lasttimestamp()
        self.post_add()
        self.get_get()

    def get_lasttimestamp(self):
        """
        GET /lasttimestamp
        """
        url = "lasttimestamp"
        headers = {
            "Accept": "application/json"
        }
        if self.ENABLE_LOGGING:
            print("[Locust] Sending GET /lasttimestamp request")
        with self.client.get(
            url=url,
            headers=headers,
            name="GET /lasttimestamp",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.ENABLE_LOGGING:
                    print("[Locust] GET /lasttimestamp succeeded")
            else:
                msg = f"GET /lasttimestamp failed with status {response.status_code}, response: {response.text}"
                response.failure(msg)
                if self.ENABLE_LOGGING:
                    logging.error(msg)

    def post_add(self):
        """
        POST /add
        """
        url = "add"
        headers = {
            "Content-Type": "text/plain",
            "Accept": "application/json"
        }
        # Send a random number of entries between 1 and 5
        entries = str(uuid.uuid4().int % 5 + 1)
        if self.ENABLE_LOGGING:
            print(f"[Locust] Sending POST /add request with body: {entries}")
        with self.client.post(
            url=url,
            data=entries,
            headers=headers,
            name="POST /add",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.ENABLE_LOGGING:
                    print("[Locust] POST /add succeeded")
            else:
                msg = f"POST /add failed with status {response.status_code}, response: {response.text}"
                response.failure(msg)
                if self.ENABLE_LOGGING:
                    logging.error(msg)

    def get_get(self):
        """
        GET /get
        """
        url = "get"
        headers = {
            "Accept": "application/json"
        }
        if self.ENABLE_LOGGING:
            print("[Locust] Sending GET /get request")
        with self.client.get(
            url=url,
            headers=headers,
            name="GET /get",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.ENABLE_LOGGING:
                    print("[Locust] GET /get succeeded")
            else:
                msg = f"GET /get failed with status {response.status_code}, response: {response.text}"
                response.failure(msg)
                if self.ENABLE_LOGGING:
                    logging.error(msg)

    def on_stop(self):
        # No resources to clean up for this scenario
        pass

# To run:
# locust -f locustfile.py -u 10 -r 2 --run-time 1m
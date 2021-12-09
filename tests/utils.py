import requests
import time


class TestClass:
    # Api container name used as domain name
    API_ADRESS = "api_ml"
    API_PORT = 8000

    def setup_method(self):
        """
        Function to check if the api is running and can receive requests
        """
        api_up = False

        while not api_up:
            try:
                check_api = requests.get(
                    url=f"http://{self.API_ADRESS}:{self.API_PORT}/"
                )
                if check_api.status_code == 200:
                    api_up = True
                else:
                    continue

            except requests.exceptions.ConnectionError:
                print(
                    f"api is not reachable at http://{self.API_ADRESS}:{self.API_PORT}/"
                )
                print("retrying...")
                time.sleep(1)
                continue

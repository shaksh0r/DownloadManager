import requests
from requests.exceptions import HTTPError

class Download:

    def __init__(self,url,id):
        self.id = id
        self.url = url
        self.contents = None
        self.length = None



    def start_download(self):
        try:
            response = requests.get(self.url)
            print(f"Download Completed for file id#{self.id}")
            print(response)
            response.raise_for_status()
            return 1
        except ConnectionError:
            return 0
        except HTTPError:
            return -1
import requests
from pathlib import Path
from requests.exceptions import HTTPError

class Download:

    def __init__(self,url,id,file_path):
        self.id = id
        self.url = url
        self.contents = None
        self.length = None
        self.path = file_path



    def start_download(self):
        try:
            response = requests.get(self.url,timeout=1)
            print(response.headers.get("Content-Length"))
            content = response.content
            if response.headers.get("Content-Length") != len(content):
                print("Partial Download. Not Saving")
                raise EOFError("Unexpected end of response stream")
            print(f"Download Completed for file id#{self.id}")
            with open(self.path, 'bw') as file:
                file.write(content)
            print(response)
            response.raise_for_status()
            return 1
        except ConnectionError:
            return 0
        except HTTPError:
            return -1
        except EOFError:
            return -2
import requests
import os
from pathlib import Path
from requests.exceptions import HTTPError

class Download:

    def __init__(self,url,id,file_path,chunk_size):
        self.id = id
        self.url = url
        self.contents = None
        self.length = None
        self.path = file_path
        self.chunk_size = chunk_size
        self.offset = 0
        self.file_size = 0

    def head_request(self):
        try:
            response = requests.head(self.url)
            self.file_size = int(response.headers.get("Content-Length"))
        except ConnectionError:
            print("Connection Error")

    def single_download(self):
        try:
            self.offset = 0
            with open(self.path, "wb") as file:
                response = requests.get(self.url, timeout=1,stream=True)
                if response.status_code != 200:
                    raise HTTPError("not single download")

                file_size = int(response.headers.get("Content-Length"))
                file_size = file_size if file_size else None
                received_size = 0

                for data in response.iter_content(chunk_size=8192):
                    if data:
                        file.write(data)
                        received_size += len(data)


                if file_size is not None and received_size != file_size:
                    file.close()
                    raise ConnectionAbortedError("Full file not downloaded")


        except HTTPError:
            print("Single Download Failed")

    def range_download(self):
        try:
            with open(self.path,"wb") as file:
                while self.offset < self.file_size:
                    if self.offset < self.file_size:
                        header = {
                            "Range": f"bytes={self.offset}-{self.offset + self.chunk_size - 1}"
                        }
                    else:
                        header = {
                            "Range": f"bytes={self.offset}-{self.file_size - 1}"
                        }
                    response = requests.get(self.url, timeout=1,headers=header,stream=True)
                    print(response.headers.get("Content-Length"))

                    if response.status_code == 206:
                        for data in response.iter_content(chunk_size=8192):
                            if data:
                                file.write(data)
                        self.offset += len(data)

                    elif response.status_code == 200:
                        raise RuntimeError("Server stopped honoring ranges")
                    elif response.status_code == 416:
                        raise RuntimeError("Invalid range; aborting")
                    else:
                        response.raise_for_status()
            return 1
        except ConnectionError:
            return 0
        except HTTPError:
            return -1
        except EOFError:
            return -2
        except RuntimeError:
            self.single_download()
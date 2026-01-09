import uuid
from pathlib import Path
from download import Download
class Manager:

    def __init__(self):
        self.downloaded = list()


    def id_generator(self):
        return uuid.UUID

    def download(self,url,filePath):
        id = self.id_generator()
        download = Download(url,id,filePath)
        response = download.start_download()
        if response == 0:
            print("Download Failed")
        else:
            print("Download Successful")
            self.downloaded.append(id)




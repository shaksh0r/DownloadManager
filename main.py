import os
import sys
from pathlib import Path
from downloadManager import Manager


manager = Manager()

directoryPath = input("Where do you want to save this file:")
filename = input("What is the name of the file:")

root = Path(directoryPath)

if not root.is_dir():
    sys.exit()

filePath = root / filename



manager.download("http://httpbin.org/image/jpeg",filePath)
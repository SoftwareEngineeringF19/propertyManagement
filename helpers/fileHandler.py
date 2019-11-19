import os
from werkzeug.datastructures import FileStorage

class FileHandler:
    def saveImage(self, folder: str, file: FileStorage) -> None:
        file.filename = file.filename.lower()
        file.save(os.path.join(folder, file.filename))

    # returns the image path based off the folder and filename. If the requested image does
    # exist, a default image will be returned
    def getImage(self, folder, fileName) -> str:
        fileName = fileName.lower()
        filePath = os.path.join(folder, fileName)
        fileExists = os.path.isfile(filePath)
        if (not fileExists): return os.path.join(folder, 'defaultAvatar.png')
        return filePath
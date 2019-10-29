import os
from werkzeug.datastructures import FileStorage

class FileHandler:
    def saveImage(self, folder: str, file: FileStorage) -> None:
        file.save(os.path.join(folder, file.filename))

    # returns the image path based off the folder and filename. If the requested image does
    # exist, a default image will be returned
    def getImagePathOrDefault(self, folder, fileName) -> str:
        filePath = os.path.join(folder, f"{fileName}.png")
        fileExists = os.path.isfile(filePath)
        if (not fileExists): return os.path.join(folder, 'defaultAvatar.png')
        return filePath
import os

class FileHandler:
    def saveImage(self, file, folder: str) -> None:
        file.save(os.path.join(folder, file.filename))

    # returns the image path based off the folder and filename. If the requested image does
    # exist, a default image will be returned
    def getImagePathOrDefault(self, folder, fileName) -> str:
        filePath = os.path.join(folder, fileName)
        fileExists = os.path.isfile(filePath)
        if (not fileExists): return os.path.join(folder, 'defaultAvatar.png')
        return filePath
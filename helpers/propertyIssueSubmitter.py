import sys, os
from pathlib import Path
# sys.path.insert(1, os.path.join(sys.path[0], '..')) # Expose modules from root directory

from .. import database as db, config
from .. models.propertyIssue import PropertyIssue
from . fileHandler import FileHandler

class PropertyIssueSubmitter:
    def handlePropertySubmission(self, propertyIssue: PropertyIssue):
        fileHandler = FileHandler()
        imageFolderPath = f"{config.propertyIssuesImageFolder}/{propertyIssue.propertyId}/"
        if (not os.path.exists(imageFolderPath)): os.makedirs(imageFolderPath)
        propertyIssue.image.filename = self.__createUniqueImageName(imageFolderPath, propertyIssue.image.filename)
        fileHandler.saveImage(imageFolderPath, propertyIssue.image)
        db.addPropertyIssue(propertyIssue)
    
    def __createUniqueImageName(self, imageFolderPath, imageName: str) -> str: 
        filesInDirectory = list (os.listdir(imageFolderPath))
        numberOfFiles = len(filesInDirectory)
        imageNameWithoutExtension = Path(imageName).stem
        imageExtension= Path(imageName).suffix
        return f"{imageNameWithoutExtension}_{numberOfFiles}{imageExtension}"

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..')) # Expose modules from root directory

import database as db, config
from models.propertyIssue import PropertyIssue
from fileHandler import FileHandler

class PropertyIssueSubmitter:
    def handlePropertySubmission(self, propertyIssue: PropertyIssue):
        fileHandler = FileHandler()
        imageFolderPath = f"{config.propertyIssuesImageFolder}/propertyIssues/{propertyIssue.propertyId}/"
        os.makedirs(imageFolderPath)
        fileHandler.saveImage(propertyIssue.imageName, imageFolderPath)
        # db.addPropertyIssue(propertyIssue)
        print(imageFolderPath)

# p = PropertyIssue("123", "hi", 1, "hihi.png", "dom")

# pr = PropertyIssueSubmitter()

# pr.handlePropertySubmission(p)
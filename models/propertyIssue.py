from werkzeug.datastructures import FileStorage

class PropertyIssue:
    def __init__(self, propertyId: str, issueDescription: str, priority: int, image: FileStorage, submittedBy: str):
        self.propertyId = propertyId
        self.issueDescription = issueDescription
        self.priority = priority
        self.image = image
        self.submittedBy = submittedBy
    
    def toDictionary(self) -> dict:
        return {
            "Linked Property Id": self.propertyId,
            "Issue Description": self.issueDescription,
            "Priority": self.priority,
            "Image Name": self.image.filename,
            "Submitted By Tenant": self.submittedBy, 
            "Resolved": False
        }

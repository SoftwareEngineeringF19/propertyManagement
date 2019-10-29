class PropertyIssue:
    def __init__(self, propertyId: str, issueDescription: str, priority: int, imageName: str, submittedBy: str):
        self.propertyId = propertyId
        self.issueDescription = issueDescription
        self.priority = priority
        self.imageName = imageName
        self.submittedBy = submittedBy
    
    def toDictionary(self) -> dict:
        return {
            "Linked Property Id": self.propertyId,
            "Issue Description": self.issueDescription,
            "Priority": self.priority,
            "Image Name": self.imageName,
            "Submitted By Tenant": self.submittedBy
        }

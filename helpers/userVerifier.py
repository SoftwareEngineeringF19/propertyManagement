import re
from .. import database

class UserVerifier:

    # returns true if the tenant collection contains the given username and password
    def tenantExists(self, username: str, password: str) -> bool:
        tenantCollection = database.db['Tenant']
        tenant = tenantCollection.find_one({"Username": re.compile(username, re.IGNORECASE)})
        if (not tenant): return False
        if (not tenant['Password'] == password): return False
        return True
    
    # returns true if the landlord collection contains the given username and password
    def landLordExists(self, username: str, password: str) -> bool:
        landlordCollection = database.db['LandLord']
        landlord = landlordCollection.find_one({"Username": re.compile(username, re.IGNORECASE)})
        if (not landlord): return False
        if (not landlord['Password'] == password): return False
        return True

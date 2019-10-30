from .. import database as db

class UserVerifier:
    def tenantExists(self, username: str, password: str) -> bool:
        tenant = {
            "username": username,
            "password": password
        }
        
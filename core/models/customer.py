import re
from core.exceptions.base import InvalidEmailException


class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.validate_email(email)
        self.email = email

    def validate_email(self, email):
        # Simple regex for email
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern, email):
            raise InvalidEmailException(f"Invalid email address: {email}")

        return True



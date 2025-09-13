from faker import Faker
from datetime import datetime
import random
import string

fake = Faker()


def generate_user_body():
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return {
        "email": f"testuser{timestamp}@example.com",
        "password": fake.password(length=12, special_chars=True, digits=True),
        "name": fake.first_name()
    }


class UserGenerator:
    @staticmethod
    def random_user():
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return {
            "email": f"test_{random_str}@example.com",
            "password": "Qwerty123",
            "name": f"Test User {random_str}"
        }

    @staticmethod
    def random_email():
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"updated_{random_str}@example.com"

    @staticmethod
    def random_password():
        return fake.password(length=12, special_chars=True, digits=True)
import uuid

from .model import User


class UserFactory:
    def create_user(self, name: str, last_name: str) -> User:
        user_id = uuid.uuid1()
        return User(user_id, name, last_name)

from time import time
from faker import Faker


class UserInfo:
    user_id: str
    id: str
    user_name: str
    user_nick_name: str
    user_password: str
    user_email: str
    user_auth_role: str
    user_head_portrait: str
    user_create_time: time
    user_follow_topic_list: list

    def __init__(self, mock=False):
        faker = Faker()
        if mock:
            self.user_id = faker.ssn()
            self.id = faker.uuid4()
            self.user_name = faker.name_female()
            self.user_nick_name = faker.user_name()
            self.user_password = faker.password()
            self.user_email = faker.email
            self.user_auth_role = faker.numerify()
            self.user_head_portrait = faker.uri()
            self.user_create_time = faker.date_time()
            self.user_follow_topic_list = faker.pylist()
        return

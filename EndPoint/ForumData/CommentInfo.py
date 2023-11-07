from time import time

from faker import Faker


class CommentInfo:
    type_name = 'commentInfo'
    comment_id: str
    comment_content: str
    comment_state: str
    comment_username: str
    comment_create_time: str
    comment_creator_user_id: str
    comment_is_comment_to_topic: bool
    comment_father_id: int

    def __init__(self, mock=False):
        faker = Faker()
        if mock:
            self.comment_id = faker.uuid4()
            self.comment_content = faker.paragraph()
            self.comment_state = faker.null_boolean()
            self.comment_username = faker.name_female()
            self.comment_create_time = str(faker.date_time())
            self.comment_creator_user_id = faker.uuid4()
            self.comment_is_comment_to_topic = faker.null_boolean()
            self.comment_comment_id_list = faker.uuid4()
        return

    def getId(self):
        return self.comment_id

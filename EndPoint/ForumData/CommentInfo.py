from time import time

from faker import Faker


class CommentInfo:
    comment_id: str
    comment_content: str
    comment_state: str
    comment_create_time: time
    comment_creator_user_id: str
    comment_is_comment_to_topic: bool
    comment_father_id: int

    def __init__(self, mock=False):
        faker = Faker()
        if mock:
            self.comment_id = faker.uuid4()
            self.comment_content = faker.locale()
            self.comment_state = faker.null_boolean()
            self.comment_create_time = faker.date_time()
            self.comment_creator_user_id = faker.uuid4()
            self.comment_is_comment_to_topic = faker.null_boolean()
            self.comment_comment_id_list = faker.uuid4()
        return

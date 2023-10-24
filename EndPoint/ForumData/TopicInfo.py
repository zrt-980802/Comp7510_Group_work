import time

from faker import Faker


class TopicInfo:
    type_name = 'topicInfo'
    topic_id: str
    topic_title: str
    topic_content: str
    topic_annex: str
    topic_state: int
    topic_create_time: str
    topic_creator_user_id: str

    def __init__(self, mock=False):
        faker = Faker()
        if mock:
            self.topic_id = faker.uuid4()
            self.topic_title = faker.word()
            self.topic_content = faker.paragraph()
            self.topic_annex = faker.url()
            self.topic_state = faker.random_digit()
            self.topic_create_time = str(faker.date_time())
            self.topic_creator_user_id = faker.uuid4()
        return

    def getId(self):
        return self.topic_id

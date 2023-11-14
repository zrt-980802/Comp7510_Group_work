class PostInfo:
    type_name = 'postInfo'
    post_id: str = None
    post_title: str = None
    post_content: str = None
    post_annex: list = None
    post_state: int = None  # 0 normal -1 deleted
    post_create_time: str = None
    post_create_time_num: int = None
    post_creator_user_id: str = None

    def __init__(self, mock=False):
        # faker = Faker()
        # if mock:
        #     self.post_id = faker.uuid4()
        #     self.post_title = faker.word()
        #     self.post_content = faker.paragraph()
        #     self.post_annex = [faker.url(), faker.url(), faker.url()]
        #     self.post_state = faker.random_digit()
        #     self.post_create_time = str(faker.date_time())
        #     self.post_create_time_num = time.time()
        #     self.post_creator_user_id = faker.uuid4()
        return

    def getId(self):
        return self.post_id

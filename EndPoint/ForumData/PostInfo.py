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

    def __init__(self):
        return

    def getId(self):
        return self.post_id

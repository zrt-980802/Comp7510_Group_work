
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

    def __init__(self):
        return

    def getId(self):
        return self.comment_id

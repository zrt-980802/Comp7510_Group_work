
class UserInfo:
    type_name = 'userInfo'
    user_id: str
    id: str
    user_name: str
    user_nick_name: str
    user_password: str
    user_phone_number: str
    user_email: str
    user_auth_role: str
    user_head_portrait: list
    user_create_time: str
    user_follow_topic_list: list

    def __init__(self):
        return

    def getId(self):
        return self.user_id

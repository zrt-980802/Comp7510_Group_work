import json
from types import SimpleNamespace

import certifi
import os

from EndPoint.ForumData.CommentInfo import CommentInfo
from EndPoint.ForumData.TopicInfo import TopicInfo
from EndPoint.ForumData.UserInfo import UserInfo

os.environ['SSL_CERT_FILE'] = certifi.where()

import firebase_admin
from firebase_admin import db, storage

cred_obj = firebase_admin.credentials.Certificate('json/comp_23458844.json')

firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://comp7510-934b1-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'gs://comp7510-934b1.appspot.com'
})

db_ref = db.reference('/server/data')
bucket = storage.bucket()


def to_json(data):
    # return json.dumps(self, cls=MyEncoder, indent=4)
    print(data.__dict__)
    return json.dumps(data.__dict__)


def setInfo(info):
    db_ref.child(info.type_name).child(info.getId()).set(to_json(info))


def updateInfo(info):
    setInfo(info)


def getUserInfoById(userId: str):
    return json.loads(getInfo(userId, UserInfo.type_name), object_hook=UserInfo)


def getTopicInfoById(userId: str):
    return json.loads(getInfo(userId, TopicInfo.type_name), object_hook=TopicInfo)


def getCommentInfoById(userId: str):
    return json.loads(getInfo(userId, CommentInfo.type_name), object_hook=CommentInfo)


def getInfo(ID: str, type_name):
    return db_ref.child(type_name).child(ID).get()

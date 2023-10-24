import json
import uuid
from types import SimpleNamespace

import certifi
import os

from EndPoint.ForumData.CommentInfo import CommentInfo
from EndPoint.ForumData.PostInfo import PostInfo
from EndPoint.ForumData.UserInfo import UserInfo

os.environ['SSL_CERT_FILE'] = certifi.where()

import firebase_admin
from firebase_admin import db, storage
from google.cloud.storage import transfer_manager

cred_obj = firebase_admin.credentials.Certificate('json/token.json')

firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://comp7510-934b1-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'comp7510-934b1.appspot.com'
})

db_ref = db.reference('/server/data')
bucket = storage.bucket()


# def to_json(data):
#     # return json.dumps(self, cls=MyEncoder, indent=4)
#     print(data.__dict__)
#     return json.dumps(data.__dict__)


def setInfo(info):
    data_ref = db_ref.child(info.type_name).child(info.getId())  # .set(to_json(info))
    for data in info.__dict__.items():
        data_ref.child(data[0]).set(data[1])


def updateInfo(info):
    setInfo(info)


# 下面四个getInfo函数返回dict


def getUserInfoById(userId: str):
    """
    :param userId:
    :return: dict
    """
    return getInfo(userId, UserInfo.type_name)


def getPostInfoById(postId: str):
    """
    :param postId:
    :return: dict
    """
    return getInfo(postId, PostInfo.type_name)


def getCommentInfoById(commentId: str):
    """
    :param commentId:
    :return: dict
    """
    return getInfo(commentId, CommentInfo.type_name)


def getInfo(ID: str, type_name):
    """
    :param ID:
    :type_name:
    :return: dict
    """
    return db_ref.child(type_name).child(ID).get()


def uploadFile(filePath):
    fileId = uuid.uuid1()
    return upload_blob(filePath, fileId)


def upload_blob(filePath, fileId):
    fileName = os.path.basename(filePath)
    blob = bucket.blob(str(fileId) + '/' + fileName)
    print(str(fileId) + '/' + fileName)
    blob.upload_from_filename(filePath)
    blob.make_public()
    return blob.public_url

# todo 完善多文件上传
def upload_many_blobs_with_transfer_manager(filenames, source_directory="", processes=8
):
    results = transfer_manager.upload_many_from_filenames(
        bucket, filenames, source_directory=source_directory, max_workers=processes
    )

    for name, result in zip(filenames, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))

import uuid
import certifi
import os
import base64

from EndPoint.ForumData.CommentInfo import CommentInfo
from EndPoint.ForumData.PostInfo import PostInfo
from EndPoint.ForumData.UserInfo import UserInfo

import firebase_admin
from firebase_admin import db, storage

os.environ['SSL_CERT_FILE'] = certifi.where()

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
    # print(str(fileId) + '/' + fileName)
    path = str(fileId) + '/' + fileName
    blob.upload_from_filename(filePath)
    blob.make_public()
    return path, blob.public_url


def downloadFile(downLoadFilePath, saveFilePath):
    blob = bucket.blob(downLoadFilePath)
    blob.download_to_filename(saveFilePath)
    print(f"download successful,{saveFilePath}")


def deleteFile(deleteFilePath):
    blob = bucket.blob(deleteFilePath)

    try:
        blob.delete()
        print(f'{deleteFilePath} is deleted')
    except:
        print(f'The target file {deleteFilePath} does not exist.')



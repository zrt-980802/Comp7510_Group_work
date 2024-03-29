import json
import uuid
import certifi
import os

from EndPoint.ForumData.CommentInfo import CommentInfo
from EndPoint.ForumData.PostInfo import PostInfo
from EndPoint.ForumData.UserInfo import UserInfo

import firebase_admin
from firebase_admin import db, storage

from Tools import NowTime

os.environ['SSL_CERT_FILE'] = certifi.where()

cred_obj = firebase_admin.credentials.Certificate('source/json/token.json')
with open('source/json/path.json', 'r') as file:
    firebaseRes = json.load(file)
firebase_admin.initialize_app(cred_obj, firebaseRes)

dataBasePath = '/server/data'
db_ref = db.reference('/server/data')
bucket = storage.bucket()
userIdNameRelationship = 'UINR'
userIdCommentIdRelationship = 'UICR'
userIdPostIdRelationship = 'UIPR'


def setInfo(info):
    data_ref = db_ref.child(info.type_name).child(info.getId())
    for data in info.__dict__.items():
        print(data)
        if data[1] is None:
            continue
        data_ref.child(data[0]).set(data[1])


def deleteInfo(info):
    data_ref = db_ref.child(info.type_name).child(info.getId())
    data_ref.delete()


def getUserIdAndUserNameRel(userName):
    data_ref = db_ref.child(userIdNameRelationship).child(userName)
    return data_ref.get()


def setUserIdAndUserNameRel(userId, userName):
    data_ref = db_ref.child(userIdNameRelationship).child(userName)
    data_ref.set(userId)


def deleteUserIdAndUserNameRel(userName):
    data_ref = db_ref.child(userIdNameRelationship).child(userName)
    data_ref.delete()


def updateUserIdAndUserNameRel(userId, userName, oldUserName):
    deleteUserIdAndUserNameRel(oldUserName)
    setUserIdAndUserNameRel(userId, userName)


def isUserNameExist(userName):
    rela = getUserIdAndUserNameRel(userName)
    if rela is None:
        return [False]
    return [True, rela]


def updateInfo(info):
    setInfo(info)


# 下面四个getInfo函数返回dict


def getUserInfoById(userId: str):
    """
    :param userId:
    :return: dict
    """
    data = getInfo(userId, UserInfo.type_name)
    userInfo = UserInfo()
    userInfo.__dict__.update(data)
    # print(userInfo.__dict__)
    return userInfo


def getPostInfoByPostId(postId: str):
    """
    :param postId:
    :return: dict
    """
    data = getInfo(postId, PostInfo.type_name)
    postInfo = PostInfo()
    postInfo.__dict__.update(data)
    if postInfo.post_state == '-1':
        return None
    return postInfo


def getCommentInfoById(commentId: str):
    """
    :param commentId:
    :return: dict
    """
    data = getInfo(commentId, CommentInfo.type_name)
    commentInfo = CommentInfo()
    commentInfo.__dict__.update(data)
    return commentInfo


def getInfo(ID: str, typeName):
    """
    :param ID:
    :type_name:
    :return: dict
    """
    if ID == '' or ID is None:
        return None
    return db_ref.child(typeName).child(ID).get()


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


def getLatestPost(count=10):
    data_ref = db.reference(dataBasePath + '/postInfo')
    # data = data_ref.order_by_child('post_create_time_num').get()
    # data = data_ref.order_by_key().limit_to_first(count).get()
    datas = data_ref.get()
    list = []
    if datas is None:
        return None
    for data in datas:
        tmp = datas[data]
        if tmp['post_state'] == '-1':
            continue
        tmp['post_create_time_num'] = float(tmp['post_create_time_num'])
        list.append(tmp)
    list.sort(key=lambda x: x['post_create_time_num'], reverse=True)
    # print(data)
    return list[0:min(count, len(list))]


def getPostByKeyword(keyword):
    data_ref = db_ref.child('postInfo')
    datas = data_ref.get()
    result = []
    # print(datas)
    for data in datas:
        # print(data)
        if keyword in datas[data]['post_title']:
            # print(data)
            if datas[data]['post_state'] == '-1':
                continue
            result.append(datas[data])
    return result


def getLatestComment(postId):
    data_ref = db_ref.child(userIdCommentIdRelationship).child(postId)
    data = data_ref.get()
    tmp = []
    result = []
    if data is not None:
        for userId in data:
            for commentId in data[userId]:
                tmp.append([NowTime.str2TimeNum(data[userId][commentId]), userId, commentId])
        tmp.sort()
        count = 0
        for item in tmp:
            count += 1
            if count == 5:
                break
            commentInfo = getCommentInfoById(item[2])
            userInfo = getUserInfoById(item[1])
            info = {'userInfo': userInfo, 'commentInfo': commentInfo}
            result.append(info)
    return result


def setUserIdCommentIdRelationship(postId, userId, commentId):
    data_ref = db_ref.child(userIdCommentIdRelationship).child(postId).child(userId).child(commentId)
    data_ref.set(NowTime.nowYMDHMS())


def deleteUserIdCommentIdRelationshipByCommentId(postId, userId, commentId):
    data_ref = db_ref.child(userIdCommentIdRelationship).child(postId).child(userId).child(commentId)
    data_ref.delete()


def setUserIdPostIdRelationshipByUserId(userId, postId):
    data_ref = db_ref.child(userIdPostIdRelationship).child(userId).child(postId)
    data_ref.set(NowTime.nowYMDHMS())


def getUserIdPostIdRelationshipByUserId(userId):
    data_ref = db_ref.child(userIdPostIdRelationship).child(userId)
    return data_ref.get()


def deleteUserIdPostIdRelationshipByUserId(userId, postId):
    data_ref = db_ref.child(userIdPostIdRelationship).child(userId).child(postId)
    data_ref.delete()


def deletePostByPostIdAndHide(postId):
    data_ref = db_ref.child('postInfo').child(postId).child('post_state')
    data_ref.set('-1')


def getAllPostByUserId(userId):
    datas = getUserIdPostIdRelationshipByUserId(userId)
    result = []
    for data in datas:
        postInfo = getPostInfoByPostId(data)

        if postInfo is not None and postInfo.post_state == '0':
            result.append(postInfo)
    return result

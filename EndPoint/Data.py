import json

import certifi
import os

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


def getUserInfoById(userId: str):
    pass


def setInfo(info):
    db_ref.child(info.type_name).child(info.getId()).set(to_json(info))

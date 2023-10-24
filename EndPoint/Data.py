import certifi
import os

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


import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'thread-fetcher.appspot.com'
})

bucket = storage.bucket()
file =bucket.blob('username/threads')
file.upload_from_filename('./twitter_thread.md')
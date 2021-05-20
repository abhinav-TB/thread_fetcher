import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

class Firebase_util:
    def __init__(self):
        cred = credentials.Certificate("./config/key.json")
        firebase_admin.initialize_app(cred, {
        'storageBucket': 'thread-fetcher.appspot.com'
     })
        self.bucket = storage.bucket()
    def add_to_bucket(self,thread_name,user_name):
        file =self.bucket.blob(f'{user_name}/{thread_name}')
        file.upload_from_filename(f'./{thread_name}.pdf')




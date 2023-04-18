import firebase_admin
from firebase_admin import credentials, storage
from google.cloud.exceptions import NotFound

# Initialize Firebase app with credentials
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
  "storageBucket": "signuplogin-ee55f.appspot.com"
})

# # Download video from Firebase Storage
def download_video():
  bucket = storage.bucket()
  blob = bucket.blob('video/data/user/0/com.example.new_app/cache/5b1acfa3-e166-4592-b14d-5cd42065285d/VID-20230305-WA0000.mp4')

  try:
      blob.download_to_filename('example.mp4')
      print('Downloaded video successfully.')
  except NotFound:
      print('Video not found in Firebase Storage bucket.')
  except Exception as e:
    print('An error occurred while downloading the video:', e)

# # Upload video to Firebase Storage
# new_blob = bucket.blob('Sample.mp4')
# new_blob.upload_from_filename('Sample.mp4')

# import pyrebase

# config = {
#   "apiKey": "AIzaSyBgSe5R_ufSD4Ht1L4oSNK6p9TKVg-N16w",
#   "authDomain": "signuplogin-ee55f.firebaseapp.com",
#   "projectId": "signuplogin-ee55f",
#   "storageBucket": "signuplogin-ee55f.appspot.com",
#   "serviceAccount":"serviceAccountKey.json"
# }

# firebase_storage = pyrebase.initialize_app(config)
# storage = firebase_storage.storage()

# storage.child("Sample.mp4").put("Sample.mp4")
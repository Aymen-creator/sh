import pyrebase
from datetime import datetime
import urllib

firebase_config = {
  "apiKey": "AIzaSyBEDTRsyhZE6K84acVvg76PYEkwHBB-m8I",
  "authDomain": "tryman-b1ac7.firebaseapp.com",
  "projectId": "tryman-b1ac7",
  "databaseURL":"https://tryman-b1ac7-default-rtdb.firebaseio.com/",
  "storageBucket": "tryman-b1ac7.appspot.com",
  "messagingSenderId": "57273287940",
  "appId": "1:57273287940:web:4c656f5599fa2eec347c51",
  "measurementId": "G-SZW65WFQ6Z"
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()
storage = firebase.storage()

def stream_handler(message):
    EVENT = message["event"] 
    PATH = message["path"]
    Data = message["data"]
    
    id = Data.get("ID")
    long_txt = Data.get("long_txt")
    small_txt = Data.get("small_txt")

    if id and long_txt:
        # Downloading the image
        storage.child(f"images/{id}.png").download("d.txt","d.png")

        read_files = str(urllib.request.urlopen(long_txt).read())
        print(read_files[2:-1])

my_stream = db.child("news_info").stream(stream_handler)



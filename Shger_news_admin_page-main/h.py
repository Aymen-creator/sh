import pyrebase
from datetime import datetime


firebase_config = {
  "apiKey": "AIzaSyDTV6HFCfR9xOT1ydmjl0IcRb1sJSOOvWo",
  "authDomain": "sheger-sport.firebaseapp.com",
  "databaseURL": "https://sheger-sport-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "sheger-sport",
  "storageBucket": "sheger-sport.appspot.com",
  "messagingSenderId": "666267325545",
  "appId": "1:666267325545:web:6f62a094e6d8cb279f7ef8",
  "measurementId": "G-7TQ0EEHPVN"
}

firebase = pyrebase.initialize_app(firebase_config)

# auth = firebase.auth()
# email = "addisum443@gmail.com"
# password = "QWE123@QWE"

# auth.create_user_with_email_and_password(email, password)


db = firebase.database()
storage = firebase.storage()

# Using date and time as an ID for each news so that they are random every time
date_and_time = str(datetime.now())[::-1]
Normal_ID = date_and_time.replace(":", "").replace("-", "").replace(".", "").replace(" ","")

## fix this not only png available
image_name = Normal_ID + ".png"

# Taking the input from the user 
Short_txt = input("Please Enter the short text: ")
long_txt = input("Please Enter the real text: ")


# Uploading the image for the news
storage.child(f"images/{image_name}").put("instagram.png")
url_image = storage.child(f"images/{image_name}").get_url(None)


# Creating a text file for the whole news
with open(f"{Normal_ID}.txt", "w") as f:
    f.write(long_txt)


# Uploading the txt file
storage.child(f"{Normal_ID}.txt").put(f"{Normal_ID}.txt")
url_text = storage.child(f"{Normal_ID}.txt").get_url(None)


Data = {"ID": Normal_ID, "small_txt":Short_txt, "long_txt":url_text, "image":url_image}
db.child("news_info").push(Data)


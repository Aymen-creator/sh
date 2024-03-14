from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
import pyrebase
from datetime import datetime


'''
Code for firebase after prodxution is done

for both cases everyone can read data 
but only signed in users can write data meaning that only the admins can write data

Storage Rule for Firebase 
{
  "rules": {
    ".star": {
      "allow": "false"
    },
    "{userId}": {
      ".read": "true",
      ".write": "request.auth == userId" 
    }
  }
}


Database Rule for Firebase
{
  "rules": {
    ".read": "true", 
    ".write": "request.auth != null" 
  }
}

'''

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

# Create your views here.

# Login page
def login(response):
    if response.method == "POST":  
        auth = firebase.auth()

        email = response.POST.get("email") 
        password = response.POST.get("password")

        try:
            auth.sign_in_with_email_and_password(email,password)
            return redirect(index)
            
        except:
            return render(response, "main/login.html", {"error":"error"})
    else:
        return render(response, "main/login.html", {})

# Renders the homepage
def index(response):
    return render(response,"main/index.html",{})

# Add news
def add(request):
    if request.method == 'POST' and request.FILES['image']:
        Full_news = request.POST.get("full_news")
        Title_news = request.POST.get("title_news")
        news_type = ""

        type_of_news_list = ["trending","hot","normal","latest"]

        for item in type_of_news_list:
            if request.POST.get(item) == "on":
                news_type = item

        image = request.FILES['image']
        file_type = image.content_type.split("/")[-1]

        db = firebase.database()
        storage = firebase.storage()

        date_and_time = str(datetime.now())[::-1]
        Normal_ID = date_and_time.replace(":", "").replace("-", "").replace(".", "").replace(" ","")

        
        # Checking if it is image or not
        if not image.content_type.startswith('image/'):
            return render(request, 'main/add.html', {"sucess":"False","error":"wrong file"})

        try:
            # Use a unique name for the image based on current timestamp
            image_name = Normal_ID + str(file_type)

            with image.open() as image_file:
                # Uploading the file to Firebase's Storage
                storage.child(f'images/{image_name}').put(image_file.read(), content_type=image.content_type)
                url_image = storage.child(f"images/{image_name}").get_url(None)

                # Writing the data in the Database
                Data = {"ID": Normal_ID, "title":Title_news, "full":Full_news, "image":url_image, "type":news_type}
                db.child("news_info").push(Data)

                return render(request, 'main/add.html', {"sucess":"True"})
            
        except ValidationError as e:
            return render(request, 'main/add.html', {"sucess":"False","error":e})
        except Exception as e:
            return render(request, 'main/add.html', {"sucess":"False","error":e})
    else:
        return render(request, 'main/add.html', {}) 

# Delete News
def delete(request):
    arr = []
    IDs = []

    db = firebase.database()
    all_users = db.child("news_info").get()
    
    for user in all_users.each():
        values = user.val()
        arr.append([user.key(),values["title"],values["full"]])
        IDs.append(user.key())

    if request.method == "POST":
        # Deleting info from the database
        for i in IDs:
            if request.POST.get(i) == "habibi":
                db.child("news_info").child(i).remove()
        arr = []
        IDs = []
        for user in all_users.each():
            values = user.val()
            arr.append([user.key(),values["title"],values["full"]])
            IDs.append(user.key())

        return render(request, "main/delete.html", {"arr":arr})

    return render(request, "main/delete.html", {"arr":arr})




















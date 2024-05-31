import  firebase_admin
from firebase_admin import db, credentials

cred = credentials.Certificate("credentials.json")
obj = firebase_admin.initialize_app(cred, {"databaseURL": "https://conq-5bd89-default-rtdb.firebaseio.com"})
ref = db.reference("/")  #Root! Need to implement game specific subdirectories
#ref.child("territories").delete()
#ref.child("cards").delete()

def listener(event):
    print(f"Firebase event: {event.event_type} {event.path} {event.data}")

db.reference("/commands", app=obj).listen(listener)  #Adding the listener after database is loaded


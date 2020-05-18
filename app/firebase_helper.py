import pyrebase

config = {
    'apiKey': "AIzaSyDPW7RbXbDvJjamLCz-LxH1nyjwkwRkeiY",
    'authDomain': "kids-reward-system.firebaseapp.com",
    'databaseURL': "https://kids-reward-system.firebaseio.com",
    'projectId': "kids-reward-system",
    'storageBucket': "kids-reward-system.appspot.com",
    'messagingSenderId': "699180178462",
    'appId': "1:699180178462:web:dbbe08f6ed31841770220f"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def child_by_id(token_id, firebase_id):
    child = db.child("kids").child("kids_list").child(firebase_id).get(token_id).val()
    return child


def all_kids_list(token_id):
    all_kids = db.child('kids').child("kids_list").get(token_id).val()
    return all_kids


def all_parents_list(token_id):
    all_parents = db.child("parents").get(token_id).val()
    # print (all_parents)
    return all_parents

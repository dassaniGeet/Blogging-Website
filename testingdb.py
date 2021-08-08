from firebase import firebase
import pyrebase

Config = {
    'apiKey': "AIzaSyDtGyCnOxSqf3Lbx4DznqP6JvDx-1aljIM",
    'authDomain': "testingdb-9eec2.firebaseapp.com",
    'databaseURL': "https://testingdb-9eec2-default-rtdb.firebaseio.com",
    'projectId': "testingdb-9eec2",
    'storageBucket': "testingdb-9eec2.appspot.com",
    'messagingSenderId': "352267392961",
    'appId': "1:352267392961:web:96b9b946c5a6db441c0140",
    'measurementId': "G-5H2KV3XVPY"
}

firebase=pyrebase.initialize_app(Config)
db=firebase.database()

# data={
#     'name': 'geet',
#     'data': {
#     'Email': 'you@example.com',
#     'Phone': '8008899870'
# }
# }
# db.child("family").push(data)

# data={
#     'name': 'ansh',
#     'data': {
#     'Email': 'you@example.com',
#     'Phone': '8008899870'
# }
# }
# db.child("family").push(data)

# data={
#     'name': 'vijay',
#     'data': {
#     'Email': 'you@example.com',
#     'Phone': '8008899870'
# }
# }
# db.child("family").push(data)

# data={
#     'name': 'jaya',
#     'data': {
#     'Email': 'you@example.com',
#     'Phone': '8008899870'
# }
# }
# db.child("family").push(data)


info=db.child("family").get()
for x in info.each():
    if x.val()['name'] == "ansh":
        new_post = x.val()
        break
  # print(x.val())
#   print(x.val()['name'])
#   print(x.val()['data']['Phone'])

print(new_post['data']['Phone'])


print("Retrieved.")
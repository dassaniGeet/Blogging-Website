from flask import Flask, render_template, request, session, flash
from firebase import firebase
import pyrebase
import json
import smtplib
from email.message import EmailMessage


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']

app = Flask(__name__)
app.secret_key = "abcd"


if(local_server):
    uri = params['local_uri']
else:
    uri = params['prod_uri']


firebaseConfig = {
    'apiKey': "AIzaSyD5m8dxhIyy_jXyeEyE5Da64POrv9PcExc",
    'authDomain': "whishing-blog.firebaseapp.com",
    'projectId': "whishing-blog",
    'databaseURL': "https://whishing-blog-default-rtdb.firebaseio.com/",
    'storageBucket': "whishing-blog.appspot.com",
    'messagingSenderId': "890995803700",
    'appId': "1:890995803700:web:c41b6ef681fed1078eec61",
    'measurementId': "G-ML6CK26YK6"
}

Firebase = pyrebase.initialize_app(firebaseConfig)
db = Firebase.database()


# data={
#     'slug': 'second-post',
#     'details': {
#     'sno': 2,
#     'title': 'Here comes the Anime.',
#     'content': 'Anime (Japanese: アニメ, IPA: [aɲime] (About this soundlisten)) is hand-drawn and computer animation originating from Japan. In Japan and in Japanese, anime (a term derived from the English word animation) describes all animated works, regardless of style or origin. However, outside of Japan and in English, anime is colloquial for Japanese animation and refers specifically to animation produced in Japan.[1] Animation produced outside of Japan with similar style to Japanese animation is referred to as anime-influenced animation.'
# }
# }

# db.child("Posts").push(data)

@app.route("/")
def home():
    posts = db.child("Posts").get()
    return render_template('index.html', params=params, posts=posts)


@app.route("/index")
def firstpage():
    posts = db.child("Posts").get()
    return render_template('index.html', params=params, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    if('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard.html')

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if(username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            return render_template('dashboard.html')

    return render_template('sign-in.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    print(post_slug)
    info = db.child("Posts").get()
    for x in info.each():
        if x.val()['slug'] == post_slug:
            new_post = x.val()
            break
    return render_template('post.html', params=params, new_post=new_post)


@app.route("/createposts", methods=['POST', 'GET'])
def createposts():

    if(request.method == 'POST'):
        name = request.form.get('name')
        slug = request.form.get('slug')
        title = request.form.get('title')
        content = request.form.get('content')

        data = {
            'slug': slug,
            'details': {
                'name': name,
                'title': title,
                'content': content
            }
        }

        if data['slug'] != "":
            db.child("Posts").push(data)
            flash('Post Created Successfully')
        else:
            flash('Please Enter Valid Data')

    return render_template('createposts.html', params=params)


@app.route("/contact", methods=['POST', 'GET'])
def contact():

    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        data = {
            'Name': name,
            'details': {
                'Email': email,
                'Phone': phone,
                'Message': message
            }
        }

        db.child("Contacts").push(data)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        new_msg = EmailMessage()

        s.starttls()

        sender = params['gmail-user']
        receivers = [email]

        new_msg['Subject'] = "New Member In The Blog"
        new_msg['From'] = sender
        new_msg['To'] = receivers
        new_msg.set_content("Name: " + name + "\nEmail: " +
                            email + "\nPhone: " + phone + "\nMessage: " + message)

        s.login("geetdassani93@gmail.com", "waheguru@93")

        s.send_message(new_msg)

        s.quit()

    return render_template('contact.html', params=params)


app.run(debug=True)

from flask import Flask, url_for, session, render_template, redirect, abort, request
from authlib.integrations.flask_client import OAuth
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import pandas as pd
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Daviz"
mongo =PyMongo(app)

def config():
    load_dotenv()

app.secret_key = os.getenv('flask_secret')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='daviz',
    client_id=os.getenv('clientID'),
    client_secret=os.getenv('clientsecret'),
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/')
def home():
    user = session.get('user')
    name=user['name']
    email=user['email']
    query={'email_id':email}
    doc ={'$set':{'email_id':email,'name':name}}
    mongo.db.user.update_one(query,doc,upsert=True)
    return render_template('login.html', user=name)



@app.route('/login')
def login():
    if "user" in session:
        abort(404)
    return oauth.daviz.authorize_redirect(redirect_uri=url_for('gsignin', _external=True))


@app.route('/gsignin')
def gsignin():
    token = oauth.daviz.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("home.html")

app.config["UPLOAD_FOLDER1"]="static/csvfiles"

@app.route("/",methods=['GET','POST'])
def upload():
    if request.method=='POST':
        upload_csv=request.files['upload_file']
        if upload_csv.filename != '':
            file_path=os.path.join(app.config["UPLOAD_FOLDER1"], upload_csv.filename)
            upload_csv.save(file_path)
            upload_csv.seek(0)
            data=pd.read_csv(upload_csv)
            # print(data)
            return render_template("Upload.html",data=data.to_html(index=False))
    return render_template("home.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=os.getenv('flask_port'), debug=True)
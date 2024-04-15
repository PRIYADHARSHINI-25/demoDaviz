from flask import Flask, url_for, session, render_template, redirect, abort
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

app = Flask(__name__)
def config():
    load_dotenv()
appConfiguration = {
    # "DAVIZ_CLIENT_ID": "45114726904-1v6o2v0etu1l60fhu90msogrjehksmgg.apps.googleusercontent.com",
    # "DAVIZ_CLIENT_SECRET": "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",
    "FLASK_SECRET": "b7ad6c36-dbac-43cc-a540-c87630c77181",
    "FLASK_PORT": 5000
}
app.secret_key = appConfiguration.get("FLASK_SECRET")
#app.config.from_object('config')

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
    return render_template('home.html', user=user)


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
    return redirect('/')

@app.route("/",methods=['GET','POST'])
def fileUpload():
    return render_template("FileUpload.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=appConfiguration.get("FLASK_PORT"), debug=True)
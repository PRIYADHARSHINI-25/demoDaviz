from flask import Flask, url_for, session, render_template, redirect, abort, request
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from io import StringIO
import pandas as pd
import os,gridfs
from charts import preprocess,chartvis

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Daviz1"
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
        return render_template('login.html')

@app.route('/login')
def login():
    if "user" in session:
        user = session.get('user')
        name=user['name']
        return render_template('home.html',user=name)   
    return oauth.daviz.authorize_redirect(redirect_uri=url_for('gsignin', _external=True))


@app.route('/gsignin')
def gsignin():
    token = oauth.daviz.authorize_access_token()
    try:
        if token:
            session['user'] = token['userinfo']
            user = session.get('user')
            name=user['name']
            email=user['email']
            profile=user['picture']
                # verify=user['email_verified']
            query={'email_id':email}
            doc ={'$set':{'email_id':email,'name':name,'profile':profile}}
            mongo.db.user.update_one(query,doc,upsert=True)
            return render_template('home.html', user=name)
    except:
        return "not working"
    # return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("login.html")

# app.config["UPLOAD_FOLDER1"]="static/csvfiles"

# @app.route("/",methods=['GET','POST'])
# def upload():
#     if request.method=='POST':
#         upload_csv=request.files['upload_file']
#         if upload_csv.filename != '':
#             file_path=os.path.join(app.config["UPLOAD_FOLDER1"], upload_csv.filename)
#             upload_csv.save(file_path)
#             upload_csv.seek(0)
#             data=pd.read_csv(upload_csv)
#             return render_template("Upload.html",data=data.to_html(index=False))
#     return render_template("home.html")


@app.route("/chart",methods=['GET','POST'])
def chart():
    filegrid=gridfs.GridFS(mongo.db)
    user = session.get('user')
    email=user['email']
    if request.method=='POST':
        upload_csv=request.files['upload_file']
        # xvar=request.form.get('xAxis')
        # yvar=request.form.get('yAxis')
        # charttype=request.form.get('charttype')
        # print(xvar,yvar,charttype)
        # content.seek(0)
        content=upload_csv.read()
        csv_id=filegrid.put(content,filename=upload_csv.filename)
        mongo.db.user.update_one({'email_id':email},{'$set':{'files':csv_id}})
        grid_out = filegrid.get(csv_id)
        data = grid_out.read()
        option,df=preprocess(data)
        session['df'] = df.to_json()
        types=['line','bar','pie']
        # if xvar and yvar and charttype:
        #     chart_user= chartvis(df,xvar,yvar,charttype)
        #     return render_template("chart.html",data=chart_user)
        return render_template("chart.html",option=option,types=types)
    return render_template("login.html")

@app.route("/visualize",methods=['GET','POST'])
def visualize():
    if 'df' in session:
        df=session['df']
        df = pd.read_json(StringIO(df)) 
        print(df.head(3))
    if request.method=='POST':
         # Get the AJAX data sent from the HTML
        # charttype=request.form.get('charttyype')
        var=request.form.get("teamDropdown")
        var1=request.form.get("teamDropdown1")
        # yvar=request.form.get('yvar')
        charttype=var
        xvar=var1
        yvar='Class'
        print(xvar, yvar, charttype)
        if xvar and yvar and charttype:
            chart_user= chartvis(df,xvar,yvar,charttype)
            print(chart_user )
            return render_template("logged.html",data=chart_user,var=var)
        else:
            return "Give valid input"

if __name__=="__main__":
    app.run(port=os.getenv('flask_port'), debug=True)
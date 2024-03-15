from flask import Flask, request, jsonify,render_template

from models import *

app = Flask(__name__)


@app.route('/')
def signup():
    return render_template("signup.html")
   
@app.route('/get_signup',methods=['GET','POST'])
def get_signup():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify({"users":users})

   

@app.route('/post_signup', methods=['POST'])
def post_signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        add_user(username, email, password)
        return jsonify({"message": "Welcome, {}!".format(username)})
    else:
        return "Method Not Allowed", 405

@app.route('/delete')
def delete_userS():
    try:
        id=3
        delete_user(id)
        return "delete"
    except:
        return "no"

if __name__ == '__main__':
    app.run(debug=True)
     

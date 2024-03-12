from flask import Flask , render_template, Request,session
app = Flask(__name__)
@app.route('/')
def login():
    return 'login.html'
if __name__=="__main__":
    app.run(debug=True)         

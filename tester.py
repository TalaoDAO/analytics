from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
appFlask = Flask(__name__)
appFlask.secret_key = "27eduCBA09"
appFlask.permanent_session_lifetime = timedelta(minutes=5)
@appFlask.route("/")
def home():
    return '''<h1>The session value is: {}</h1>'''.format(session["user"])
@appFlask.route("/login")
def login():
    session["user"] = "user1"
    return '''<h1>The session value is: {}</h1>'''.format(session["user"])
@appFlask.route("/logout")
def logout():
    variable = session["user"] 
    session.pop("user", None)
    return '''<h1>The deleted session is: {}</h1>'''.format(variable)
if __name__ == "__main__":
    appFlask.run(debug=True)
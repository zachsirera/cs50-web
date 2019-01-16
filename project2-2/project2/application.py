import os

from flask import Flask, render_template, request
# from flask_socketio import SocketIO, emit

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app)


@app.route("/", methods = ["GET", "POST"])
def index():

	if request.method == "POST":
		test = request.form.get("test")

		return render_template("blank.html", test = test)

	else:

		return render_template("blank.html")
    

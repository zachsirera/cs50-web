import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Create empty lists needed for data handling
display_names = []
channels = []

@app.route("/", methods=["GET", "POST"])
def index():

	if request.method == "POST":

		# Need to check local storage and see if the user already has a display name associated with them, and if so, log them in automatically
		# Else:

		# Get the users chosen display name from form
		display_name = request.form.get("display_name")

		# Verify that the user's name is available
		if display_name in display_names:
			error = "This username is not available."
			return render_template("error.html", Error = error)
		else:
			# The username is available
			display_names.append(display_name)

			# Redirect user to a list of all channels or the option to select a chat channel. 

			# If user submits name of new channel, verify that it is available.

			# If channel name is unavailable, ask the user if they would like to join that channel or if they would like to submit another name. 

			return render_template("home.html", name = display_name)


	else:
		return render_template("index.html")


# print(display_names)

@app.route("/home", methods=["GET", "POST"])
def home():

	if request.method == "POST":
		return render_template("home.html")

	else:
		return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():

	if request.method == "POST":
		new_channel = request.form.get("new_channel")
		existing_channel = request.form.get("existing_channel")

		if new_channel != None:
			data = {name: new_channel}
			channels.append(data)
			return render_template("chat.html", channel = new_channel)

		else:
			return render_template("chat.html", channel = existing_channel)

	else:
		return render_template("home.html")




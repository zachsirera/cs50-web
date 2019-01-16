import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketIO = SocketIO(app)

<<<<<<< HEAD
# Create empty lists needed for data handling
display_names = []
channels = []
=======
display_names = []
>>>>>>> f985de0b0521d9ee0be9d25c559887ae76e1c9f2

@app.route("/", methods=["GET", "POST"])
def index():

	if request.method == "POST":

<<<<<<< HEAD
		global display_names

		print(dict(request.form))

=======
>>>>>>> f985de0b0521d9ee0be9d25c559887ae76e1c9f2
		# Need to check local storage and see if the user already has a display name associated with them, and if so, log them in automatically
		# Else:

		# Get the users chosen display name from form
		display_name = request.form.get("display_name")
<<<<<<< HEAD
		print("This is ", display_name)

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
		return render_template("index.html", names = display_names)


# print(display_names)

@app.route("/home", methods=["GET", "POST"])
def home():

	if request.method == "POST":
		return render_template("home.html")

	else:
		return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():

	global channels

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

@app.route("/direct_message", methods=["GET", "POST"])
def dm():

	if request.method == "POST":

		return render_template("dm.html")

	else:
		return render_template("users.html")

@app.route("/users", methods=["GET"])
def users():

	return render_template("users.html", users = display_names)

@app.route("/test", methods=["POST", "GET"])
def test():

	if request.method == "POST":
		test = request.form.get("test")

		return render_template("test.html", test = test)

	else:
		return render_template("test.html")

if __name__ == '__main__':
    socketIO.run(app)

=======

		# Verify that the user's name is available
		if display_name in display_names:
			error = "This username is not available"
			return render_template("error.html", Error = error)

		# The username is available
		display_names.append(display_name)

		# Redirect user to a list of all channels or the option to select a chat channel. 

		# If user submits name of new channel, verify that it is available.

		# If channel name is unavailable, ask the user if they would like to join that channel or if they would like to submit another name. 

		redirect(url_for("home.html"))



	else:
		return render_template("index.html")
>>>>>>> f985de0b0521d9ee0be9d25c559887ae76e1c9f2

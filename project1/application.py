import os
import requests
import psycopg2

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import test


app = Flask(__name__)

# Extract database credentials from private file
with open("dbparams.txt", "r") as file:
    data = file.readlines()

    params = []
    for line in data:
        words = line.split()
        params.append(words)

    mykey1 = str(params[0])
    mykey = mykey1[2:-2]

    host1 = str(params[1])
    host = host1[2:-2]

    database1 = str(params[2])
    database = database1[2:-2]

    user1 = str(params[3])
    user = user1[2:-2]

    password1 = str(params[4])
    password = password1[2:-2]

    url1 = str(params[5])
    url = url1[2:-2]

# Close dbparams.txt
file.close()

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine(url)
db = scoped_session(sessionmaker(bind=engine))

# Establish connection to PostgreSQL database
try:
	conn = psycopg2.connect(f"host={host} dbname={database} user={user} password={password}")
except:
	print("Database connection not made")

# Establish a cursor to navigate the database
cursor = conn.cursor()



@app.route("/", methods=["GET", "POST"])
def index():
    """ Render the index home page. """
    if request.method == "GET":

        return render_template('index.html')

    else:
        # user_id = session["user_id"]
        return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log a user in, if registered. """

    # Forget any user session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Please enter a username"
            return render_template("error.html", Error = error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "Please enter a password"
            return render_template("error.html", Error = error)

        # User has submitted all necessary forms.    
        else: 
            username = request.form.get("username")
            password = request.form.get("password")
            hashed = generate_password_hash(password)

            # Check that the user-submitted data is present in users database
            cursor.execute("SELECT hash FROM users WHERE username = %s", (username,))
            row = cursor.fetchall()
            if cursor.rowcount != 1:
                error = "You have not entered a valid username."
                return render_template("error.html", Error = error)
            else:
                # User has entered a valid username. Verify their password.
                if not check_password_hash(row[0][0], password):
                    error = "Your username and password do not match our records."
                    return render_template("error.html", Error = error)

                else:
                    # The user has submitted a valid username and the corresponding password. Log them in. 
                    # Remember which user has logged in
                    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    row = cursor.fetchall()
                    session['user_id'] = row[0][0]

                    # Redirect user to search page
                    return redirect("/search")
                    
    else:
        return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register(): 
    """ Register users in the users database """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Please enter a username"
            return render_template("error.html", Error = error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "Please enter a password"
            return render_template("error.html", Error = error)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            error = "Please confirm your password"
            return render_template("error.html", Error = error)

        # Validate password
        if request.form.get("password") != request.form.get("confirmation"):
            error = "Your passwords do not match."
            return render_template("error.html", Error = error)

        else:
            # Set parameters from html form
            username = str(request.form.get("username"))
            password = str(generate_password_hash(request.form.get("password")))

            # Ensure that username is available
            rows = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.rowcount != 0:
                error = "This username is not available"
                return render_template("error.html", Error = error)

            else:
                # If the username is available, store in database
                cursor.execute("INSERT INTO users (username, hash) VALUES (%s, %s)", (username, password))
                # Commit changes to database
                conn.commit()

                # Once user is successfully registered, log them in and redirect them to index page.
                row = cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                session['user_id'] = row[0][0]
                return redirect("/search")

    else: 
        return render_template('register.html')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """ Log the user out of the current session """
    # Clear the user session
    session.clear()

    # Redirect user to home page
    return redirect("/login")

@app.route("/search", methods=["GET", "POST"])
def search():
    """ Allow the user to search the database """
    if request.method == "POST":
        # Confirm that the user has submitted a valid search string in the form
        if not request.form.get("user_search"):
            error = "Please enter a valid search text"
            return render_template("error.html", Error = error)
        else:
            user_search = request.form.get("user_search")

            # Make a specific query for purely numeric searches - isbn only
            if user_search.isnumeric():
                cursor.execute("SELECT * FROM books where isbn = %s", (user_search,))
                rows = cursor.fetchall()
                if cursor.rowcount == 0:
                    error = "Your search yielded no results"
                    return render_template("error.html", Error = error)
                else:
                    number = cursor.rowcount
                    return render_template("list.html", Books = rows, Number = number)
            else:
                # if not numeric search titles and authors
                cursor.execute("SELECT * FROM books WHERE title LIKE '%%' || %s || '%%' OR author LIKE '%%' || %s || '%%'", (user_search, user_search))
                rows = cursor.fetchall()
                if cursor.rowcount == 0:
                    error = "Your search yielded no results"
                    return render_template("error.html", Error = error)
                else:
                    number = cursor.rowcount
                    return render_template("list.html", Books = rows, Number = number)

    else:
        return render_template('search.html')

@app.route("/book/<isbn>", methods = ["GET", "POST"])
def book(isbn):
    """ Return information about the selected book """

    user_id = session.get('user_id')


    # Fetch necessary book information from books db
    cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
    rows = cursor.fetchall()

    title = rows[0][1]
    author = rows[0][2]
    year = rows[0][3]

    # Fetch necessary review information from goodreads
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": mykey, "isbns": isbn })
    reviews = res.json()

    reviews_count = reviews['books'][0]['reviews_count']
    average_rating = reviews['books'][0]['average_rating']

    # Fetch necessary review information from reviews db
    cursor.execute("SELECT * FROM reviews WHERE isbn = %s AND user_id = %s", (isbn, user_id))
    results = cursor.fetchall()

    # Determine if a user has submitted a review for this book yet. 
    if cursor.rowcount == 0:
        review_made = False
        return render_template("book.html", isbn = isbn, author = author, title = title, year = year, review_made = review_made, reviews_count = reviews_count, average_rating = average_rating)

    else:
        review = results[0][3]
        rating = results[0][2]
        review_made = True  
        return render_template("book.html", isbn = isbn, author = author, title = title, year = year, rating = rating, review = review, review_made = review_made, reviews_count = reviews_count, average_rating = average_rating)



@app.route("/review/<isbn>", methods=["POST"])
def review(isbn):
    """ Allow user to submit their own reivew to reviews database """

    user_id = session.get('user_id')

    # Verify that the user has submitted the necessary forms
    if not request.form.get("user_rating"):
        error = "Please select a rating for this book"
        return render_template("error.html", Error = error)
    else:
        if not request.form.get("user_review"):
            error = "Please submit a reivew"
            return render_template("error.html", Error = error)
        else:
            # User has submitted all necessary forms
            rating = request.form.get("user_rating")
            review = request.form.get("user_review")

            # Add these to the reviews database
            cursor.execute("INSERT INTO reviews (user_id, rating, review, isbn) VALUES (%s, %s, %s, %s)", (user_id, rating, review, isbn))
            conn.commit() 

            # On successful insertion into the database, bring user back to book
            cursor.execute("SELECT * FROM reviews WHERE user_id = %s AND isbn = %s", (user_id, isbn))
            rows = cursor.fetchall
            if cursor.rowcount != 0:
                review_submitted = True
                return redirect(url_for('book', isbn = isbn, review_submitted = review_submitted))
            else:
                error = "There was a problem submitting your review to the database. Please try again later."
                return render_template("error.html", Error = error)







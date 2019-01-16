import csv
import psycopg2

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

# Close dbparams.txt
file.close()

# Establish connection to PostgreSQL database
try:
	conn = psycopg2.connect(f"host={host} dbname={database} user={user} password={password}")
except:
	print("Database connection not made")

# Establish a cursor to navigate the database
cur = conn.cursor()

# Create books table
try:
	cur.execute("""CREATE TABLE books(
	    isbn text PRIMARY KEY,
	    title text,
	    author text,
	    year integer
	)
	""")
	conn.commit()
except:
	print("'books' table already exists")

# Read books.csv row by row and write to PostgreSQL database
with open('books.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	# Skip first row which contains only header data
	next(reader)
	for row in reader:
		cur.execute("INSERT INTO books VALUES (%s, %s, %s, %s)", row)

# Commit data
conn.commit()







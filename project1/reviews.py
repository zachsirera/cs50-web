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

print(host)
print(database)
print(user)
print(password)

# Establish connection to PostgreSQL database
try:
	conn = psycopg2.connect(f"host={host} dbname={database} user={user} password={password}")
	# Establish a cursor to navigate the database
	cur = conn.cursor()
except:
	print("Database connection not made")



# Create reviewss table
# try:
cur.execute("""CREATE TABLE reviews(
    user_id int PRIMARY KEY,
    isbn text REFERENCES books(isbn),
    rating int,
    review text
	)
	""")
conn.commit()
# except:
	# print("'reviews' table already exists")
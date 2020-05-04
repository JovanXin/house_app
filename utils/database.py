from .database_connection import DatabaseConnection

"""
Storing and retrieving books from a database
"""


def create_house_table():
	with DatabaseConnection("data.db") as connection:
		cursor = connection.cursor()

		cursor.execute('''
			CREATE TABLE IF NOT EXISTS houses(
				house_name text primary key,
				price integer,
				owner text,
				email text,
				location text,
				beds integer,
				bathrooms integer,
				outside_area integer,
				inside_area integer,
				description text
				)''') 



def add_house(house_name,price,owner,email,location,beds,bathrooms,outside_area,inside_area,description):
		with DatabaseConnection("data.db") as connection:	
			cursor = connection.cursor()

			cursor.execute('INSERT INTO houses VALUES(?,?,?,?,?,?,?,?,?,?)',(house_name,price,owner,email,location,beds,bathrooms,outside_area,inside_area,description))



def get_all_houses():
	with DatabaseConnection("data.db") as connection:
		cursor = connection.cursor()
		cursor.execute('DROP VIEW IF EXISTS showHouses')
		cursor.execute('''CREATE VIEW showHouses AS SELECT house_name,price,location,outside_area,inside_area FROM houses''')
		cursor.execute('SELECT * FROM showHouses')

		return [row for row in cursor.fetchall()]



def get_house_info(house_name):
	with DatabaseConnection("data.db") as connection:
		cursor = connection.cursor()
		cursor.execute('DROP VIEW IF EXISTS showHouses')
		cursor.execute('''CREATE VIEW showHouses AS SELECT house_name,price,owner,email,location,beds,bathrooms,outside_area,inside_area,description FROM houses''')
		cursor.execute('SELECT * FROM showHouses WHERE house_name=?',(house_name,))
		return [row for row in cursor.fetchall()]


def delete_house(house_name):
	with DatabaseConnection("data.db") as connection:
		cursor = connection.cursor()
		cursor.execute('DELETE FROM houses WHERE house_name=?', (house_name,)) #not sure if this works


# def fetch_password():
# 	name = input("Enter listing(house) name to fetch from:")
#     	with DatabaseConnection("data.db") as connection:
# 		    cursor = connection.cursor()
# 		    cursor.execute('SELECT * FROM houses WHERE house_name=?',(house_name,))
# 		    return [row for row in cursor.fetchall()]


# def validate_password():
#   house_data = fetch_password()
#   for house in house_data:
#     password = data[1]
#     if bcrypt.checkpw((input("enter your password").encode("utf-8")), password):
#       return True
#     else:
#       return False
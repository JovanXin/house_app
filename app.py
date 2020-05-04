"""
A application that allows users to see avaliable houses, and add their own listings. 
SQLite3

To-Learn:
Authentication and security
Hosting databases
Email-sending -> purchase house -> inform buyer/seller
Purchase'd house -> stripe payment (probably not yet, too advanced)

"""


from utils import database
from collections import namedtuple
import textwrap
from utils.classemail import Email


USER_CHOICE = """
Enter:
-'a' to add a new house
-'l' to list avaliable houses
-'s' to show specific house
-'p' to contact the seller of a house 
-'d' to delete a house listing
-'r' to report a listing
-'q' to quit

Your choice:"""

HOUSE_TEMPLATE = """
LISTING NAME:
{house_name}

CONTACT INFORMATION:
House Owner: {owner}
Contact Email: {email}

ABOUT HOUSE:
PRICE: {price}
Location: {location}
Beds: {beds}
Bathrooms: {bathrooms}
Outside Area: {outside_area}
Inside Area: {inside_area}
Description: {description}"""


House = namedtuple("House","house_name price owner email location beds bathrooms outside_area inside_area description")
ListHouse = namedtuple("ListHouse","house_name price location outside_area inside_area")
def menu():
	database.create_house_table()
	while True:
		user_input = input(USER_CHOICE)
		if user_input == "q":
			break
		elif user_input == "a":
			prompt_add_house()
		elif user_input == "l":
			list_houses()
		elif user_input == "p":
			contact_seller()
		elif user_input == "r":
			prompt_report_house()
		elif user_input == "d":
			prompt_delete_house()
		elif user_input == "s":
			prompt_show_house()
		else:
			print("Unknown command, please try again\n")


def prompt_add_house():
	house_name = input("Enter listing name:")
    # hashed_password = bcrypt.hashpw(input("Enter password to access the information:").encode("utf-8"), bcrypt.gensalt())
	price = input("How much do you want to sell the house for?:")
	owner = input("Enter house owner:")
	email = input("Enter email you'd like to be contacted:")
	location = input("Enter location of house:")
	beds = input("Enter number of beds:")
	bathrooms = input("Enter number of bathrooms:")
	outside_area = input("Enter outside area, in meters squared:")
	inside_area = input("Enter inside area, in meters squared:")
	description = input("Describe the house:")

	database.add_house(house_name,price,owner,email,location,beds,bathrooms,outside_area,inside_area,description)


#Lists out simple information for each house
def list_houses():
	houses = database.get_all_houses()
	for house in houses:
		house = ListHouse(*house)
		print(f"{house.house_name}\n${house.price} house in {house.location}, area:{int(house.inside_area) + int(house.outside_area)}\n")


#Emails seller from classemail
def contact_seller():
	house_name = input("Which house are you interested in?:")
	subject = input("Type email subject:")
	price = int(input("How much would you be willing to pay for?:")) #could check against houses table to see if greater than asking price
	message = input("What message would you like to send to the owner?:")
	buyer_name = input("What is your name?:")

	house_data = fetch_database_info(house_name)
	seller_email = house_data.email
	owner = house_data.owner

	if house_data.price <= price:

		contact = Email(house_name=house_name,price=price,subject=subject,message=message,buyer_name=buyer_name,owner=owner,seller_email=seller_email)
		contact.main("contact owner")
	else:
		print("Sorry, the price you are willing to pay is below the asking value of the owner.")


#Shows detailed information for a specific house in a template
def prompt_show_house():
	house_name = input("Please enter the name of the house you'd like to see more about:")
	house_data = fetch_database_info(house_name)
	print(HOUSE_TEMPLATE.format(**house_data._asdict()))


#Prevents the need to fetch database in each individual function
def fetch_database_info(house_name):
	houses = database.get_house_info(house_name)
	for house in houses:
		house = House(*house)
		return house


#Emails support for any listing issues
def prompt_report_house():
	house_name = input("Enter which house 'name' you'd like to report:")
	reason = input("Enter why you'd like to report this house:")
	seller_email = fetch_database_info(house_name).email
	report = Email(house_name=house_name,reason=reason,seller_email=seller_email)
	report.main("report")


#Deletes a house listing
def prompt_delete_house():
	house_name = input("Enter which house you'd like to remove as a listing:")
	database.delete_house(house_name)



if __name__ == '__main__':
	menu()
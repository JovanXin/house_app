import smtplib, ssl

from string import Template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

HOST_ADDRESS = "smtp.gmail.com"
SSL_PORT = 465
TLS_PORT = 587



def create_message(FILENAME):
	message_template = read_template(FILENAME)



def send_message():
	msg.attach(MIMEText(message, 'plain'))

	#user authentication
	EMAIL = input("Login with email:")
	PASSWORD = input("Type your password:")

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", SSL_PORT, context=context) as server:
	# s.starttls()
		server.login(USER_EMAIL,USER_PASSWORD)

		#setup the message

		print(message) #just so we can debug
		server.sendmail(MY_ADDRESS,seller_email,msg.as_string())	


def read_template(FILENAME):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(FILENAME,"r") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def contact_house_owner(self,house_name,price,subject,message,buyer_name,buyer_email,owner,seller_email):
	message_template = read_template("messages/contact_owner.txt")
	message = message_template.substitute(
		PERSON_NAME=owner.title(),
		MESSAGE_CONTENT=message,
		BUYER_NAME=buyer_name,
		PRICE=price,
		BUYER_EMAIL=buyer_email)

	msg = MIMEMultipart()

	if subject:
		msg["Subject"] = subject
	else:
		msg["Subject"] = DEFAULT_SUBJECT	

	msg["From"] = USER_EMAIL
	msg["To"] = buyer_email



def main(option):
	if option == "contact owner":
		contact_house_owner()


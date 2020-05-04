import smtplib, ssl

from string import Template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

HOST_ADDRESS = "smtp.gmail.com"
SSL_PORT = 465
TLS_PORT = 587

FILENAME = "utils/message.txt"



def notify_purchase(house_name,price,subject,message,buyer_name,buyer_email,owner,seller_email):

	EMAIL = input("Login with email:")
	PASSWORD = input("Type your password:")

	message_template = read_template(FILENAME)
	msg = MIMEMultipart()

	message = message_template.substitute(
		PERSON_NAME=owner.title(),
		MESSAGE_CONTENT=message,
		BUYER_NAME=buyer_name,
		PRICE=price,
		BUYER_EMAIL=buyer_email)

	if subject:
		msg["Subject"] = subject
	else:
		msg["Subject"] = "Someone is interested in your house!"	
	msg["From"] = USER_EMAIL
	msg["To"] = buyer_email
	#start the server
	msg.attach(MIMEText(message, 'plain'))

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


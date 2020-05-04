import smtplib, ssl
from string import Template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
	def __init__(self,house_name,price,subject,message,buyer_name,buyer_email,owner,seller_email):
		self.house_name = house_name
		self.price = price
		self.subject = subject
		self.message = message
		self.buyer_name = buyer_name
		self.buyer_email = buyer_email
		self.owner = owner
		self.SELLER_EMAIL = seller_email
		self.HOST_ADDRESS = "smtp.gmail.com"
		self.SSL_PORT = 465
		self.USER_EMAIL = input("Enter your email:")
		self.USER_PASSWORD = input("Enter your password:")
		self.DEFAULT_SUBJECT = "Someone is interested in your house!"
		self.FILENAME = "utils/messages/contact_owner.txt"

	def read_template(self):
	    """
	    Returns a Template object comprising the contents of the 
	    file specified by filename.
	    """
	    with open(self.FILENAME,"r") as template_file:
	        self.message_template = Template(template_file.read())
	    return self.message_template


	def send_message(self,action):

		self.msg = MIMEMultipart()
		self.message_template = self.read_template()

		action()

		self.msg.attach(MIMEText(self.message, 'plain'))

		self.context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self.HOST_ADDRESS, self.SSL_PORT, context=self.context) as self.server:
			self.server.login(self.USER_EMAIL,self.USER_PASSWORD)

			#setup the message

			print(self.message) #just so we can debug
			self.server.sendmail(self.USER_EMAIL,self.SELLER_EMAIL,self.msg.as_string())


	def contact_house_owner(self):
		self.message = self.message_template.substitute(
			PERSON_NAME=self.owner.title(),
			MESSAGE_CONTENT=self.message,
			BUYER_NAME=self.buyer_name,
			PRICE=self.price,
			BUYER_EMAIL=self.buyer_email)


		if self.subject:
			self.msg["Subject"] = self.subject
		else:
			self.msg["Subject"] = self.DEFAULT_SUBJECT	

		self.msg["From"] = self.USER_EMAIL
		self.msg["To"] = self.buyer_email



	def contact_house_owner(self):
		self.send_message(self.contact_house_owner)




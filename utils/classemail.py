import smtplib, ssl
from string import Template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


USER_EMAIL = input("""
	LOGIN WITH GOOGLE ACCOUNT - You need to allow access from 'less secure' apps. (This lets you send emails)
	Enter your email:""") 
USER_PASSWORD = input("""
	Enter your password:""")
SUPPORT_EMAIL = "jovan3.1415926@gmail.com"

class Email:
	def __init__(self,house_name=None,reason=None,price=None,subject=None,message=None,buyer_name=None,owner=None,seller_email=None):
		self.house_name = house_name
		self.reason = reason
		self.price = price
		self.subject = subject
		self.message = message
		self.buyer_name = buyer_name
		self.owner = owner
		self.seller_email = seller_email
		self.HOST_ADDRESS = "smtp.gmail.com"
		self.SSL_PORT = 465
		self.DEFAULT_SUBJECT = "Someone is interested in your house!"

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

		if self.subject:
			self.msg["Subject"] = self.subject
		else:
			self.msg["Subject"] = self.DEFAULT_SUBJECT	

		self.msg["From"] = USER_EMAIL
		if self.seller_email:
			self.msg["To"] = self.seller_email
		else:
			self.msg["To"] = SUPPORT_EMAIL

		self.msg.attach(MIMEText(self.message, 'plain'))

		self.context = ssl.create_default_context()
		with smtplib.SMTP_SSL(self.HOST_ADDRESS, self.SSL_PORT, context=self.context) as server:
			server.login(USER_EMAIL,USER_PASSWORD)

			#setup the message

			print(self.message) #just so we can debug
			server.sendmail(USER_EMAIL,self.seller_email,self.msg.as_string())


	def contact_house_owner(self):
		self.message = self.message_template.substitute(
			PERSON_NAME=self.owner.title(),
			MESSAGE_CONTENT=self.message,
			BUYER_NAME=self.buyer_name,
			PRICE=self.price,
			BUYER_EMAIL=USER_EMAIL)


	def report_listing(self):
		self.message = self.message_template.substitute(
			REPORTED_LISTING_NAME=self.house_name,
			REASON=self.reason)


	def main(self,option):
		if option == "contact owner":
			self.FILENAME = "utils/messages/contact_owner.txt"
			self.send_message(self.contact_house_owner)
		elif option == "report":
			self.FILENAME = "utils/messages/report_listing.txt"
			self.send_message(self.report_listing)






from cowin_api import CoWinAPI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, datetime
from bs4 import BeautifulSoup #To install: pip3 install beautifulsoup4
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, datetime
from bs4 import BeautifulSoup #To install: pip3 install beautifulsoup4


email_sender_account = "pavred10@gmail.com" 
email_sender_username = "pavred10@gmail.com"  #your email username
email_sender_password = "pavan8123565021"#your email password
email_smtp_server = "smtp.gmail.com" #change if not gmail.
email_smtp_port = 587 #change if needed.
email_recepients = ["pavred10@gmail.com"] #your receipts  #pavred08@gmail.com

def SendEmail (vaccine_text,entire_text,time):
	email_subject = f"Vaccine available. {vaccine_text}"
	email_body = '<html><head></head><body>'
	email_body += '<style type="text/css"></style>' 
	email_body += f'<h2> Vaccine Availability info: {time}</h2>' 

	email_body += f'<h2 style="color: rgb(9, 179, 23);">' 
	email_body += f'<b> {vaccine_text}</b> </h2>' 

	email_body += f'<h2 style="color: rgb(9, 179, 23);">' 
	email_body += f'<b> {entire_text}</b> </h2>' 

 
	server = smtplib.SMTP(email_smtp_server,email_smtp_port) 
	print(f"Logging in to {email_sender_account}")
	server.starttls() 
	server.login(email_sender_username, email_sender_password)
	for recipient in email_recepients:
		print(f"Sending email to {recipient}")
		message = MIMEMultipart('alternative') 
		message['From'] = email_sender_account 
		message['To'] = recipient 
		message['Subject'] = email_subject 
		message.attach(MIMEText(email_body, 'html')) 
		server.sendmail(email_sender_account,recipient,message.as_string())
	server.quit()
	print ("Email Sent")


# district_id = '294'
# date = '12-05-2021'  # Optional. Takes today's date by default
# min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

district_ids=["294"] #294  #74
dates= ["12-05-2021"]
min_age_limits= [18] #18

cowin = CoWinAPI()

count_api_calls=0

while True:
	try:
		overall_flag=False
		for district_id, date, min_age_limit in zip(district_ids,dates,min_age_limits):
			
			available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
			# print(available_centers)
			l=[]
			centers=available_centers['centers']
			# print (centers)
			# vaccine_avail_centres={}
			for each_center in centers:
				flag=False
				name= each_center["name"]
				district= each_center["district_name"]
				sessions= each_center["sessions"]
				# print ("Name:",name)
				# vaccine_avail_centres
				available_dates=[]
				for each_session in sessions:
					session_date= each_session["date"]
					session_available_cap= each_session["available_capacity"]
					session_min_age= each_session["min_age_limit"]
					session_vaccine_type= each_session["vaccine"]
					session_slot= each_session["slots"]

					# print ("Name:",name,",  Available:",session_available_cap, ",  Age:",session_min_age, "Slots:",session_slot)
					# print ("type:",type(session_available_cap))
					# if session_available_cap>0 or session_min_age==18:  # to test email
					if session_available_cap>0:
						available_dates.append(session_date)
						flag=True
						overall_flag=True
						# vaccine_text= "Name:"+name+",  Available:"+str(session_available_cap)+",   Age:"+str(session_min_age)+ ",   Slots:"+str(session_slot)
				if flag:
					vaccine_text= "Name:"+name + ",   Available Dates:"+ str(available_dates)
					entire_text = str(each_center)
					SendEmail(vaccine_text, entire_text,time=str(datetime.datetime.now()))

		if overall_flag:			
			time.sleep(60)
		else:
			# time.sleep(2)
			time.sleep(1)
		count_api_calls+=1
		print("Count:",count_api_calls)
	except Exception as e:
		print ("Sleeping cuz api problem. ",e)
		time.sleep(120)
		
	

	


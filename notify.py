from api_functions import Api
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
    
my_email, password = 'myemail@gmail.com', 'gmail app password'
out_email = "recipent@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"], message["From"], message["To"] = "NBA GAMES PLAYED TODAY", my_email, out_email

nba = Api()
html = nba.output()

html_email = MIMEText(html, "html")
message.attach(html_email)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(my_email, password)
    server.sendmail(
        my_email, out_email, message.as_string()
    )

    cleaned up functions and added email sender

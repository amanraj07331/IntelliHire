import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

class EmailService:
    def __init__(self):
        # Load configuration from config.json
        with open('config.json') as config_file:
            self.config = json.load(config_file)


    def send_otp(self, email, otp):
        msg = MIMEMultipart()
        msg["Subject"] = self.config["email_subject"] #subject
        msg["From"] = self.config["hr_email"] #hr email
        msg["To"] = email
        text = f"Hi, your otp is : {otp}" #message with otp
        part = MIMEText(text, "plain")
        msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.config["hr_email"], self.config["hr_password"])
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
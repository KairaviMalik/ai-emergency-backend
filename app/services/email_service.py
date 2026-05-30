import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body):
    try:
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            raise Exception("Email credentials missing in .env")

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # IMPORTANT FIX: explicit IPv4 + timeout
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender_email, sender_password)
        server.send_message(msg)

        server.quit()

        print("Email sent successfully to", to_email)

    except Exception as e:
        print("EMAIL ERROR:", str(e))
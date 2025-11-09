# https://python.plainenglish.io/5-beginner-python-projects-that-actually-teach-you-how-to-think-like-a-coder-a2f4e102b8b3
import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):
    msg = EmailMessage()
    msg['From'] = "ronald.montgomery@gmail.com"
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("ronald.montgomery@gmail.com", "your mom")
        smtp.send_message(msg)

send_email("ronald.montgomery@gmail.com", "Automation Test", "This is an automated message.")
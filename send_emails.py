import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv   ### pip install python-dotenv

### you have to use post according to your email_server
PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

### Load the envirnoment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

### Read envirnoment varibales
sender_email = os.getenv("EMAIL")
sender_password = os.getenv("PASSWORD")


def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    ### Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Coding Is Fun Corp.", f"{send_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = send_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        I just wanted to drop you a quick note to remind you that {amount} USD in respect of our invoice {invoice_no} is due for payment on {due_date}.
        I would be really greateful if you could confirm that everything is on track for payment.
        Best regards
        Muhammad
        """
    )
    ### Add the html version. This convert the message into multipart/alternative.
    ### container, with the original text message as the first part and the new html
    ### message as the second part.
    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hi {name},</p>
        <p>I hope you are well.</p>
        <p>I just wanted to drop you a quick note to remind you that <strong>{amount}</strong> USD in respect of our invoice <strong>{invoice_no}</strong> is due for payment on <strong>{due_date}</strong>.</p>
        <p>I would be really greateful if you could confirm that everything is on track for payment.</p>
        <p>Best regards</p>
        <p>Muhammad</p>
      </body>
    </html>
    """,
        subtype = "html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    
if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Muhammad",
        receiver_email="your email",
        due_date="05, May 2024",
        invoice_no="INV-21-21",
        amount="5",
    )

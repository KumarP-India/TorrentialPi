import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import os

def send_email(log_files, subject="Log Files", email_body="The requested log files are attached."):

    # Read settings from settings.json

    with open('../Settings.json') as f:

        settings = json.load(f)

    sender_address = settings['Email to send']
    sender_password = settings['Email to send password']
    recipient = settings['Email to receive']

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = recipient
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(email_body, 'plain'))

    # Attach files to the email
    for file in log_files:
        try:
            attachment = open(file, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(file))
            message.attach(p)
        except Exception as e:
            print(f"Error attaching file {file}: {str(e)}")

    # Create SMTP session
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Add correct SMTP server and port
        server.starttls()
        server.login(message['From'], sender_password)
        text = message.as_string()
        server.sendmail(message['From'], recipient, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


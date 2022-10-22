# libraries to be imported
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
#from re import sub
import ssl
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")
email_cc = os.getenv("EMAIL_CC")
env_file_path = os.getenv("FILE_PATH")


class Email():
    def __init__(self):
        pass

    def send(self, message=None):
        print('Sending email...')
        try:
            subject = 'Email Automation with Python'
            body = "\n".join([f"""
            Hello {email_receiver}
            This is a test email, send from python script to automate the process.   
            """, message])

            em = EmailMessage()
            em['From'] = 'Contact <{sender}>'.format(sender=email_sender)
            em['To'] = email_receiver
            em['CC'] = email_cc
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
                smpt.login(email_sender, email_password)
                smpt.sendmail(email_sender, email_receiver.split(
                    ";") + (email_cc.split(";") if email_cc else []), em.as_string())
                smpt.quit()
            print("Email was sent Successfully...")
        except Exception as ex:
            print(f'Exception Occured ! \n {ex}')

    def sendFile(self, file_path=None):
        print(f'Sending email with attachment...')
        if file_path is None:
            file_path = env_file_path
        file_ext = self.file_extension(file_path)
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 465
            subject = 'Email Attachment Automation with Python'
            em = MIMEMultipart('mixed')
            em['From'] = 'Contact <{sender}>'.format(sender=email_sender)
            em['To'] = email_receiver
            em['CC'] = 'sebastian_gvl@hotmail.com'
            em['subject'] = subject

            em_content = f'<h4>Hello {email_receiver},<br> This is a test email with attachment, send from python script to automate the process.</h4>\n'
            body = MIMEText(em_content, 'html')
            em.attach(body)

            with open(file_path, "rb") as attachment:
                p = MIMEApplication(attachment.read(), _subtype=file_ext)
                p.add_header(
                    'Content-Disposition', "attachment; filename= %s" % file_path.split("\\")[-1])
                em.attach(p)
                attachment.close()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smpt:
                smpt.ehlo()
                smpt.login(email_sender, email_password)
                smpt.sendmail(email_sender, email_receiver.split(
                    ";") + (email_cc.split(";") if email_cc else []), em.as_string())
                smpt.quit()

            print("Email was sent Successfully...")
        except Exception as ex:
            print(f'Exception Occured ! \n {ex}')

    def check_file(self, file_name):
        file_name = file_name.translate(
            {ord(i): None for i in '!#@{}[]<>=+£$%^&*()?|,;:/\\\'\"'})
        return file_name

    def file_extension(self, file_path):
        i = -1
        c = file_path[i]
        file_ext = ""
        while c != '.':
            file_ext = ''.join([c, file_ext])
            i = i - 1
            c = file_path[i]
        return file_ext

from project import email_handler

if __name__ == "__main__":
    email_handler = email_handler.Email()
    email_handler.send("Congratulations, this email was sent successfully!!!")

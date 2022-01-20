import pandas as pd
import smtplib, ssl
from pretty_html_table import build_table
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



#Import secret information from local file (not in github)
from dotenv import load_dotenv
import os
load_dotenv()



#Create CSV function
def create_csv(df,path):
    df.to_csv(path, index=False)
    return ("CSV created properly")

#Create html function
def create_html(df):
    output = build_table(df, 'blue_light')
    with open('nearest_bicimad_station.html', 'w') as f:
        f.write(output)
    return ('html created properly')


#Send email function, importing the secret information from env file
def send_email(secret_number):
    sender_email = os.getenv('sender_email')
    password = os.getenv('password_sender')
    admin_email=os.getenv('admin_email')
    print('\n')
    receiver_email = input("Please, enter your email: ")

    if admin_email==receiver_email: #We double check that the user has entered the email from the admin
        print('\n')

        message = MIMEMultipart("alternative")
        message["Subject"] = 'Verification Code - Admin_role'
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\

        Hi!

        Your verification code is {secret_number}. 

        Enter this code in our application to verify your admin role.


        The Ironhack team

        """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            return (print ("Email sent successfully!"))
        except Exception as ex:
            return (print ("Something went wrong….Try it again",ex))
    
    else:
        return(1)



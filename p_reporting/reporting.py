import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Create CSV function
def create_csv(df,path):
    df.to_csv(path, index=False)
    return print("CSV created properly")


def create_html(df):
    html = df.to_html()
    
    # write html to file
    text_file = open("nearest_bicimad_station.html", "w")
    text_file.write(html)
    text_file.close()
    return ('html created properly')



def send_email(secret_number):
    sender_email = "iv.repilado@gmail.com"
    password = input("Type your password and press enter: ")
    print('\n')
    receiver_email = input("Please, enter your email: ")
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




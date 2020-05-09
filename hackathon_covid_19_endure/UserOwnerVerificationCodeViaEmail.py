# this class is used to generate and send OTP to email and update OTP in the Database.

import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generateOTP():
    digits = "0123456789"
    code = ""
    for i in range(6):
        code += digits[math.floor(random.random() * 10)]

    print('Generated code:', code)
    return code


def content(otp):
    message = f"""Here is your verification code for Endure signup.

        Code: {str(otp)}
        
        Please enter the verification code and login to your account. Hope you have a pleasant time in Endure.
        
        Ignore this message if this action was not performed by you.
        
        Regards,
        Team Endure.
        Have a good day ahead."""

    return message


def sendMail(myDB, myCursor, of, email):
    """
    :param of: 'user' or 'owner'
    """

    otp = generateOTP()
    try:
        senderEmail = "samplehackathonx@gmail.com"
        receiverEmail = email

        message = MIMEMultipart()
        message["From"] = senderEmail
        message["To"] = receiverEmail
        message["Subject"] = 'Verification Code for Endure'

        # Add body to email
        body = content(otp)
        message.attach(MIMEText(body, "plain"))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()  # start TLS for security
        s.login(senderEmail, "")

        print('sending message')
        text = message.as_string()
        print('sending notification message')
        s.sendmail(senderEmail, email, text)
        s.quit()
        print('message sent')

        # update `otp` field in the receiver's account in database
        myCursor.execute(
            "UPDATE `batchdatabase`.`" + of + "` SET `otp` = '" + otp + "' WHERE(`email` = '" + email + "');"
        )

        print('before commit')
        myDB.commit()
        print('commit done')
        return True
    except BaseException as e:
        print('Error: ', str(e))
        return False

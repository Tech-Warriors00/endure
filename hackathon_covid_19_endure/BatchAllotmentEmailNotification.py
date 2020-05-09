# this class is used to send email notification to shopkeeper's when batch-allotment is done

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def content(day, batch, incomingTime, outgoingTime, name, shopId):
    message = f"""Hey {str(name)}! Here is your batch allotment details.

            Opening time: {str(incomingTime)}
            Closing time: {str(outgoingTime)}
            Day: {str(day)}

            Batch {str(batch)} has been alloted.
            Shop ID: {str(shopId)}
            
            Please be puntual with your shop opening and closing time. Reach out to us in case of any problem.

            Regards,
            Team Endure.
            Have a good day ahead."""

    return message


def sendMail(email, day, batch, incomingTime, outgoingTime, name, shopId):
    try:
        senderEmail = "samplehackathonx@gmail.com"
        receiverEmail = email

        message = MIMEMultipart()
        message["From"] = senderEmail
        message["To"] = receiverEmail
        message["Subject"] = 'Batch Allotted'

        # Add body to email
        body = content(day, batch, incomingTime, outgoingTime, name, shopId)
        message.attach(MIMEText(body, "plain"))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()  # start TLS for security
        s.login(senderEmail, "")

        text = message.as_string()
        print('sending notification message...')
        s.sendmail(senderEmail, email, text)
        s.quit()
        print('one message sent')
        return True
    except BaseException as e:
        print('Error: ', str(e))
        return False

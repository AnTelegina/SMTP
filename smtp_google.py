import smtplib
from email.message import EmailMessage
import imghdr

with open('conf.txt', 'r') as file:
    EMAIL_ADRRESS = file.readline()
    PASSWORD = file.readline()

"""msg = EmailMessage()
msg["Subject"] = "Check out..."
msg["From"] = EMAIL_ADRRESS
msg["To"] = EMAIL_ADRRESS
msg.set_content("Image atteched...")"""

subject = "Check out..."
body = 'Image attached'

msg = 'Subject: ' + subject + '\n\n' + body.format(subject, body)

with open('kitty.jpg', 'rb') as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name

#msg.add_attachment(file_data, maintype='image', subtype = file_type, filename = file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADRRESS, PASSWORD)
    smtp.send_message(msg)



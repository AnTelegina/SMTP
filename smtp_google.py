import smtplib

with open('conf.txt', 'r') as file:
    EMAIL_ADRRESS = file.readline()
    PASSWORD = file.readline()

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADRRESS, PASSWORD)

    subject = 'hello'
    body = 'goodbye'

    msg = f'Subject: {subject}\n\n{body}'

    smtp.sendmail("sweerlie@gmail.com", "sweerlie@gmail.com", msg)



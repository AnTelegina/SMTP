import socket
import ssl
import base64
import sys

with open("inf.txt", 'r') as information_file:
    USER_NAME = information_file.readline()
    PASSWORD = information_file.readline()

target = USER_NAME

user_name = USER_NAME
password =  PASSWORD

def request(socket, request):
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65535).decode()
    return recv_data


host_addr = 'smtp.yandex.ru'
port = 465


def read_msg():
    with open('msg.txt', 'rb') as file:
        return base64.b64encode(file.read()).decode()

def read_pict(filename):
    with open(filename, 'rb') as file:
        return base64.b64encode(file.read()).decode()


def create_head(user, target, subject, bound):
    head = ""
    head += f"From:{user}\n"
    head += f"To:{target}\n"
    head += f"Subject: =?utf-8?B?{base64.b64encode(subject.encode()).decode()}?=\n"
    head += "MIME-Version: 1.0\n"
    head += f'Content-Type: multipart/mixed; boundary="{bound}"\n'
    head += "\n"

    return head

def create_body(bound, attachments):
    body = ""
    body += f"--{bound}\n"
    body += "Content-Type: text/plain; "
    body += 'charset="UTF-8"\n'
    body += "Content-Transfer-Encoding: base64 " + '\n' + '\n'
    body += read_msg() + '\n'

    for attach in attachments:
        body += f"--{bound}\n"
        body += 'Content-Disposition: attachment; filename="' + attach + '"' \
                '\nContent-Transfer-Encoding: base64' \
                '\nContent-Type: image/png; name="icon.png"' + '\n' + '\n'
        body += read_pict(attach) + '\n'

    body += f"--{bound}--\n"
    body += '.' + '\n'

    return body

def create_message(user, target, subject, attachments):
    bound = "bound123456789"
    return create_head(user, target, subject, bound)+create_body(bound, attachments)

def parse_configs():
    user = ''
    targets = None
    passwd = ''
    subject = ''
    attachments = None

    with open('configs.txt', encoding='utf-8') as file:
        for line in file:
            if line.find("from:") == 0:
                user = line.split(' ')[1].strip()
            if line.find("to:") == 0:
                targets = line[4:].strip().split(' ')
            if line.find("password:") == 0:
                passwd = line.split(' ')[1].strip()
            if line.find("subject:") == 0:
                subject = line.split(' ')[1].strip()
            if line.find("attachments:") == 0:
                attachments = line[13:].strip().split(' ')
        if user == '' or targets is None or passwd == '':
            sys.exit(-1)


        return user, passwd, subject, targets, attachments

def send_letter(user, passwd, subject, targets, attachments):
    for t in targets:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host_addr, port))
            client = ssl.wrap_socket(client)
            client.recv(1024)
            request(client, 'ehlo Ivan')
            base64login = base64.b64encode(user.encode()).decode()
            base64password = base64.b64encode(passwd.encode()).decode()
            request(client, 'AUTH LOGIN')
            request(client, base64login)
            request(client, base64password)
            request(client, 'MAIL FROM: ' + user)
            request(client, "RCPT TO: " + t)
            request(client, 'DATA')
            request(client, create_message(user, t, subject, attachments))

def main():
    user, passwd, subject, targets, attachments = parse_configs()
    send_letter(user, passwd, subject, targets, attachments)

if __name__ == '__main__':
    main()
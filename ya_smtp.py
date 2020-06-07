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

def parse_file_configs():
    user = ''
    targets = None
    passwd = ''
    subject = ''
    attachments = None

    with open('configs.txt', encoding='utf-8') as config_file:
        for line in config_file:
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

parse_file_configs()
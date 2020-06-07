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


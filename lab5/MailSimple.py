import smtplib
import argparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_addr: str, filename: str):
    from_addr = 'stXXXXXX@student.spbu.ru'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Hello!"
    msg['From'] = from_addr
    msg['To'] = to_addr

    with open(filename, 'r') as file:
        data = file.read()

    ext = filename.split('.')[-1]
    if ext == "txt":
        body = MIMEText(data, 'plain')
    elif ext == "html":
        body = MIMEText(data, 'html')
    else:
        body = MIMEText("It's python", 'plain')

    msg.attach(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_addr, 'password')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple stmp client')
    parser.add_argument('to_addr', type=str, help='Destination address')
    parser.add_argument('filename', type=str, help='File name')
    args = parser.parse_args()
    send_email(args.to_addr, args.filename)


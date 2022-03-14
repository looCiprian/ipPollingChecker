import argparse
import requests
import os
from pynotifier import Notification

APITOKEN = "" # API Token from https://ipgeolocation.io/

parser = argparse.ArgumentParser(description='Ip Polling service')

IPS = []

def sendNotification(title, message, severity):
    Notification(
	title=title,
	description=message,
	#icon_path='/absolute/path/to/image/icon.png', # On Windows .ico is required, on Linux - .png
	duration=5,                                   # Duration in seconds
	urgency=severity).send()

def install():

    os.system("pip3 install py-notifier")
    try:
        open(os.path.expanduser('~') + "/.ips","x")
    except FileExistsError:
        print("[-] Configuration file already exists")

    print("Add expected IP inside " + os.path.expanduser('~') + "/.ips")
    print("""Add a cron job using crontab -e and the following line "*/5 * * * * XDG_RUNTIME_DIR=/run/user/$(id -u) python3 <script path.py>" """)
    return

def checkIfInstalled():
    return os.path.exists(os.path.expanduser('~') + "/.ips")

def run():
    with open(os.path.expanduser('~') + "/.ips") as f:
        lines = f.readlines()
        for line in lines:
            IPS.append(line.strip())

    print(IPS)

    result = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + APITOKEN)

    if result.status_code != 200:
        sendNotification("ERROR", "Cannot get the IP from api.ipgeolocation.io", 'critical')
        return 
    
    response = result.json()
    ip = response['ip']

    if ip not in IPS:
        sendNotification("WRONG IP", "Your current ip is not listed in the" + os.path.expanduser('~') + "/.ips" + " file\nYour current ip is " + ip, 'critical')
        
    print("Current ip " + ip)

def main():
    parser.add_argument("-install", help='Install service', action='store_true')
    args = parser.parse_args()

    if args.install:
        install()
        exit(0)

    if not checkIfInstalled():
        print("Run with -install option")
        exit(0)
        
    run()

if __name__ == "__main__":
    main()

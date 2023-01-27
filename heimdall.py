# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime 
import time
import json

SLEEP_TIME = 10
STALE_TIME = 30

message = Mail(
    from_email='<send-grid-authorized-sender>',
    to_emails='<receiver-email>',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')

#print(os.environ.get('SENDGRID_API_KEY'))

def sendMail():
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        rescode = response.status_code
        print(rescode)
    except Exception as e:
        print(e.message)

def getNodeData():
    with open('nodeData.json') as d:
        metrics = json.load(d)
    return metrics

while True:
    now = int(time.time())
    utc = datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc)
    #localtime = datetime.datetime.fromtimestamp(now)
    print(f"UTC-time: {utc:%d-%m-%Y %H:%M:%S}")
    #print(f"Local-time: {localtime:%d-%m-%Y %H:%M:%S}")
    metrics = getNodeData()

    try:
        for pools in metrics:
            if 'time' in pools:
                lastUpdateEpochTime = int(pools['time'])
                lastUpdateUtcTime = datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc)
                if now - lastUpdateEpochTime > STALE_TIME: 
                    print(f"Stagnant Data - LastUpdate (UTC): {lastUpdateUtcTime:%d-%m-%Y %H:%M:%S}")
                    #Send Email 
                    #Create Notify File with Email Dispatch Time (limit sending)   
    except Exception as e:
        print(e)
    time.sleep(SLEEP_TIME)
#sendMail()

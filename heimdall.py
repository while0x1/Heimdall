# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime 
import time
import json
import requests

SLEEP_TIME = 10
STALE_TIME = 30
REPEAT_EMAIL = 30
BLOCK_DIFF = 10

message = Mail(
    from_email='<send-grid-authorized-sender>',
    to_emails='<receiver-email>',
    subject='Cardano Node Alerts',
    html_content='<strong>Connection or Block Stagnant!</strong>')

#print(os.environ.get('SENDGRID_API_KEY'))

def sendMail():
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        rescode = response.status_code
        print(rescode)
    except Exception as e:
        print(e.message)
        
def getTip():
    try:
        r = requests.get("https://api.koios.rest/api/v0/tip")
        content = json.loads(r.content)
        if r.status_code != 200:
            r = requests.get("https://api.koios.rest/api/v0/tip")
            content = json.loads(r.content)
        return content            
    except Exception as e:
        print(e)

def getNodeData():
    try:
        with open('nodeData.json') as d:
            metrics = json.load(d)
        return metrics
    except Exception as e:
        print(e)

def getAlarmData():
    try:
        with open('alarmData.json') as d:
            alarmData = json.load(d)
        return alarmData
    except Exception as e:
        print(e)

while True:
    now = int(time.time())
    utc = datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc)
    #localtime = datetime.datetime.fromtimestamp(now)
    print('===================TIP=======================')
    print(f"Current time (UTC): {utc:%d-%m-%Y %H:%M:%S}")
    #print(f"Local-time: {localtime:%d-%m-%Y %H:%M:%S}")
    metrics = getNodeData()
    chainTipData = getTip()
    try:
        tipBlockNo = chainTipData[0]['block_no']
        tipBlockTime = chainTipData[0]['block_time']
        print(f"chainTip block: {tipBlockNo}")
        tipBlockTimeUTC = datetime.datetime.fromtimestamp(int(tipBlockTime), tz=datetime.timezone.utc)
        tipBlockTimeUTC = tipBlockTimeUTC.replace(tzinfo=None)
        print(f"chainTip last block time {tipBlockTimeUTC}")
    except Exception as e:
        print(e)
    try:
        for pools in metrics:
            #print(pools)
            if 'time' in pools:
                lastUpdateEpochTime = int(pools['time'])
                lastUpdateUtcTime = datetime.datetime.fromtimestamp(lastUpdateEpochTime, tz=datetime.timezone.utc)

                if now - lastUpdateEpochTime > STALE_TIME or tipBlockNo - pools['block'] > BLOCK_DIFF: 
                    print('===================ALARMS====================')
                    print(f"Stagnant Data for ({pools['id']}) - LastUpdate (UTC): {lastUpdateUtcTime:%d-%m-%Y %H:%M:%S}")
                    print(f"Chain Tip Block {tipBlockNo} Client {pools['id']} block {pools['block']}")
                    if tipBlockNo - pools['block'] > BLOCK_DIFF and now - lastUpdateEpochTime < STALE_TIME:
                            print('Updating but Block out of Sync')
                    alarmData = getAlarmData()
                    if any(d['id'] == pools["id"] for d in alarmData):
                        #In Alarm File already and Still STALE update 
                        for alarms in alarmData: 
                            if alarms["id"] == pools["id"]:
                                if 'lastAlarm' in alarms:
                                    lastAlarmOnFile = int(alarms["lastAlarm"])
                                    if now - lastAlarmOnFile > REPEAT_EMAIL:
                                        alarms["lastAlarm"] = now
                                        print(f"RESENDING-EMAIL to {pools['id']}")
                                        #customise Mail messages and enable Send Here!
                                        #sendMail()
                    else:
                        alarmData.append({"id":pools['id'],"lastAlarm":now})
                        #Customise Mail messages and enable Send Here!
                        #sendMail()
                    json_object = json.dumps(alarmData, indent=4)
                    with open("alarmData.json", "w") as outfile:
                        outfile.write(json_object)
                    print('=============================================')
                    #Send Email 
                    #Create Notify File with Email Dispatch Time (limit sending)   
    except Exception as e:
        print(e)
    time.sleep(SLEEP_TIME)
#Fin

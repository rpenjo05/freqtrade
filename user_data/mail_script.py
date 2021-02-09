import requests as r
import smtplib, ssl
from time import sleep
import subprocess

def send_mail(msg):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "rpenjo05@gmail.com"  # Enter your address
    receiver_email = "rpenjo05@gmail.com"  # Enter receiver address
    password = "tyabskxfprzvixqy"
    message = msg
    print(message)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        
flag = 0

while True:
    res = r.get('https://www.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=20')
    data = res.json()
    if float(data[-1][4]) > float(data[0][4]):
        percentage = 1 - float(data[0][4])/float(data[-1][4])
        if percentage > 0.08 and  flag==0: 
            str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json stopbuy",shell=True)
            send_mail("""Stopbuy\
                      percentage Change="""+str(percentage) + """     
                      
                      """ + str_out )
            flag = 1
        else:
            if flag == 1:
                str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json reload_conf",shell=True)
                send_mail("""Reload Config"""+
                          """     
                      
                      """ + str_out )
                flag = 0
                
    sleep(30)

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

flag = 0
send_mail("Mails Service Started")
#percentage = 0.8
#str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json stopbuy",shell=Tru
e)
#send_mail('Stopbuy\n percentage Change='+str(percentage) +'  \n  ' + str(str_out) )
#str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json reload_config",she
ll=True)
#send_mail('Reload Config   \n  '+ str(str_out) )

while True:
    res = r.get('https://www.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=20')
    data = res.json()
    if float(data[-1][4]) > float(data[0][4]):
        percentage = 1 - float(data[0][4])/float(data[-1][4])
        if percentage > 0.08 and  flag==0:
            str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json stopbuy
",shell=True)
            send_mail('Stopbuy\n percentage Change='+str(percentage) +'  \n  ' + str(str_out) )
            flag = 1
        else:
            if flag == 1:
                str_out = subprocess.check_output("python /workspace/testing/freqtrade/scripts/rest_client.py -c /workspace/testing/freqtrade/rest_config.json rel
oad_config",shell=True)
                send_mail('Reload Config   \n  '+ str(str_out) )
                flag = 0

    sleep(30)

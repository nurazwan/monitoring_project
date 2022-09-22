import datetime
import os
import pymsteams

from data_classes import login_stats_collector


portal=['PORTAL','https://portal.nie.edu.sg/_layouts/15/CustomLoginFBA/LoginPage.aspx','https://portal.nie.edu.sg/Pages/System/Home.aspx']
isaac=['ISAAC','https://isaac.nie.edu.sg/Account/LogOn','https://isaac.nie.edu.sg/']
place=['PLACE','https://place.nie.edu.sg/Login','https://place.nie.edu.sg/']

webhook=os.environ.get('applicationAlert_webhook')
applications=[portal,isaac,place]

for i in applications:
    variables=login_stats_collector(name=i[0],uri=i[1],verification=i[2])
    applicationName=variables.name
    statusCode,elapseTime=variables.status()
    verify,logs = variables.login_successful()
    
    if verify== 0: 
        message=f'{applicationName} login verification is unsuccessful'
        log_message=logs
        #write to influxdb
        try:
            mteams = pymsteams.connectorcard(webhook)
            mteams.text(message)
            mteams.send()
            mteams.text(log_message)
            mteams.send()

        except Exception:
            pass
    
        # try:
        #write to influxdb
        # except Exception

    else:
        # write to influxdb
        pass
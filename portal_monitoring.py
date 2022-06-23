import datetime as dt
import numpy as np
import pandas as pd
import requests as r
import sys
import time

while True:
    #connect to db
    
    portal=pd.read_csv('portals.csv')
    portal=portal[portal.Mute==False]
    timestamp=str((dt.datetime.today()))
    for i in range(len(portal)):
        try:
            if r.get(portal.uri[i],timeout=3).status_code==200:
                status=1
            else:
                status=0
            time_elapsed=r.get(portal.uri[i],timeout=3).elapsed.total_seconds()
            
        except:
            status=None
            time_elapsed=None
            
        
        # write to db
        #close connection to db
        print([timestamp,portal.uri[i],status,time_elapsed])
    
    time.sleep(5)

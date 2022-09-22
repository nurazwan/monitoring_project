import os
import pandas as pd
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class login_stats_collector:
    def __init__(self,name,uri,verification):
        self.name=name
        self.uri=uri
        self.verification=verification

    def status(self):
        r=requests.get(self.uri)
        return r.status_code, r.elapsed.microseconds
    def login_successful(self):
        #get password
        svc_username=os.environ.get('NIE_user')
        svc_password=os.environ.get('NIE_password')

        Logger=[]
        current_URI=None
        chrome_options = Options() 
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("incognito")
        # chrome_options.add_argument("--window-size=240x135")
        chrome_driver = webdriver.Chrome(options=chrome_options)
        # chrome_driver.implicitly_wait(5)

        chrome_driver.get(self.uri)

        content=chrome_driver.page_source
        # chrome_driver.close()

        #element patterns
        user_field_pattern=r'type\="[Tt]ext"'
        password_field_pattern=r'type\="[\w\d]*assword\"'
        button_pattern= r'type\="[sSBb](ubmit|utton)\"'

        # search and validate user field
        user_field_id_object=re.search(user_field_pattern,content)

        if user_field_id_object!=None:
            user_field_id=user_field_id_object.group().replace('"','').replace("type=","")
        else:
            user_field_id='user id field not found'
            
        # search and validate password field
        password_field_object=re.search(password_field_pattern,content)

        if password_field_object!=None:
            password_field_id=password_field_object.group().replace('"','').replace("type=","")
        else:
            password_field_id='password field not found'
            
        # search and validate submit button
        button_object=re.search(button_pattern,content)

        if button_object!=None:
            button_id=button_object.group().replace('"','').replace("type=","")
        else:
            button_id='button not found'


        success=[user_field_id,password_field_id,button_id] != ['user id field not found','password field not found','password field not found']
        Logger.append('Element found: ' + str(success))
        
        if success==True:
            user_field=f"//input[@type='{user_field_id}']"
            password_field=f"//input[@type='{password_field_id}']"
            button_field=f"//input[@type='{button_id}']"
            Logger.append([user_field,password_field,button_field])

            # insert user id to field
            try:
                user_field_location=chrome_driver.find_element(By .XPATH, user_field)
                user_field_location.send_keys(svc_username)
                Logger.append('user insertion successful')
            except:
                Logger.append('user insertion fail')
            # insert password to field
            try:
                password_field_location=chrome_driver.find_element(By .XPATH, password_field)
                password_field_location.send_keys(svc_password)
                Logger.append('password insertion successful')
            except:
                Logger.append('password insertion fail')
            # click the submit button
            try:
                button_location=chrome_driver.find_element(By .XPATH, button_field)
                button_location.click()
                Logger.append('submit successful')
            except:
                Logger.append('submit fail')
        else:
            Logger.append("test not run")

        current_URI=chrome_driver.current_url
        
        chrome_driver.close()

        if current_URI==self.verification:
            verify=1
        else:
            verify=0


        return verify,Logger


# portal_test=login_stats_collector('portal','https://portal.nie.edu.sg/_layouts/15/CustomLoginFBA/LoginPage.aspx','https://portal.nie.edu.sg/Pages/System/Home.aspx')
# print(portal_test.name,portal_test.status_code(),portal_test.login_successful())

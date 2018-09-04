import requests
import http.client
import re
from threading import Thread
import time

Client_Array = [
                "http://texascourses.org",
                "http://texasgateway.org"
                ]

Temp_Client_Array =[]


tropo_token_down = "594c69476d61706e52765947736e4b735053425a78725241634c7644646269595578626b724a4d534c544944"
tropo_token_up = "674c6d78776f697645704e6777636b6d56646b67637a4f51444966495747474f7766686474536f5744676c52"
tropo_url = "https://api.tropo.com/1.0/sessions?action=create&token="
TestVariable = "Hello"
print "HellO"       

def myfunc1():
    while True:
        for site in Client_Array:
            WebsiteStatus = url_ok(site)
            Status = str(WebsiteStatus)
            #print ("The Status of" + " " + client + " " + Status)
            if WebsiteStatus == 200:
                print (site + " Site is UP")
            else:
                Client_Array.remove(site) # Removes entry from client list
                Temp_Client_Array.append(site) #Adds an entry to the temp dictionary 
                print (site + " Site is DOWN and being added to Critical Status")
                             
            time.sleep(60) 

def myfunc2():
    trigger1 = True
    randomValue = 1
    while True:
        for site in Temp_Client_Array:
            #print (randomValue)
            #print (trigger1)
            WebsiteStatus = url_ok(site)
            if WebsiteStatus == 200:
                tropo_alert_site_up(site)
                print (site + " Site is UP and Removed from Critical Status")
                Temp_Client_Array.remove(site)
                Client_Array.append(site)
                if len(Temp_Client_Array) == 0:
                    trigger1 = True
                else:
                    randomValue = randomValue - 1
                
            else: 
                print (site + " Site is DOWN")
                if (trigger1 == True) and (len(Temp_Client_Array) < 2):                
                    tropo_alert_site_down(site)
                    trigger1 = False
                    
                elif len(Temp_Client_Array) > randomValue:
                    tropo_alert_site_down(site)
                    randomValue = randomValue + 1
                    
        
            time.sleep(60)
            


            ''' The Code Below works pretty good for a simple response code '''
def url_ok(url):
    r = requests.get(url)
    SiteStatus = (r.status_code)
    return SiteStatus

def tropo_alert_site_down(site):
	base_url = ""+tropo_url+""+tropo_token_down+"&Tropo_Site_Name="+site+""
	base_url_resp = requests.get(base_url)

def tropo_alert_site_up(site):
	base_url = ""+tropo_url+""+tropo_token_up+"&Tropo_Site_Name="+site+""
	base_url_resp = requests.get(base_url)    
    
    
    


T1 = Thread(target = myfunc1)
T1.daemon = True
T2 = Thread(target = myfunc2)
T2.daemon = True
T1.start()
T2.start()




while True:
    time.sleep(1)




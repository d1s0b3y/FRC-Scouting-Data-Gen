from Hidden import API_KEYS as APIkey
TBA_API_KEY=APIkey.TBA_API_KEY
import requests
import json
def ping(url:str,headConditions:dict={},name:str=None,):
    for i in ['headers','params','auth','allow_redirects','proxies','hooks','stream','verify','cert','timeout','cookies','files']:
        try:
            headConditions[i]
            # print(f"{i} condition found")
        except KeyError:
            # print(f"{i} condition not found, setting to None")
            headConditions[i]=None

    status=requests.head(url=url,headers=headConditions['headers'],params=headConditions['params'],auth=headConditions['auth'],allow_redirects=headConditions['allow_redirects'],proxies=headConditions['proxies'],hooks=headConditions['hooks'],stream=headConditions['stream'],verify=headConditions['verify'],cert=headConditions['cert'],timeout=headConditions['timeout'],cookies=headConditions['cookies'],files=headConditions['files'])
    if status.status_code == 200:
        print(f"connection to {name if name!=None else ''} successful, link pinged: {url}")
    else:
        print(f"connection to {str(name) if name!=None else str(url)} not successful")
        print(status)
        print(status.status_code)

def get_team_events_data(team: int,year:int):
    events={}
    # getting event codes
    print("getting event codes")
    TBAresponse=requests.get(f"https://www.thebluealliance.com/api/v3/team/{'frc'+str(team)}/events/2026/keys",headers={"X-TBA-Auth-Key":TBA_API_KEY})
    TBAtext=TBAresponse.text.split('"')

    # formating event codes
    for i in TBAtext:
        if i.__contains__(str(year))==False:
            TBAtext.remove(i)
    TBAtext.reverse()
    # getting event data
    print("getting event data")
    for eventKey in TBAtext:
        print(f"getting data for {eventKey}")
        SBresponse=requests.get(f"https://api.statbotics.io/v3/event/{eventKey}",)
        if SBresponse.ok==False:
            print(SBresponse.status_code)
        else:
            events[eventKey]=json.loads(SBresponse.text)
    return events
        

team=3414
# SBparams={"metric":"norm_epa","limit":2}

ping(url="https://www.thebluealliance.com/api/v3/status",name="TBA",headConditions={"headers":{"X-TBA-Auth-Key":TBA_API_KEY}})
ping(url="https://api.statbotics.io/openapi.json",name="SB")

# response=get_team_events_data(team=team)

# print(response)

# yes I did regenerate the API Key so if you try to use the one in the old commit it won't work
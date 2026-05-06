# DO NOT SHARE!!!!!!            API_KEY = StFmcbQSa2R3CgVBAyKOVxwxEprPStQxseGkMcZqVjghT421r6OIVYPbvxCcxSky 
import requests
import json
def ping(url:str,headers=None,params=None,timeout=None,name=None):
    status=requests.head(url=url,headers=headers,params=params,timeout=timeout)
    if status.status_code == 200:
        print(f"connection to {name if name!=None else ''} successful, link pinged: {url}")
    else:
        print("connection not successful")
        print(status)
        print(status.status_code)

def get_team_events_data(team: int):
    events={}
    # getting event codes
    print("getting event codes")
    TBAresponse=requests.get(f"https://www.thebluealliance.com/api/v3/team/{'frc'+str(team)}/events/2026/keys",headers={"X-TBA-Auth-Key":"StFmcbQSa2R3CgVBAyKOVxwxEprPStQxseGkMcZqVjghT421r6OIVYPbvxCcxSky"})
    TBAtext=TBAresponse.text.split('"')

    # formating event codes
    for i in TBAtext:
        if i.__contains__('2026')==False:
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

# ping(url="https://www.thebluealliance.com/api/v3/status",name="TBA",headers={"X-TBA-Auth-Key":"StFmcbQSa2R3CgVBAyKOVxwxEprPStQxseGkMcZqVjghT421r6OIVYPbvxCcxSky"})
# ping(url="https://api.statbotics.io/openapi.json",name="SB")

response=get_team_events_data(team=team)

print(response)

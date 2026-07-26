from Hidden import API_KEYS as APIkey
TBA_API_KEY=APIkey.TBA_API_KEY
import requests
import json
def ping(url:str,headConditions:dict={},name:str=None,print_success:bool=False,print_fail:bool=True) -> bool:
    for i in ['headers','params','auth','allow_redirects','proxies','hooks','stream','verify','cert','timeout','cookies','files']:
        try:
            headConditions[i]
            # print(f"{i} condition found")
        except KeyError:
            # print(f"{i} condition not found, setting to None")
            headConditions[i]=None

    status=requests.head(url=url,headers=headConditions['headers'],params=headConditions['params'],auth=headConditions['auth'],allow_redirects=headConditions['allow_redirects'],proxies=headConditions['proxies'],hooks=headConditions['hooks'],stream=headConditions['stream'],verify=headConditions['verify'],cert=headConditions['cert'],timeout=headConditions['timeout'],cookies=headConditions['cookies'],files=headConditions['files'])
    if status.status_code == 200:
        if print_success:
            print(f"connection to {name if name!=None else ''} successful, link pinged: {url}")
        return True
    else:
        if print_fail:
            print(f"connection to {str(name) if name!=None else str(url)} not successful")
            print(status)
            print(status.status_code)
        return False

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
year=2026
attempts=1000
sucess=0
# ping(url=f"https://api.statbotics.io/openapi.json/v3/{team}/{year}")
for i in range(attempts-1):
    if ping(url="https://api.statbotics.io/openapi.json/v3/3414/2026",name="SB",print_success=False,print_fail=False):
        sucess+=1
    print(f"{sucess}/{i+1}")
print(f"Final Count: {sucess}/{attempts}")

# response=get_team_events_data(team=team)

# print(response)

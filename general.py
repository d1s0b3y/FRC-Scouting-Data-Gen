import requests
import json
import csv

statbotics_base_url="https://api.statbotics.io/v3/"
popcornpenguins_base_url="https://api-statbotics.popcornpenguins.com/v3/"


teams=[{'team': 4414, 'name': 'HighTide', 'country': 'USA', 'state': 'CA', 'district': 'ca', 'rookie_year': 2012, 'active': True, 'last_active_year': 2026, 'record': {'wins': 351, 'losses': 54, 'ties': 2, 'count': 407, 'winrate': 0.8649}, 'norm_epa': {'current': 1997.0, 'recent': 1864.0, 'mean': 1830.0, 'max': 1997.0}}, {'team': 254, 'name': 'The Cheesy Poofs', 'country': 'USA', 'state': 'CA', 'district': 'ca', 'rookie_year': 1999, 'active': True, 'last_active_year': 2026, 'record': {'wins': 927, 'losses': 173, 'ties': 8, 'count': 1108, 'winrate': 0.8403}, 'norm_epa': {'current': 1950.0, 'recent': 1899.0, 'mean': 1893.0, 'max': 2058.0}}, {'team': 1323, 'name': 'MadTown Robotics', 'country': 'USA', 'state': 'CA', 'district': 'ca', 'rookie_year': 2004, 'active': True, 'last_active_year': 2026, 'record': {'wins': 607, 'losses': 214, 'ties': 12, 'count': 833, 'winrate': 0.7359}, 'norm_epa': {'current': 1921.0, 'recent': 1941.0, 'mean': 1722.0, 'max': 2043.0}}, {'team': 7769, 'name': 'The CREW', 'country': 'USA', 'state': 'MI', 'district': 'fim', 'rookie_year': 2019, 'active': True, 'last_active_year': 2026, 'record': {'wins': 289, 'losses': 122, 'ties': 5, 'count': 416, 'winrate': 0.7007}, 'norm_epa': {'current': 1920.0, 'recent': 1768.0, 'mean': 1703.0, 'max': 1920.0}}, {'team': 1690, 'name': 'Orbit', 'country': 'Israel', 'state': None, 'district': 'isr', 'rookie_year': 2005, 'active': True, 'last_active_year': 2026, 'record': {'wins': 552, 'losses': 174, 'ties': 6, 'count': 732, 'winrate': 0.7582}, 'norm_epa': {'current': 1909.0, 'recent': 1895.0, 'mean': 1723.0, 'max': 1942.0}}, {'team': 2056, 'name': 'OP Robotics', 'country': 'Canada', 'state': 'ON', 'district': 'ont', 'rookie_year': 2007, 'active': True, 'last_active_year': 2026, 'record': {'wins': 964, 'losses': 144, 'ties': 5, 'count': 1113, 'winrate': 0.8684}, 'norm_epa': {'current': 1908.0, 'recent': 1928.0, 'mean': 1947.0, 'max': 2021.0}}, {'team': 27, 'name': 'Team RUSH', 'country': 'USA', 'state': 'MI', 'district': 'fim', 'rookie_year': 1997, 'active': True, 'last_active_year': 2026, 'record': {'wins': 1039, 'losses': 433, 'ties': 14, 'count': 1486, 'winrate': 0.7039}, 'norm_epa': {'current': 1897.0, 'recent': 1799.0, 'mean': 1758.0, 'max': 1923.0}}, {'team': 2481, 'name': 'Roboteers', 'country': 'USA', 'state': 'IL', 'district': None, 'rookie_year': 2008, 'active': True, 'last_active_year': 2026, 'record': {'wins': 522, 'losses': 155, 'ties': 6, 'count': 683, 'winrate': 0.7687}, 'norm_epa': {'current': 1886.0, 'recent': 1816.0, 'mean': 1760.0, 'max': 1886.0}}, {'team': 1114, 'name': 'Simbotics', 'country': 'Canada', 'state': 'ON', 'district': 'ont', 'rookie_year': 2003, 'active': True, 'last_active_year': 2026, 'record': {'wins': 1030, 'losses': 268, 'ties': 8, 'count': 1306, 'winrate': 0.7917}, 'norm_epa': {'current': 1885.0, 'recent': 1787.0, 'mean': 1868.0, 'max': 2136.0}}, {'team': 125, 'name': 'NUTRONs', 'country': 'USA', 'state': 'MA', 'district': 'ne', 'rookie_year': 1998, 'active': True, 'last_active_year': 2026, 'record': {'wins': 831, 'losses': 404, 'ties': 15, 'count': 1250, 'winrate': 0.6708}, 'norm_epa': {'current': 1878.0, 'recent': 1805.0, 'mean': 1671.0, 'max': 1883.0}}]

def statbotics_status() -> bool:
    """Returns true if statbotics is up"""
    try:
        test=requests.get("https://api.statbotics.io/v3/team_year/3414/2026")
        if test.status_code!=200:
            raise UserWarning
        else:
            return True
    except Exception as e:
        return False

metrics_list=["norm_epa","team"]
valid_conditions=["active"]
def get_teams(url:str,amount:int,other_conditions:dict,metric:str="norm_epa",offset:int=0,numbers:bool=False)->list[int]:
    """get teams given a set of conditions and a url and outputs in a dict with the key of either team name or number"""
    formatted_conditions=""
    
    # metric conditions
    metric_condition=""
    for i in metrics_list:
        if metric == i:
            metric_condition=f"metric={metric}"
    if metric_condition == "" and metric !="":
        print("Invalid metric when searching for teams")
    formatted_conditions+=metric_condition

    # other conditions 
    valid=False
    for i in other_conditions.keys():
        for j in valid_conditions:
            if i==j:
                valid=True
                break
        if valid:
            formatted_conditions+=f"&{i}={other_conditions.get(i)}"

    # print(url+"teams?"+formatted_conditions+f"&limit={amount}")
    
    teams=[]
    if amount>1000:
        while amount>0:
            if amount<1000:
                limit=amount
            else:
                limit=1000
            teams_response=requests.get(url+"teams?"+formatted_conditions+f"&limit={limit}"+f"&offset={offset}")
            for teams_group in json.loads(teams_response.text):
                teams.append(teams_group)
            offset+=1000
            amount-=1000
    else:
        teams_response=requests.get(url+"teams?"+formatted_conditions+f"&limit={amount}"+f"&offset={offset}")
        teams=json.loads(teams_response.text)
    team_numbers=[]
    for i in teams:
        team_numbers.append(i.get("team"))

    if numbers:
        return team_numbers
    else:
        return teams

valid_fields=["team","name","country","state","district","rookie_year","active","last_active_year","record","norm_epa"]
valid_keys=["name","team"]
def format_general_teams_data(key:str,general_teams_data:list[dict],fields:list[str]=["team","name","record"]) -> dict|None:
    """formats general team data to only contain the requested fields"""
    data={}
    key_valid=False
    for i in valid_keys:
        if key==i:
            key_valid=True

    if key_valid==False:
        print("invalid key")
        return None
    
    for i in general_teams_data:
        team_data={}
        valid=False
        for j in fields:
            for k in valid_fields:
                if j==k:
                    valid=True
                    break
            if valid:
                team_data[j]=i.get(j)
        data[i.get(key)]=team_data
    return data

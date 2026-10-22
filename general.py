import requests
import json
import csv
from enum import Enum
statbotics_base_url="https://api.statbotics.io/v3/"
popcornpenguins_base_url="https://api-statbotics.popcornpenguins.com/v3/"


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

class Get_Data:
    
    metrics_list=["norm_epa","team"]
    valid_conditions=["active"]
    valid_outputs=["team","name","all"]
    def get_teams(self,url:str,amount:int,other_conditions:dict,metric:str="norm_epa",offset:int=0,output:str="team")->list[int]:
        """get teams given a set of conditions and a url and outputs in a dict with the key of either team name or number"""
        formatted_conditions=""
        
        # metric conditions
        metric_condition=""
        for i in self.metrics_list:
            if metric == i:
                metric_condition=f"metric={metric}"
        if metric_condition == "" and metric !="":
            print("Invalid metric when searching for teams")
        formatted_conditions+=metric_condition

        # other conditions 
        valid=False
        for i in other_conditions.keys():
            for j in self.valid_conditions:
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
        team_names=[]
        for i in teams:
            team_numbers.append(i.get("team"))
            team_names.append(i.get("name"))

        if output=="team":
            return team_numbers
        elif output=="name":
            return team_names
        else:
            return teams

    year=2026
    def get_teams_year(self,url:str,year:int=year,teams:list=[]):
        total_stats={}
        for i in teams:
            team_stats_response=requests.get(url+f"team_year/{i}/{year}")
            team_stats=json.loads(team_stats_response.text)
            total_stats[i]=team_stats
        return total_stats

#    get team event
# get team events
class Format_Data:
    
    valid_general_fields=["team","name","country","state","district","rookie_year","active","last_active_year","record","norm_epa"]
    valid_keys=["name","team"]
    def format_general_teams_data(self,key:str,general_teams_data:list[dict],fields:list[str]=["team","name","record"]) -> dict|None:
        """formats general team data to only contain the requested fields"""
        data={}
        key_valid=False
        for i in self.valid_keys:
            if key==i:
                key_valid=True

        if key_valid==False:
            print("invalid key")
            return None
        
        for i in general_teams_data:
            team_data={}
            for j in fields:
                valid=False
                for k in self.valid_general_fields:
                    if j==k:
                        valid=True
                        break
                if valid:
                    team_data[j]=i.get(j)
            data[i.get(key)]=team_data
        return data

    valid_team_year_fields=["team","year","name","country","state","district","rookie_year","epa","stats","ranks","record","competing"]
    def format_teams_year_data(self,key:str,teams_year_data:list[dict],fields:list[str]):
        data={}
        key_valid=False
        for j in self.valid_keys:
            if key==j:
                key_valid=True

        if key_valid==False:
            print("invalid key")
            return None

        for i in teams_year_data:
            team_data={}
            for j in fields:
                field_valid=False
                for k in self.valid_team_year_fields:
                    if j==k:
                        field_valid=True
                        break
                if field_valid:
                    team_data[j]=i.get(j)
            data[i.get(key)]=team_data
        return data
            
# format team events data
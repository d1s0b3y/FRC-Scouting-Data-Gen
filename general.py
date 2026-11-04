from typing import Iterable,Any
import requests
import json
import csv
import re
STATBOTICS_BASE_URL="https://api.statbotics.io/v3/"
POPCORNPENGUINS_BASE_URL="https://api-statbotics.popcornpenguins.com/v3/"

team_data=dict[str,str|int|dict[str,Any]]

def statbotics_status(label:bool=False) -> bool:
    """Returns true if statbotics is up"""
    try:
        test=requests.get("https://api.statbotics.io/v3/team_year/3414/2026")
        if test.status_code!=200:
            raise UserWarning
        else:
            if label:
                print("statbotics is up")
            return True
    except Exception as e:
        if label:
            print("statbotics is down")
        return False

def get_many_teams(full_url:str,amount:int,offset:int=0) -> list[team_data]:
    """A utility function 
    \n Allowing you to get the information(based on url) 
    \n With no limit on team amount"""
    teams=[]
    if amount>1000: #only lets you get 1k at a time, so if more then special case
        while amount>0:
            if amount<1000: #just in case you have an amount thats not a multiple of 1k
                limit=amount
            else:
                limit=1000
            teams_response=requests.get(full_url+f"&limit={limit}"+f"&offset={offset}")
            for teams_group in json.loads(teams_response.text):
                teams.append(teams_group)
            offset+=1000
            amount-=1000
    else:
        teams_response=requests.get(full_url+f"&limit={amount}"+f"&offset={offset}")
        teams=json.loads(teams_response.text)
    return teams

def convert_key(desired_key:Any,input_key:Any,dictionary:dict,regex:bool=False,retry:bool=True,prints=False) -> dict[Any,Any]|None:
    found=False
    if regex:
        for i in dictionary.keys():
            if re.match(input_key,i):
                val=dictionary.pop(i)
                dictionary[desired_key]=val
                found=True
                break
            else:
                print("not found")
    else:
        try: # if it fails, try as regex
            val=dictionary.pop(input_key)
            dictionary[desired_key]=val
        except KeyError as e:
            print(f"Key Error: {e}, trying as regex\n" if prints else "\0",end='')
            if retry: #try again as regex by calling recursively but without retry
                return convert_key(desired_key,input_key,dictionary,True,False,prints)
            else:
                found=False

    if found==False:
        print("key not found\n" if prints else "\0",end='')
        return None
    else:
        return dictionary

class Data_collector:

    base_url=STATBOTICS_BASE_URL if statbotics_status() else POPCORNPENGUINS_BASE_URL
    year=2026
    prints=False
    def __init__(self,
                 base_url:str=STATBOTICS_BASE_URL if statbotics_status() else POPCORNPENGUINS_BASE_URL,
                 year:int=2026,prints:bool=False) -> None:
        self.base_url=base_url
        self.year=year
        self.prints=prints

    
    valid_metrics=["norm_epa","team"]
    valid_conditions=["active"]
    valid_outputs=["team","name","all"]
    def get_teams(self,amount:int,url:str=base_url,conditions:dict[str,str]={"active":"true"},metric:str="norm_epa",offset:int=0,output:str="team") -> Iterable[team_data|int|str]:
        """get teams given a set of conditions and a url and outputs in a dict with the key of either team name or number"""
        formatted_conditions=""
        
        # metric conditions
        metric_condition=""
        for i in self.valid_metrics:
            if metric == i:
                metric_condition=f"metric={metric}"
        if metric_condition == "" and metric !="":
            print("Invalid metric when searching for teams\n" if self.prints else "\0",end='')
        formatted_conditions+=metric_condition

        # other conditions 
        valid=False
        for i in conditions.keys():
            for j in self.valid_conditions:
                if i==j:
                    valid=True
                    break
            if valid:
                formatted_conditions+=f"&{i}={conditions.get(i)}"
        # print(url+"teams?"+formatted_conditions+f"&limit={amount}")
        teams=get_many_teams(full_url=url+"teams?"+formatted_conditions,amount=amount,offset=offset)
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

    def get_teams_year(self,teams:list[int],url:str=base_url,year:int=year) -> dict[int,team_data]:
        total_stats={}
        for i in teams:
            team_stats_response=requests.get(url+f"team_year/{i}/{year}")
            team_stats=json.loads(team_stats_response.text)
            total_stats[i]=team_stats
        return total_stats

# TODO:
#    get team event
# get team events
class Data_Formater:
    prints=False
    valid_keys=["name","team"]
    def __init__(self) -> None:
        pass

    valid_general_fields=["team","name","country","state","district","rookie_year","active","last_active_year","record","norm_epa"]
    def format_general_teams_data(self,key:str,general_teams_data:list[dict],fields:list[str]=["team","name","record"]) -> dict|None:
        """formats general team data to only contain the requested fields"""
        data={}
        key_valid=False
        for i in self.valid_keys:
            if key==i:
                key_valid=True

        if key_valid==False:
            print("invalid key\n" if self.prints else "",end='')
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
    def format_teams_year_data(self,key:str,teams_year_data:list[dict],fields:list[str]) -> dict|None:
        data={}
        key_valid=False
        for j in self.valid_keys:
            if key==j:
                key_valid=True

        if key_valid==False:
            print("invalid key\n" if self.prints else "\0",end='')
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

class File_Manager:
    prints=False
    file_name="Collected Data"
    file_extension="csv"
    full_file_name=file_name+"."+file_extension
    encoding='utf-8'
    fields=[]
    def __init__(self,encoding:str=encoding,file_name:str=file_name,file_extension:str=file_extension,fieldnames:list[str]=fields) -> None:
        self.encoding=encoding
        self.file_name=file_name
        self.file_extension=file_extension
        self.full_file_name=file_name+'.'+file_extension
        self.fields=fieldnames


    def write_csv(self,data:dict[str,Any],fieldnames:list[str],header:bool=False,name:str=file_name) -> None:
        with open(name+'.csv','a',newline='',encoding=self.encoding) as file:
            writer=csv.DictWriter(file,fieldnames=fieldnames)
            if header:
                writer.writeheader()
            writer.writerow(data)
        file.close()

    def write_data(self,data:list[dict[str,Any]],name:str=file_name,header:bool=False):
        if header:
            write_header=True
        else:
            write_header=False
        for i in data:
            keys=[]
            for key,_ in i.items():
                keys.append(key)
            self.write_csv(i,keys,write_header,name)
            if write_header:
                write_header=False

# TODO:
# format team events data
# 
# ---------------------------------------------------------------
# TESTING
file_manager=File_Manager()
data_collector=Data_collector()
data_formater=Data_Formater()
prints=True
file_manager.prints=prints
data_collector.prints=prints
data_formater.prints=prints
regexs={
"numbers":r"/\b\d+\b/gm",
}
# file_manager.write_data([{"team":123,"name":456,"other data":{"epa":1,"norm":2}},{"team":456,"name":123,"other data":{"epa":2,"norm":1}}],header=True)
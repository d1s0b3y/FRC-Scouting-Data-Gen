import requests
import json
import csv
import tqdm

# get the base url (try from popcorn penuins if statbotics is down)
try:
    test=requests.get("https://api.statbotics.io/v3/team_year/3414/2026")
    if test.status_code!=200:
        raise UserWarning
    base_url="https://api.statbotics.io/v3/"
except Exception as e:
    print(f"error with statbotics using popcornpenguins statbotics:\n{e}")
    base_url="https://api-statbotics.popcornpenguins.com/v3/"

team_amount=1000
year=2026
output_file_name="more_than_1K_teams"
teams=[]

print("finding teams")
if team_amount>1000:
    offset=0
    while team_amount>0:
        if team_amount<1000:
            limit=team_amount
        else:
            limit=1000
        teams_response=requests.get(base_url+f"teams?active=true&metric=norm_epa&limit={limit}&offset={offset}")
        for teams_group in json.loads(teams_response.text):
            teams.append(teams_group)
        offset+=1000
        team_amount-=1000
else:
    teams_response=requests.get(base_url+f"teams?active=true&metric=norm_epa&limit={team_amount}")
    teams=json.loads(teams_response.text)

print("gathering team data")
with open(output_file_name+'.csv', 'a', newline='',encoding='utf-8') as file:
    fieldnames=["Team number","Team name","Epa","Auto EPA","Teleop EPA","Energized","Supercharged","Transition","First Shift","Second Shift","Endgame","Win Rate","Wins","Losses"]
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()

    for team in tqdm.tqdm(teams):
        team_stats_response=requests.get(base_url+f"team_year/{team['team']}/{year}")
        team_stats=json.loads(team_stats_response.text)
        # stats to gether
        total_points=team_stats['epa']
        points = total_points['total_points']
        mean=points
        breakdown=total_points['breakdown']
        record=team_stats['record']
        wins=record['wins']
        losses=record['losses']
        writer.writerow({"Team number":team['team'],"Team name":team_stats['name'],"Epa":mean,"Auto EPA":breakdown['auto_points'],"Teleop EPA":breakdown['teleop_points'],"Energized":breakdown['energized_rp'], "Supercharged":breakdown['supercharged_rp'],"Transition":breakdown['transition_fuel'],"First Shift":breakdown['first_shift_fuel'],"Second Shift":breakdown['second_shift_fuel'],"Endgame":breakdown['endgame_fuel'],"Win Rate":team_stats['record']['winrate'],"Wins":wins,"Losses":losses})
        # print(f"gathered stats for {team['team']}:{team['name']}\n{teams.index(team)+1} teams queried, {len(teams)-teams.index(team)-1} remaining")



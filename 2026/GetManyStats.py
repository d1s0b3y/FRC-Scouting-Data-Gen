import statbotics
import csv
# using statbotics
sb= statbotics.Statbotics()
statsLst=[]
teamAmt=1
teams=sb.get_teams(metric='norm_epa',limit=teamAmt,fields=['team','name'])
print("finding teams")

for team in teams:
    teamStats=sb.get_team_year(team['team'],2026)
    total_points=teamStats['epa']
    points = total_points['total_points']
    mean=points['mean']
    breakdown=total_points['breakdown']
    record=teamStats['record']
    wins=record['wins']
    losses=record['losses']
    if teamStats['competing']['next_event_key']=='2026cmptx':
        qualified=True
    else:
        qualified=False
    statsLst.append({"Team number":team['team'],"Team name":team['name'],"Epa":mean,"Auto EPA":breakdown['auto_points'],"Teleop EPA":breakdown['teleop_points'],"Energized":breakdown['energized_rp'], "Supercharged":breakdown['supercharged_rp'],"Transition":breakdown['transition_fuel'],"First Shift":breakdown['first_shift_fuel'],"Second Shift":breakdown['second_shift_fuel'],"Endgame":breakdown['endgame_fuel'],"Win Rate":teamStats['record']['winrate'],"Wins":wins,"Losses":losses})
    print(f"gathered stats for {team['name']}      {teams.index(team)+1} teams queried, {len(teams)-teams.index(team)-1} remaining",)

fieldnames=statsLst[0].keys()

with open('500teams.csv', 'a', newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(statsLst)
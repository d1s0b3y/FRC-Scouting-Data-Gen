import statbotics
import csv
# using statbotics

sb= statbotics.Statbotics()
statsLst=[]
teams=[2096,10396,10217,6652,10114,7551,5968,9646,3630,321,772,7403,11269]
print("finding teams")

for team in teams:
    teamStats=sb.get_team_year(team,2026)
    total_points=teamStats['epa']
    points = total_points['total_points']
    mean=points['mean']
    breakdown=total_points['breakdown']
    if teamStats['competing']['next_event_key']=='2026cmptx':
        qualified=True
    else:
        qualified=False
    statsLst.append({"Team number":teamStats['team'],"Team name":teamStats['name'],"Epa":mean,"Auto EPA":breakdown['auto_points'],"Teleop EPA":breakdown['teleop_points'],"Energized":breakdown['energized_rp'], "Supercharged":breakdown['supercharged_rp'],"Transition":breakdown['transition_fuel'],"First Shift":breakdown['first_shift_fuel'],"Second Shift":breakdown['second_shift_fuel'],"Endgame":breakdown['endgame_fuel'],"Win Rate":teamStats['record']['winrate'],"Qualified for worlds": qualified})
    print(f"gathered stats for {teamStats['name']}      {teams.index(team)+1} teams queried, {len(teams)-teams.index(team)-1} remaining",)

fieldnames=statsLst[0].keys()

with open('field teams.csv', 'a', newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(statsLst)

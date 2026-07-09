import statbotics
import csv
# using statbotics
sb= statbotics.Statbotics()
statsLst=[]
teamAmt=1
teams=sb.get_teams(metric='norm_epa',limit=teamAmt,fields=['team','name'])
print("finding teams")

for team in teams:
    teamStats=sb.get_team_year(team['team'],2026,fields=['competing'])
    statsLst.append({"Team number":team['team'],"Team name":team['name'],"Next event":team['competing']['next_event_key']})
    print(f"gathered stats for {team['name']}      {teams.index(team)+1} teams queried, {len(teams)-teams.index(team)-1} remaining",)

fieldnames=statsLst[0].keys()

with open('asd.csv', 'a', newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(statsLst)

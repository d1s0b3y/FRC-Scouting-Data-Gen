import statbotics
import csv

# wins=0
# totals=0
# for key in dicts:
#     wins+=dicts[key]['wins']
#     totals+=dicts[key]['total']
# print(wins/totals)
# 0.8011025928159187
def listContatins(value,list):
    # print("cheching if key already queried")
    for i in list:
        if i ==value:
            return True
    return False
def changeKey(key,newKey,dict):
    values=dict.pop(key)
    dict[newKey]=(values)

sb= statbotics.Statbotics()
teamAmt=10
print("finding teams")
countryErrors=0
try:
    teams=sb.get_teams(metric='norm_epa',limit=teamAmt,fields=['team','name','state','country'])
    autonWinsTeam={'general':{'total wins':0,'total matches checked':0,'score errors total':0,'winner errors total':0,'event errors total':0}}
    matchKeys=[]
    for team in teams:
        autonWinsTeam[team['name']]={'wins':0,'total':0,'proportion':0,'score errors':0,'winner errors':0,'event errors':0}
        try:
            try:        
                events=sb.get_events(year=2026,state=team['state'],country=team['country'],fields=['key','name'])
            except ValueError:
                print("Country couldnt be found WHAT THE FUCK?")
                countryErrors+=1
        except UserWarning:
            events={}
            print("Events could not be found WTF?")
            autonWinsTeam['general']['event errors total']+=1
            autonWinsTeam[team['name']]['event errors']+=1
        # print(events)
        print(f"{teams.index(team)} teams queried, {len(teams)-teams.index(team)} remaining")
        for event in events:
            # print(events)
            # print(f"{events.index(event)+1} events queried, {len(events)-teams.index(event)-1} remaining")
            try:
                matches=sb.get_matches(team=team['team'],event=event['key'],fields=['result','key'])
                for match in matches:
                    result=match['result']
                    print(f"{str(team['name'])} found in {match['key']}")
                    if result['red_auto_points']==None:
                        autonWinsTeam['general']['score errors total']+=1
                        autonWinsTeam[team['name']]['score errors']+=1
                        result['red_auto_points']=0
                        print("red auto points = none?")
                    if result['blue_auto_points']==None:
                        autonWinsTeam['general']['score errors total']+=1
                        autonWinsTeam[team['name']]['score errors']+=1
                        result['blue_auto_points']=0
                        print("blue auto points = none?")
                    if result['winner']==None:
                        autonWinsTeam['general']['winner errors total']+=1
                        autonWinsTeam[team['name']]['winner errors']+=1
                        result['winner']=''
                        print("no winner?")
                    if (result['winner'].lower()=='red' and result['red_auto_points']>result['blue_auto_points'])or(result['winner'].lower()=='blue' and result['red_auto_points']<result['blue_auto_points']):
                        # print("auton predicted winner")
                        autonWinsTeam[team['name']]['wins']+=1
                        if not listContatins(match['key'],matchKeys):
                            autonWinsTeam['general']['total wins']+=1
                    autonWinsTeam[team['name']]['total']+=1

                    if not listContatins(match['key'],matchKeys):
                        matchKeys.append(match['key'])
                        autonWinsTeam['general']['total matches checked']+=1
                    # else:
                        # print(f"match {match['key']} already counted towards total")
                        # print(matchKeys)
            except UserWarning:
                print(f"{team['name']} not found in {event['name']}")
        if autonWinsTeam[team['name']]['total'] >0:
            autonWinsTeam[team['name']]['proportion']=autonWinsTeam[team['name']]['wins']/autonWinsTeam[team['name']]['total']

except Exception as e:
    print(f"General error {e}")
    # raise InterruptedError

with open('blah blah blah.csv', 'a', newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=['name','wins','total','proportion','score errors','winner errors','event errors'])
    writer.writeheader()

    for key,value in autonWinsTeam.items():
        if key == 'general':
            changeKey('total wins','wins',value)
            changeKey('total matches checked','total',value)
            changeKey('score errors total','score errors',value)
            changeKey('winner errors total','winner errors',value)
            changeKey('event errors total','event errors',value)
        row={'name':key}
        row.update(value)
        writer.writerow(row)

print(autonWinsTeam['general'])
print(f"country errors idfk {countryErrors}")

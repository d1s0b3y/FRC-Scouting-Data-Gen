import statbotics
import csv
import random

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
teamAmt=500
print("finding teams")
teams=[]
randomNumbers=[]
print("Generating randoms")
for i in range(1001): # gets the random numbers here so that it runs faster getting the teams from statbotics
    number=random.randint(0,1000)
    if not listContatins(number,randomNumbers):
        randomNumbers.append(number)
    else: # make sure no duplicates so we dont collect data twice
        i-=1
print("Getting teams")
try:
    for i in range(teamAmt):
        teams.append(sb.get_teams(metric='norm_epa',limit=1,fields=['team','name','state','country'],offset=randomNumbers[i])[0])
        print(i+1,"Team(s) Found")
    autonWinsTeam={'general':{'total wins':0,'total losses':0,'total matches checked':0,'score errors total':0,'winner errors total':0,'event errors total':0,"Country errors total":0}}
    matchKeys=[]
    print("collecting data for teams")
    for team in teams:
        eventOff=0
        autonWinsTeam[team['name']]={'wins':0,'losses':0,'total':0,'proportion':0,'score errors':0,'winner errors':0,'event errors':0,'country errors':0}
        run=True
        while run==True:
            try:
                try:        
                    events=sb.get_events(year=2026,state=team['state'],country=team['country'],fields=['key','name'],offset=eventOff)
                    run=False
                except ValueError:
                    print("Country couldnt be found HOW???")
                    autonWinsTeam['general']['Country errors total']+=1
                    autonWinsTeam[team['name']]['country errors']+=1
                    run=False
            except UserWarning:
                events={}
                eventOff+=100
                if eventOff<10000:
                    run=True
                else:
                    run = False
                    print("Max offset reached, skipping")
                print("Events could not be found ??? (offseting)")
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
                    else:
                        autonWinsTeam[team['name']]['losses']+=1
                        if not listContatins(match['key'],matchKeys):
                            autonWinsTeam['general']['total losses']+=1

                    autonWinsTeam[team['name']]['total']+=1

                    if not listContatins(match['key'],matchKeys):
                        matchKeys.append(match['key'])
                        autonWinsTeam['general']['total matches checked']+=1
                    # else:
                        # print(f"match {match['key']} already counted towards total amount of matches")
                        # print(matchKeys)
            except UserWarning:
                print(f"{team['name']} not found in {event['name']}")
        if autonWinsTeam[team['name']]['total'] >0:
            autonWinsTeam[team['name']]['proportion']=autonWinsTeam[team['name']]['wins']/autonWinsTeam[team['name']]['total']
except:
    print("Interrupted")
    # print(f"General error {e}")
    # raise InterruptedError

with open('Actually Random Auton Correlation Data.csv', 'a', newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=['name','wins','losses','total','proportion','score errors','winner errors','event errors','country errors'])
    writer.writeheader()

    for key,value in autonWinsTeam.items():
        if key == 'general':
            changeKey('total wins','wins',value)
            changeKey('total losses','losses',value)
            changeKey('total matches checked','total',value)
            changeKey('score errors total','score errors',value)
            changeKey('winner errors total','winner errors',value)
            changeKey('event errors total','event errors',value)
            changeKey('Country errors total','country errors',value)
        row={'name':key}
        row.update(value)
        writer.writerow(row)

print(autonWinsTeam['general'])

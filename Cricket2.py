from math import modf
import random
from os import system

#initialize some variables
totalRuns = 0
wicketsTaken =0
currentBatsman = 0
nonStriker = 1
global teamA, teamB

#perform toss by using random() function
def toss(teams):
    return f"\n{random.choice(teams)} won the toss.\n"

#initialize team members
def initializeBattingTeam(n):
    team = []
    for _ in range(n):
        team.append( batter() )
    return team

def initializeBowlingTeam(n):
    team = []
    for _ in range(n):
        team.append( bowler() )
    return team

#define class batter
class batter:
    def __init__(self):
        self.runsScored = 0
        self.ballsFaced = 0
        self.condition = "DNB"

    def scored(self,runs=0):
        self.runsScored += runs
        self.ballsFaced += 1

    def display(self):
        return(f"{self.runsScored}({self.ballsFaced})  {self.condition}")
#define class bowler
class bowler:
    def __init__(self):
        self.oversBowled = 0
        self.runsConceded = 0
        self.wicketsTaken = 0

    def bowled(self,runs=0,case=" "):

        if case == "extras": #wide or no-ball
            self.runsConceded += 1+runs
        elif case == "wicket":  #wicket
            self.oversBowled += 0.1
            self.wicketsTaken += 1
        else:
            self.oversBowled += 0.1
            self.runsConceded += runs
        
        #to manage overs bowled counter
        a = modf(self.oversBowled)
        #returns a tuple of(decimal,integer)
        #happens to return 0.6000001
        if a[0] >= 0.6:
            over = a[1] + 1.0
            self.oversBowled = over

    def display(self):
        return( '%.1f '%self.oversBowled , '%3d '%self.runsConceded , '%2d '%self.wicketsTaken)

def bowlingOutcomes():
    #possible outcomes on a single ball
    return('''
    0) No run       1) One run
    2) Two runs     3) Three runs
    4) Four runs    5) Five runs
    6) Six runs     7) Wide ball
    8) No ball      9) Wicket       ''')

def outcomeExecution(ballResult, currentBatsman, currentBowler):
    global totalRuns, wicketsTaken

    if ballResult in range(7):
        teamA[currentBatsman].scored(ballResult)
        teamB[currentBowler].bowled(ballResult)
        totalRuns += ballResult
        return str(ballResult)

    elif ballResult == 7:
        teamB[currentBowler].bowled(case="extras")
        totalRuns += 1
        return "WD"
    elif ballResult == 8:
        teamB[currentBowler].bowled(case="extras")
        totalRuns += 1
        return "NB"

    elif ballResult == 9:
        teamB[currentBowler].bowled(case="wicket")
        teamA[currentBatsman].condition = "Out"     #batsman status
        wicketsTaken += 1
        return "WT"

#main() function
if __name__ == '__main__':
    
    #clearing the terminal
    try:
        system('clear')
    except :
        system('cls')

    noOfPlayers = int(input("No. of players - "))
    overs = int(input("Match length in overs: "))

    print(toss(["TeamA","TeamB"])) 

    #when teamA bats
    teamA = initializeBattingTeam(noOfPlayers)
    teamB = initializeBowlingTeam(noOfPlayers)
    
    inning1 = open("inning1.txt", "w")

    teamA[currentBatsman].condition = "NotOut" #new batsman
    teamA[nonStriker].condition = "NotOut" #new batsman

    for i in range(overs):
        
        if(wicketsTaken == noOfPlayers-1):  #all out
            break
        
        overHistory = []    #record the over
        ballsInOver = 1     #no. of balls bowled in that over
        
        try:
            currentBowler = int(input(f"Enter bowler id(0-{noOfPlayers-1}) for over {i+1}: "))
            if not currentBowler in range(noOfPlayers):
                raise Exception
        except:
            print("Invalid Input...Try again!!!")
            currentBowler = int(input(f"Enter bowler id(0-{noOfPlayers-1}) for over {i+1}: "))

        while(ballsInOver<=6):
            print(f"\nEnter the outcome for ball {i}.{ballsInOver} :", end="")
            print(bowlingOutcomes())
            
            try:
                ballResult = int(input("Outcome --> "))
                if not ballResult in range(10):
                    raise Exception
            except:
                print("Invalid input!!! Enter again")
                continue

            outcome = outcomeExecution(ballResult, currentBatsman, currentBowler)
            ballsInOver += 1

            overHistory.append(outcome)

            if ballResult in [1,3,5]: #odd runs
	    # to change the batsman on strike
                currentBatsman, nonStriker = nonStriker, currentBatsman
            elif ballResult == 7 : #wide ball
                print("Wide ball, bowl again!!!")
                ballsInOver -= 1
            elif ballResult == 8 : #no ball
                print("No ball, bowl a free hit!!!")
                ballsInOver -= 1
            elif ballResult == 9: #wicket
                
                if(wicketsTaken == noOfPlayers-1):  #all out
                    print("ALL OUT!!!")
                    break
                currentBatsman = max(currentBatsman, nonStriker) + 1
                teamA[currentBatsman].condition = "NotOut" #new batsman
        
        print(f"Over {i+1} : [" + " , ".join(overHistory) + "]")
        print(f"Runs after over {i+1} = {totalRuns}")
        inning1.write(f"Over {i+1} : [" + " , ".join(overHistory) + "]\n")
        print("\n")
        currentBatsman, nonStriker = nonStriker, currentBatsman

#1st innings stats
    print(f"\nTotal runs scored after first innings: {totalRuns} \n\n")
    inning1.write(f"\nTotal runs scored after first innings: {totalRuns} \n")

    print("Batting team stats:")
    inning1.write("\nBatting team stats:\n")
    for i in range(len(teamA)):
        print(f"Batsman{i}: {teamA[i].display()}")
        inning1.write(f"Batsman{i}: {teamA[i].display()}\n")
        
    print("\n\nBowling team stats:")
    inning1.write("\nBowling team stats:\n")
    for i in range(len(teamB)):
        print(f"Bowler{i}: {teamB[i].display()}")
        inning1.write(f"Bowler{i}: {teamB[i].display()}\n")

    inning1.close()

    _ = input("\n\nPress enter to start innings 2: ")

    #--------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------
    #-------------------------------------Second Innings-------------------------------------
    #--------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------

    #clearing the terminal
    try:
        system('clear')
    except :
        system('cls')

    #base initialization
    scoreToBeChased = totalRuns+1
    totalRuns = 0
    wicketsTaken =0
    currentBatsman = 0
    nonStriker = 1
    teamA = initializeBattingTeam(noOfPlayers)
    teamB = initializeBowlingTeam(noOfPlayers)
    
    print("Starting Innings 2: ")
    print(f"Score to be chased --> {scoreToBeChased}\n\n")
    inning2 = open("inning2.txt", "w")
    inning2.write(f"Score to be chased --> {scoreToBeChased}\n\n")

    teamA[currentBatsman].condition = "NotOut" #new batsman
    teamA[nonStriker].condition = "NotOut" #new batsman

    for i in range(overs):
        
        if(wicketsTaken == noOfPlayers-1):  #all out
            break 
        if(totalRuns >= scoreToBeChased):   #runs chased
            break
        
        overHistory = []    #record the over
        ballsInOver = 1     #no. of balls bowled in that over
        
        try:
            currentBowler = int(input(f"Enter bowler id(0-{noOfPlayers-1}) for over {i+1}: "))
            if not currentBowler in range(noOfPlayers):
                raise Exception
        except:
            print("Invalid Input...Try again!!!")
            currentBowler = int(input(f"Enter bowler id(0-{noOfPlayers-1}) for over {i+1}: "))

        while(ballsInOver<=6):
            print(f"\nEnter the outcome for ball {i}.{ballsInOver} :", end="")
            print(bowlingOutcomes())
            try:
                ballResult = int(input("Outcome --> "))
                if not ballResult in range(10):
                    raise Exception
            except:
                print("Invalid input!!! Enter again")
                continue

            outcome = outcomeExecution(ballResult, currentBatsman, currentBowler)
            ballsInOver += 1

            overHistory.append(outcome)

            if ballResult in [1,3,5]: #odd runs
  	    # to change the batsman on strike
                currentBatsman, nonStriker = nonStriker, currentBatsman
            elif ballResult == 7 : #wide ball
                print("Wide ball, bowl again!!!")
                ballsInOver -= 1
            elif ballResult == 8 : #no ball
                print("No ball, bowl a free hit!!!")
                ballsInOver -= 1
            elif ballResult == 9: #wicket
                if(wicketsTaken == noOfPlayers-1):  #all out
                    print("ALL OUT!!!")
                    break
                currentBatsman = max(currentBatsman, nonStriker) + 1
                teamA[currentBatsman].condition = "NotOut" #new batsman
            
            # if runs chased
            if(totalRuns >= scoreToBeChased): 
                break
        
        print(f"\nOver {i+1} : [" + " , ".join(overHistory) + "]")
        print(f"Runs after over {i+1} = {totalRuns}")
        print(f"Runs required--> {scoreToBeChased-totalRuns}")
        inning2.write(f"Over {i+1} : [" + " , ".join(overHistory) + "]\n")
        print("\n")
        currentBatsman, nonStriker = nonStriker, currentBatsman

    if totalRuns >= scoreToBeChased:
        print("Score Chased!!!!")
        inning2.write("\nScore Chased!!!!\n")
    elif(totalRuns == scoreToBeChased-1):
        print("Match Drawn!!!!")
        inning2.write("\nMatch Drawn!!!!\n")
    elif(totalRuns < scoreToBeChased-1):
        print("Match Lost!!!!")
        inning2.write(f"\nMatch Lost by {scoreToBeChased-1-totalRuns}!!!!\n")
#2nd innings stats

    print(f"\nTotal runs scored in second innings: {totalRuns} \n")
    inning2.write(f"\nTotal runs scored in second innings: {totalRuns} \n")

    print("Batting team stats:")
    inning2.write("\nBatting team stats:\n")
    for i in range(len(teamA)):
        print(f"Batsman{i}: {teamA[i].display()}")
        inning2.write(f"Batsman{i}: {teamA[i].display()}\n")
        
    print("\nBowling team stats:")
    inning2.write("\nBowling team stats:\n")
    for i in range(len(teamB)):
        print(f"Bowler{i}: {teamB[i].display()}")
        inning2.write(f"Bowler{i}: {teamB[i].display()}\n")
    inning2.close()


# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:21:14 2024

A fun script developed in my PD time.
- Plots position or margin of desired number of tipsters. 
- 

@author: giuseppe.caporaso
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.image as image
# from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from tipping_func import *
import seaborn as sns
# from tkinter import *
# from tkinter import tk
sns.set()

# Load in all the excel files, there should be one per round, and the spreadsheet that records who tipped what. 
tips, fixture = loaddf('.\\')

# Initialise key variables


def generateladder(tips, fixture):
    no_users = int(tips.nunique()["NAME"])
    tipstername = np.sort(tips["NAME"].unique()).tolist()
    rounds = np.arange(0,int(len(tips)/no_users))
    teams = np.sort(fixture['Home Team'].unique()).tolist()
    teamshort = ['ADL','BRIS','CARL','COL','ESS','FRE','GWS','GEEL','GCS','HAW','MEL','NTH','PORT','RICH','STK','SYD','WCE','WB']
    teamsdf = pd.DataFrame()
    teamsdf['Team'] = teams
    teamsdf['Teamshort'] = teamshort
    
    # Manually reload data?
    reload=False
    
    try:
        homeawayresult
        totalperteamhome
        totalperteamaway
        correct
    except NameError:
        loadflag = True
        #print("Preparing data..")
    else:
        loadflag = False
        #print("Data appears loaded. To manually retry, set reload to true.")
        
    if reload:
        del homeawayresult, totalperteamhome, totalperteamaway, correct
    
        
    if (loadflag | reload):
        fixture_home_score = []
        fixture_away_score = []
        for i in range(len(fixture)):
            # The first 4 games are in 'Opening Round' which annoyingly labels the round as a string not a number, so just manually filter this for now.
            if (i < 4):
                fixture_home_score.append(int(fixture['Result'][i][0:3]))
                fixture_away_score.append(int(fixture['Result'][i][-3:]))
            # limit for now as the round havent completed yet.
            elif (fixture['Round'][i] <= max(rounds)):
                fixture_home_score.append(int(fixture['Result'][i][0:3]))
                fixture_away_score.append(int(fixture['Result'][i][-3:]))
                
        # Home tips are given a "1" and away "0"
        # However, fixture_score home scores are in row 1, and away in row 0.
        fixture_score = [fixture_away_score, fixture_home_score]
        homeawayresult = pd.DataFrame()
        homeawayresult['Team'] = teams   
        homeawayresult['Wins Home'] = 0
        homeawayresult['Wins Away'] = 0
        homeawayresult['Draw Home'] = 0
        homeawayresult['Draw Away'] = 0
        homeawayresult['Lose Home'] = 0
        homeawayresult['Lose Away'] = 0
        totalperteamhome = pd.DataFrame()
        totalperteamhome['Home Team'] = teams
        totalperteamaway = pd.DataFrame()
        totalperteamaway['Away Team'] = teams
        for i in tipstername:    
            totalperteamhome[i] = 0
            totalperteamaway[i] = 0
        correcthome = totalperteamhome.copy()
        correctaway = totalperteamaway.copy()
        
        for i in range(0,len(fixture_score[0])):
            if (i % 2 == 0):
                print("Loading data.. ", int(round(i/len(fixture_score[0]),2)*100), "%")   
            
            # If the home score is greater than the away score, home team wins. 
            if (fixture_score[1][i] > fixture_score[0][i]):
                homeawayresult.loc[(homeawayresult['Team']==fixture['Home Team'][i]), 'Wins Home'] += 1
                homeawayresult.loc[(homeawayresult['Team']==fixture['Away Team'][i]), 'Lose Away'] += 1
                
                for j in tipstername:   
                    # If that tipster backed the home team that won i.e the fixture dataframe will contain a "1" for that match and tipster
                    if (fixture.iloc[i][j] == 1):
                        # Create a tally of which tipsters tipped what and where, even if they're not right.
                        totalperteamhome.loc[totalperteamhome['Home Team']==fixture['Home Team'][i], j] += 1
                        correcthome.loc[correcthome['Home Team']==fixture['Home Team'][i],j] += 1
                        
                        
                    # Otherwise, they backed the away team (a zero is in that element).
                    elif (fixture.iloc[i][j] == 0):
                        totalperteamaway.loc[totalperteamaway['Away Team']==fixture['Away Team'][i], j] += 1
        
                    # Uh oh spaghettio's! They forgot to tip
                    #else:
                        
            # In this case, the away team won so check if the tipster has a "0" for that match in the fixture df.            
            elif (fixture_score[1][i] < fixture_score[0][i]):
                homeawayresult.loc[(homeawayresult['Team']==fixture['Away Team'][i]), 'Wins Away'] += 1
                homeawayresult.loc[(homeawayresult['Team']==fixture['Home Team'][i]), 'Lose Home'] += 1
        
                for j in tipstername: 
                    # Same setup as before, tipster backed the away team and they won.
                    if (fixture.iloc[i][j] == 0):
                        #.iloc[i][j] = 1
                        totalperteamaway.loc[totalperteamaway['Away Team']==fixture['Away Team'][i], j] += 1
                        correctaway.loc[correctaway['Away Team']==fixture['Away Team'][i],j] += 1
        
        
                    elif (fixture.iloc[i][j] == 1):
                        totalperteamhome.loc[totalperteamhome['Home Team']==fixture['Home Team'][i], j] += 1
        
                    #else:
            
            else:
                # Its a draw! Everybody wins! Still isolate whether a tipster backed the home or away team.
                homeawayresult.loc[(homeawayresult['Team']==fixture['Home Team'][i]), 'Draw Home'] += 1
                homeawayresult.loc[(homeawayresult['Team']==fixture['Away Team'][i]), 'Draw Away'] += 1
                
                for j in tipstername: 
                    if (fixture.iloc[i][j] == 0):
                        totalperteamaway.loc[totalperteamaway['Away Team']==fixture['Away Team'][i], j] += 1
                        correctaway.loc[correctaway['Away Team']==fixture['Away Team'][i],j] += 1
                        
                    elif (fixture.iloc[i][j] == 1):
                        totalperteamhome.loc[totalperteamhome['Home Team']==fixture['Home Team'][i], j] += 1
                        correcthome.loc[correcthome['Home Team']==fixture['Home Team'][i],j] += 1
                    
                    # Forgot to tip catchall.
                    #else:                      
        correct = correcthome.iloc[:, 1:no_users+1] + correctaway.iloc[:, 1:no_users+1]
        loadflag=False
        
    
    # Per team plot
    totalwins, totalwinshome, totalwinsaway = [[] for x in range(3)]
    for i in range(len(teams)):
        # This section is for when one/several tipster views all teams.
        totalwins.append(homeawayresult.loc[homeawayresult['Team']==teams[i], ['Wins Home','Wins Away']].sum().sum())
        totalwinshome.append(homeawayresult.loc[homeawayresult['Team']==teams[i], 'Wins Home'].sum())
        totalwinsaway.append(homeawayresult.loc[homeawayresult['Team']==teams[i], 'Wins Away'].sum())
        
    # How many times total did a given tipster tip a team?
    totalperteam = totalperteamhome.iloc[:, 1:no_users+1] + totalperteamaway.iloc[:, 1:no_users+1]
    totalperteam.insert(0, "Team", teams)
    winsanddraws = homeawayresult['Wins Home']+homeawayresult['Wins Away']+homeawayresult['Draw Home']+homeawayresult['Draw Away']
    winsanddrawshome = homeawayresult['Wins Home']+homeawayresult['Draw Home']
    winsanddrawsaway = homeawayresult['Wins Away']+homeawayresult['Draw Away']
    
    
    teamshort = ['ADL','BRIS','CARL','COL','ESS','FRE','GWS','GEEL','GCS','HAW','MEL','NTH','PORT','RICH','STK','SYD','WCE','WB']
    teamsdf = pd.DataFrame()
    teamsdf['Team'] = teams
    teamsdf['Teamshort'] = teamshort
    # Start at one and add one because the first column is the team. 
    
    del correcthome['Home Team']
    del correctaway['Away Team']
    del totalperteamhome['Home Team']
    del totalperteamaway['Away Team']
    
    propperteam = correct.T.astype(float).div(totalperteam.T.iloc[1:, 0:].astype(float))
    propperteam.fillna(0, inplace=True)
    
    propperteamhome = correcthome.T.astype(float).div(totalperteamhome.T.iloc[:, :].astype(float))
    propperteamhome.fillna(0, inplace=True)
    
    propperteamaway = correctaway.T.astype(float).div(totalperteamaway.T.iloc[:, :].astype(float))
    propperteamaway.fillna(0, inplace=True)
    
    #return(no_users)

# This plot is for all teams, one tipster.
def teamsscoresheet(tipster, order, totalperteam, winsanddraws, correct, teamsdf):
    newindex = []
    if (order=='Correct Tips'):
        newindex = correct[tipster].sort_values(ascending=False).index
    elif (order=='Total Tips'):
        newindex = totalperteam[tipster].sort_values(ascending=False).index  
    teamsdf = teamsdf.loc[newindex]
    totalperteam = totalperteam.loc[newindex]
    correct = correct.loc[newindex]
    winsanddraws = winsanddraws.loc[newindex]
        
    x_ax = np.arange(len(teamsdf.iloc[:,1:2]))
    barwidth = 0.25
    plt.figure(figsize=(16,9))
    plt.bar(x_ax-barwidth, totalperteam[tipster], barwidth, label="Total Tips", align='center', edgecolor='black')
    plt.bar(x_ax, winsanddraws, barwidth, align='center', label="Total Wins & Draws", edgecolor='black')
    plt.bar(x_ax+barwidth, correct[tipster], barwidth, label="Correct Tips", align='center', edgecolor='black')
    
    plt.title(tipster+" Score Sheet", fontsize=20)
    bar_settings(list(teamsdf['Teamshort']), 'Teams', x_ax)
    
def tipstersscoresheet(team, order, totalperteam, winsanddraws, correct, teamsdf):
    
    x_ax = np.arange(len(range(0, correct.shape[1])))
    barwidth = 0.25
    plt.figure(figsize=(16,9))
    newindex = []
    if (order=='Correct Tips'):
        newindex = correct.T[teamsdf.loc[teamsdf['Team']==team].index[0]].sort_values(ascending=False).index
    elif (order=='Total Tips'):
        newindex = totalperteam.T[teamsdf.loc[teamsdf['Team']==team].index[0]][1:].sort_values(ascending=False).index
        
    df1 = totalperteam.T.loc[newindex]
    df2 = correct.T.loc[newindex]
    df3 = winsanddraws.loc[teamsdf['Team']==team]
    # This plot is for all teams, one tipster.
    plt.bar(x_ax-0.5*barwidth, df1[teamsdf.loc[teamsdf['Team']==team].index[0]], barwidth, label="Total Tips", align='center', edgecolor='black')
    plt.hlines(y=df3, xmin=0, xmax=23, color='grey', label=team+" Wins & Draws")
    plt.bar(x_ax+0.5*barwidth, df2[teamsdf.loc[teamsdf['Team']==team].index[0]], barwidth, label="Correct Tips", align='center', edgecolor='black')
    
    plt.title(team+" Across Tipsters", fontsize=20)
    bar_settings(newindex, 'Tipsters', x_ax)
    
def propsheet(team, propperteam, totalperteam, correct, teamsdf):
    
    x_ax = np.arange(len(correct.columns))
    barwidth = 0.4
    plt.figure(figsize=(16,9))
    newindex = propperteam[teamsdf.loc[teamsdf['Team']==team].index[0]].sort_values(ascending=False).index
    
    proportion = round(propperteam.iloc[:, teamsdf.loc[teamsdf['Team']==team].index[0]],2)*100
    proportion = round(proportion.loc[newindex],2)
    proportion = [int(x) for x in proportion]
    
    
    # Find the new index by proportion.
    df1 = totalperteam.T.loc[newindex]
    df2 = correct.T.loc[newindex]
    
    # This plot is for all teams, one tipster.
    plt.plot([], [], color='none', label="Success Rate (%)")
    plt.bar(x_ax, df1[teamsdf.loc[teamsdf['Team']==team].index[0]], barwidth, label="Total Tips", align='center', edgecolor='black')
    #plt.hlines(y=df3, xmin=0, xmax=23, color='grey', label=team+" Wins & Draws")
    plt.bar(x_ax, df2[teamsdf.loc[teamsdf['Team']==team].index[0]], barwidth, label="Correct Tips", align='center', edgecolor='black')
    for i, v in enumerate(proportion):
        plt.text(x_ax[i]-0.25, df1[teamsdf.loc[teamsdf['Team']==team].index[0]][i]+0.1, str(v)+"%")
    
    plt.title(team+" across all tipsters \nOrdered by success rate", fontsize=20)
    bar_settings(newindex, 'Tipsters', x_ax)


def margin_per_round(tipster, full_name_flag, no_users=int(tips.nunique()["NAME"])):
    rounds = np.arange(0,int(len(tips)/no_users))
    cm_1 = plt.get_cmap('gist_ncar_r')
    # Does the username exist? 
    if not(bool(tipster)) or '' in tipster:
        plt.figure(figsize=(12, 8))
        margin_per_user, margin_profile = calc_margin(tips, rounds, no_users)
        for user in range(no_users):  
            if full_name_flag:
                plt.plot(rounds, margin_per_user[user], label=dict_user_names[margin_profile[-1]['NAME'].iloc[user]], linewidth=4, color=cm_1(user*10+15)) 
            else:
                plt.plot(rounds, margin_per_user[user], label=margin_profile[-1]['NAME'].iloc[user], linewidth=4, color=cm_1(user*10+15))
            
    else:       
        margin_per_user, margin_profile = calc_margin(tips, rounds, no_users)
        df = margin_profile[-1]
        save_tipster = list_input(tipster, df, no_users)
        plt.figure(figsize=(12, 8))
        for user in range(0, no_users):
            # This converts the negative number (to access the most recent round) into an index where the name is positioned in terms
            # of rank in the most recent round.
            if (user-no_users) in save_tipster:
                # Again, -25 brings us to the most recent round which is ordered.
                if full_name_flag:
                    plt.plot(rounds, margin_per_user[user], label=dict_user_names[margin_profile[-1]['NAME'].iloc[user]], linewidth=4, color=cm_1(user*10+15))   
                else:
                    plt.plot(rounds, margin_per_user[user], label=margin_profile[-1]['NAME'].iloc[user], linewidth=4, color=cm_1(user*10+15))   

                
            else:
                # Everyone else appears grey
                if full_name_flag:
                    plt.plot(rounds, margin_per_user[user], label=dict_user_names[margin_profile[-1]['NAME'].iloc[user]], linewidth=1, color='grey')  
                else:
                    plt.plot(rounds, margin_per_user[user], label=margin_profile[-1]['NAME'].iloc[user], linewidth=1, color='grey')  

    plot_settings(no_users, rounds, 1)
        
def position_per_round(tipster, full_name_flag, no_users=int(tips.nunique()["NAME"])):
    rounds = np.arange(0,int(len(tips)/no_users))
    cm_1 = plt.get_cmap('gist_ncar_r')
    rank_profile = []
    # Does the username exist? 
    if not(bool(tipster)) or '' in tipster:
        plt.figure(figsize=(12, 8))
        # Go through each tipster
        for user in range(0, no_users):
            # This line extracts a tipsters score for each round, along with an index indicating their final position after each round. Very handy!
            rank_profile.append(tips[tips['NAME'] == tips.iloc[user-no_users][1]]['RANK'])
            if full_name_flag:
                plt.plot(rounds, rank_profile[user], label=dict_user_names[tips.iloc[user-no_users][1]], linewidth=4, color=cm_1(user*10+15)) 
            else:
                plt.plot(rounds, rank_profile[user], label=tips.iloc[user-no_users][1], linewidth=4, color=cm_1(user*10+15))                


    else:
        save_tipster = list_input(tipster, tips, no_users)
        plt.figure(figsize=(12, 8))
        for user in range(0, no_users):
            rank_profile.append(tips[tips['NAME'] == tips.iloc[user-no_users][1]]['RANK'])
            # This converts the negative number (to access the most recent round) into an index where the name is positioned in terms
            # of rank in the most recent round.
            if (user-no_users) in save_tipster:
                # Again, -25 brings us to the most recent round which is ordered.
                if full_name_flag:
                    plt.plot(rounds, rank_profile[user], label=dict_user_names[tips.iloc[user-no_users][1]], linewidth=4, color=cm_1(user*10+15))
                else:
                    plt.plot(rounds, rank_profile[user], label=tips.iloc[user-no_users][1], linewidth=4, color=cm_1(user*10+15))

            else:
                # Everyone else appears grey
                if full_name_flag:
                    plt.plot(rounds, rank_profile[user], label=dict_user_names[tips.iloc[user-no_users][1]], linewidth=1, color='grey')
                else:
                    plt.plot(rounds, rank_profile[user], label=tips.iloc[user-no_users][1], linewidth=1, color='grey')

    # Last input is whether its margin (1) or position (0) for title purposes.
    plot_settings(no_users, rounds, 0)

def cumulative_score(round_min, round_max, score_min, score_max):
    cm_1 = plt.get_cmap('gist_ncar_r')
    cscore, dummy = [[] for _ in range(2)]
    round_cols = [2,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,54]
    plt.figure(figsize=(16,9))
    for user in range(-no_users,0):
        # Add 3 because of the indexes that exist before opening round, like rank and name etc.
        for index in rounds:
            dummy.append(tips.iloc[user][round_cols[0:index+1]].sum(axis=0))
        
        cscore.append(dummy)
        dummy = []
        
        plt.plot(rounds, cscore[user+no_users], label=tips.iloc[user][1], linewidth=2, color=cm_1((user+25)*10+15))
        plt.xticks(rounds)
        plt.axis([round_min, round_max, score_min, score_max])
        plt.xlabel('Round', fontsize=16)
        plt.ylabel('Total Score', fontsize=16)
        plt.legend(title='Current Ladder', loc=(1.04, 0.5))
        plt.plot() 

# Tipsters must be entered as a list of strings (in square brackets), even if its a single name.
# position_per_round(['Lee Blucher','PVAnotC'])

#propsheet('Port Adelaide', propperteam, totalperteam, correct, teamsdf)
#propsheet('Gold Coast Suns', propperteamaway, totalperteamaway, correctaway, teamsdf, no_users)
#propsheet('West Coast Eagles', propperteamhome, totalperteamhome, correcthome, teamsdf, no_users)

#tipstersscoresheet('West Coast Eagles', 'Correct Tips', totalperteam, winsanddraws, correct, teamsdf)

# Inputs: Tipster, 'Correct Tips' or 'Total Tips', the rest dont touch.
#teamsscoresheet('AndyT23', 'Correct Tips', totalperteam, winsanddraws, correct, teamsdf)

#def tipsterladder(tipster)





#position_per_round([''])


# Tipsters must be entered as a list of strings (in square brackets), even if its a single name.
#margin_per_round(['AndyT23','DemocracyManifestt'])
#margin_per_round(['CANT1053','DemocracyManifestt','AndyT23'])




# Which span of rounds and points you'd like to view, with min and max as the two inputs.
# No input implies all rounds.
#cumulative_score(14, max(rounds))











#tipsterpic = 'C:\\Users\\giuseppe.caporaso\\Downloads\\tipsterpic'
# Find a way to loop through all images
# pic  = image.imread(os.path.join(tipsterpic,'G_Caporaso.jpg'))

# Checks
# for user in range(no_users):
#     print("Tipster            :",tips.iloc[user-no_users][1])
#     print("Total (spreadsheet):", result[tips.iloc[user-no_users][1]].sum())
#     print("Total (online)     :", tips.iloc[user-no_users][4])

#################### Below code is for home vs away data ##############################
# I need to know the home locations for each team.
# homeloc = []
# awayloc = []
# for i in range(len(teams)):
#     homeloc.append(fixture.loc[fixture['Home Team']==teams[i], 'Location'].unique().tolist())
#     awayloc.append(fixture.loc[fixture['Away Team']==teams[i], 'Location'].unique().tolist())
        

# Find every ground each team has played on.
# no_loc_per_team = []
# for i in teamsdf.iloc[:, 0].tolist():
#     # Append all unqiue locations that satisfy either home or away teams.
#     no_loc_per_team.append(fixture['Location'][(fixture['Home Team']==i) | (fixture['Away Team']==i)].unique())      

# Note, for team input, maybe have a dictionary 
# so various different versions of the names still find the name as defined in the dataframe.
# team_name_variations = {
#     'Adelaide': no_teams[0], 
#     'Crows':    no_teams[0],
#     'Crom':     no_teams[0], 
#     'Brisbane': no_teams[1],
#     'Lions':    no_teams[1],
#     'Blues':    no_teams[2],
#     'The Blues': no_teams[2],
#     'Pies':     no_teams[3],
#     'Magpies':  no_teams[3],
#     'Bombers': no_teams[3]}




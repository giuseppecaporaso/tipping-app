# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:28:54 2024

@author: giuseppe.caporaso
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.image as image
# from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from tipping_func import *
from tipping import *
import seaborn as sns
import itertools
# from tkinter import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QRadioButton, QButtonGroup, QTabWidget
sns.set()

tips, fixture = loaddf('C:\\Users\\giuseppe.caporaso\\Downloads\\tipping_files\\')
tipstername = fixture.columns[7:].tolist()
teamshort = ['ADL','BRIS','CARL','COL','ESS','FRE','GWS','GEEL','GCS','HAW','MEL','NTH','PORT','RICH','STK','SYD','WCE','WB']
teams = sorted(list(fixture['Home Team'].unique()))



whatifscore = pd.DataFrame()
whatifscore['Team'] = teams
for name in tipstername:
    whatifscore[name] = 0

class Tipster:
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.totalscore = self.df['Correct'].sum()
        
    # Total correct tips for a given team and location.
    def get_team_score(self, team, location):
        if (location=='All'):
            self.teamscore = self.df[((self.df['Home Team']==team) & (self.df[self.name]==1)) \
                                    | ((self.df['Away Team']==team) & (self.df[self.name]==0))]['Correct'].sum()
        
        elif (location=='Home'):
            self.teamscore = self.df[(self.df['Home Team']==team) & (self.df[self.name]==1)]['Correct'].sum()
            
            
        elif (location=='Away'):
            self.teamscore = self.df[(self.df['Away Team']==team) & (self.df[self.name]==0)]['Correct'].sum()
            # print(self.df[(self.df['Away Team']==team) & (self.df[self.name]==0)]['Correct'])
            
        # A unique venue has been entered, filter by it. 
        else:
            if (location in self.df['Location'].unique()):
                self.teamscore = self.df[(self.df['Location']==location) & \
                                        (((self.df['Home Team']==team) & (self.df[self.name]==1)) \
                                        | ((self.df['Away Team']==team) & (self.df[self.name]==0)))]['Correct'].sum()
            else:
                raise Exception("Check the spelling on the venue. Here's a list of all defined venues. ", fixture['Location'].unique().tolist())
    
    # Total tipping attempts for a given team and location.            
    def get_team_attempts(self, team, location):
        if (location=='All'):
            self.teamattempts = len(self.df[((self.df['Home Team']==team) & (self.df[self.name]==1)) \
                                    | ((self.df['Away Team']==team) & (self.df[self.name]==0))]['Round'].unique())
        
        elif (location=='Home'):
            self.teamattempts = len(self.df[(self.df['Home Team']==team) & (self.df[self.name]==1)]['Round'].unique())
            
            
        elif (location=='Away'):
            self.teamattempts = len(self.df[(self.df['Away Team']==team) & (self.df[self.name]==0)]['Round'].unique())
            
        # A unique venue has been entered, filter by it. 
        else:
            if (location in self.df['Location'].unique()):
                self.teamattempts = len(self.df[(self.df['Location']==location) & \
                                        (((self.df['Home Team']==team) & (self.df[self.name]==1)) \
                                        | ((self.df['Away Team']==team) & (self.df[self.name]==0)))]['Round'].unique())
            else:
                raise Exception("Check the spelling on the venue. Here's a list of all defined venues. ", fixture['Location'].unique().tolist())
    
    # Total number of wins, draws and losses for a given team and location. 
    def get_team_wins_draws_losses(self, team, location):
        counter = 0
        #self.teamwinsdraws = 1
        if (location=='All'): 
            dummy = self.df[(self.df['Home Team']==team)]
            for index in range(len(dummy)):
                if (pd.isna(dummy['Result'].iloc[index])):
                    continue
                
                if int(dummy['Result'].iloc[index][0:3]) >= int(dummy['Result'].iloc[index][-3:]):
                    counter += 1
                    
            dummy = self.df[(self.df['Away Team']==team)]
            for index in range(len(dummy)):
                if (pd.isna(dummy['Result'].iloc[index])):
                    continue
                
                if int(dummy['Result'].iloc[index][0:3]) <= int(dummy['Result'].iloc[index][-3:]):
                    counter += 1
        
        elif (location=='Home'):
            dummy = self.df[(self.df['Home Team']==team)]
            for index in range(len(dummy)):
                if (pd.isna(dummy['Result'].iloc[index])):
                    continue
                
                if int(dummy['Result'].iloc[index][0:3]) >= int(dummy['Result'].iloc[index][-3:]):
                    counter += 1
            
        elif (location=='Away'):
            dummy = self.df[(self.df['Away Team']==team)]
            for index in range(len(dummy)):
                if (pd.isna(dummy['Result'].iloc[index])):
                    continue
                
                if int(dummy['Result'].iloc[index][0:3]) <= int(dummy['Result'].iloc[index][-3:]):
                    counter += 1
            
        # A unique venue has been entered, filter by it. 
        else:
            if (location in self.df['Location'].unique()):
                dummy = self.df[(self.df['Location']==location) & (self.df['Home Team']==team)]
                for index in range(len(dummy)):
                    if (pd.isna(dummy['Result'].iloc[index])):
                        continue
                
                    if int(dummy['Result'].iloc[index][0:3]) >= int(dummy['Result'].iloc[index][-3:]):
                        counter += 1
                
                dummy = self.df[(self.df['Location']==location) & (self.df['Away Team']==team)]
                for index in range(len(dummy)):
                    if (pd.isna(dummy['Result'].iloc[index])):
                        continue
                
                    if int(dummy['Result'].iloc[index][0:3]) <= int(dummy['Result'].iloc[index][-3:]):
                        counter += 1
        
            else:
                raise Exception("Check the spelling on the venue. Here's a list of all defined venues. ", fixture['Location'].unique().tolist())
        
        self.teamwinsdraws = counter
    
    # Total correct tips for a given tipster across all teams.
    def get_tipster_score_per_team(self, teamlist, location):
        temp, temp2, temp3 = [[] for _ in range(3)]
        if (location=='All'):
            for team in sorted(list(self.df['Home Team'].unique())):
                # We already have 'tipped the team and the team won' (via yscore)
                # Tipped the team but didn't win the tip
                temp.append(-1*len(self.df[(((self.df['Home Team']==team) & (self.df[self.name]==1)) | ((self.df['Away Team']==team) & (self.df[self.name]==0))) & \
                                                      (self.df['Correct']==0)]))

                # Didn't tip the team but the team won (implying that you lost the tip)
                temp2.append(-1*len(self.df[(((self.df['Home Team']==team) & (self.df[self.name]==0)) | ((self.df['Away Team']==team) & (self.df[self.name]==1))) &                  \
                                                (self.df['Correct']==0)]))
                    
                # Didn't tip the team and the team didn't win (implying that you won the tip)
                temp3.append(len(self.df[(((self.df['Home Team']==team) & (self.df[self.name]==0)) | ((self.df['Away Team']==team) & (self.df[self.name]==1))) &                  \
                                                (self.df['Correct']==1)]))
        
        elif (location=='Home'):
            for team in sorted(list(self.df['Home Team'].unique())):
                # Tipped the team but didn't win the tip
                temp.append(-1*len(self.df[((self.df['Home Team']==team) & (self.df[self.name]==1)) & \
                                          (self.df['Correct']==0)]))

                # Didn't tip the team but the team won (implying that you lost the tip)
                temp2.append(-1*len(self.df[((self.df['Home Team']==team) & (self.df[self.name]==0)) & \
                                          (self.df['Correct']==0)]))
                    
                # Didn't tip the team and the team didn't win (implying that you won the tip)
                temp3.append(len(self.df[((self.df['Home Team']==team) & (self.df[self.name]==0)) & \
                                          (self.df['Correct']==1)]))          
        elif (location=='Away'):
            for team in sorted(list(self.df['Home Team'].unique())):
                # Tipped the team but didn't win the tip
                temp.append(-1*len(self.df[((self.df['Away Team']==team) & (self.df[self.name]==0)) & \
                                          (self.df['Correct']==0)]))

                # Didn't tip the team but the team won (implying that you lost the tip)
                temp2.append(-1*len(self.df[((self.df['Away Team']==team) & (self.df[self.name]==1)) & \
                                          (self.df['Correct']==0)]))
                    
                # Didn't tip the team and the team didn't win (implying that you won the tip)
                temp3.append(len(self.df[((self.df['Away Team']==team) & (self.df[self.name]==1)) & \
                                          (self.df['Correct']==1)]))          
            
        else:
            if (location in self.df['Location'].unique()):
                for team in sorted(list(self.df['Home Team'].unique())):
                    # Tipped the team but didn't win the tip
                    temp.append(-1*len(self.df[(self.df['Location']==location) & \
                                            (((self.df['Home Team']==team) & (self.df[self.name]==1)) | ((self.df['Away Team']==team) & (self.df[self.name]==0))) & \
                                                            (self.df['Correct']==0)]))
                    
                    # Didn't tip the team but the team won (implying that you lost the tip)
                    temp2.append(-1*len(self.df[(self.df['Location']==location) & \
                                          (((self.df['Home Team']==team) & (self.df[self.name]==0)) | ((self.df['Away Team']==team) & (self.df[self.name]==1))) & \
                                                          (self.df['Correct']==0)]))
                                       
                    # Didn't tip the team and the team didn't win (implying that you won the tip)
                    temp3.append(len(self.df[(self.df['Location']==location) & \
                                            (((self.df['Home Team']==team) & (self.df[self.name]==0)) | ((self.df['Away Team']==team) & (self.df[self.name]==1))) & \
                                                            (self.df['Correct']==1)]))
            else:
                raise Exception("Check the spelling on the venue. Here's a list of all defined venues. ", fixture['Location'].unique().tolist())

        self.tippedbutdidntwin = temp
        self.didnttipbutwon = temp2
        self.didnttipdidntwin = temp3

# Preallocate a dictionary for the tipsters
tipsters = {}

# Isolate dataframes to have the game info and the tipper in question. 
gamedata = fixture.iloc[:,0:7]
dummy = pd.DataFrame()

# Add a column that tracks whether the tips are correct.
dummy['Correct'] = 0

for name in tipstername:
    # for i in range(len(fixture)):
    temp = fixture[name]
    df = pd.concat([gamedata, temp, dummy], axis=1)
    
    for index in range(len(fixture['Match Number'])):
        if (pd.isna(fixture['Result'][index])):
            continue

        df['Correct'] = df['Correct'].replace(np.nan, 0)
        result = checktip(fixture, name, index)
        df.loc[index, 'Correct'] += result
        
        # Calculate "What If" ladder
        # If zero, they tipped away
        if (int(fixture[name][index])==0):
            whatifscore.loc[teams.index(fixture['Away Team'][index]), name] += 4
            
        # If one, they tipped home
        elif (int(fixture[name][index])==1):
            whatifscore.loc[teams.index(fixture['Home Team'][index]), name] += 4
            
        # Anything else, they didn't tip that game. Award a draw
        else: 
            whatifscore.loc[teams.index(fixture['Home Team'][index]), name] += 2
            whatifscore.loc[teams.index(fixture['Away Team'][index]), name] += 2
        
    tipsters[name] = Tipster(name, df)
    
def plotwhatifladder(whatifscore, variable):
    variable = 'Adam Slimming'
    # print("variable: ", variable)
    plt.figure(figsize=(9,9))
    whatiftipster = whatifscore[['Team', variable]] #.sort_values(by=str(variable), ascending=False)
    df4 = whatiftipster.sort_values(by=str(variable), ascending=False)
    fig, ax = plt.subplots() 
    ax.set_axis_off() 
    data = np.array(whatiftipster[['Team', variable]])
    table = ax.table(cellText = np.array(df4), colLabels = ('Team', variable),  
    cellLoc ='center',  
    loc ='center')
    plt.show()

def rundata(location):
    team='Adelaide Crows' # Just a placeholder- is overwritten later. 
    # Utilise the class methods. 
    
    print(location)
    yscore, yattempts, yteamwinsdraws, ytippedbutdidntwin, ydidnttipdidntwin, ydidnttipbutwon = [[] for _ in range(6)]
    for name in tipstername:
        tipsters[name].get_team_score(team, location)
        tipsters[name].get_team_attempts(team, location)
        tipsters[name].get_team_wins_draws_losses(team, location)
        tipsters[name].get_tipster_score_per_team(team, location)
    
        yscore.append(tipsters[name].teamscore)
        yattempts.append(tipsters[name].teamattempts)
        # yteamwinsdraws will result in just a number. It should be the same number of wins/draws
        # for a given team irrespective of tipster! But I do it this way for consistency.
        yteamwinsdraws.append(tipsters[name].teamwinsdraws)
        ytippedbutdidntwin.append(tipsters[name].tippedbutdidntwin)
        ydidnttipbutwon.append(tipsters[name].didnttipbutwon)
        ydidnttipdidntwin.append(tipsters[name].didnttipdidntwin)
        
    # Form a new data set that breaks down individual tipping selections.
    tscore = []
    for name in tipstername:
        temp = []
        for i in sorted(list(fixture['Home Team'].unique())):
            tipsters[name].get_team_score(i, location)
            temp.append(int(tipsters[name].teamscore))
        tscore.append(temp)
    
    # Compile results into a dataframe purely to make sorting easier. 
    y = pd.DataFrame()
    t = pd.DataFrame()
    
    # Per Tipster
    y['yscore'] = yscore
    y['yattempts'] = yattempts
    y['Name'] = tipstername
    y['yteamwinsdraws'] = yteamwinsdraws
    y = y.sort_values(['yscore','yattempts'], ascending=[False, True])
    
    # Per Team
    t['Name'] = tipstername
    t['Score'] = tscore
    t['ytippedbutdidntwin'] = ytippedbutdidntwin
    t['ydidnttipbutwon'] = ydidnttipbutwon
    t['ydidnttipdidntwin'] = ydidnttipdidntwin
        
    return(t, y)

# 2nd to last variable can be either a tipster name or team name
# The last variable is the option to break down the tips.
def plotbar(t, teams, teamshort, tipstername, location, variable, detailed):
    listcorrect, listwrong, listcorrect2, listwrong2, listtotal, totalcorrectpertipster, totalwrongpertipster, totalpertipster = [[] for _ in range(8)]
    # Some check to see if its a team or tipster
    barwidth = 0.25
    plt.figure(figsize=(9,6))
    if variable in tipstername:
        x_ax = np.arange(len(teams))
        plt.title(variable+" Across All Teams\n Location - "+location, fontsize=18)
        plt.xlabel('Teams', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        for i in range(len(teams)):
            if detailed:
                listcorrect.append(list(t[t['Name']==variable]['Score'])[0][i])#, barwidth, color='blue', label="Tipped and team won", align='center', edgecolor='black')
                listcorrect2.append(list(t[t['Name']==variable]['ydidnttipdidntwin'])[0][i])#, barwidth, color='deepskyblue', label="Didn't tip and team lost/drew", align='center', edgecolor='black')
                listwrong.append(list(t[t['Name']==variable]['ydidnttipbutwon'])[0][i])#, barwidth, color='pink', label="Didn't tip and team won", align='center', edgecolor='black')
                listwrong2.append(list(t[t['Name']==variable]['ytippedbutdidntwin'])[0][i])#, barwidth, color='red', label="Tipped and team lost/drew", align='center', edgecolor='black')
            else:
                listcorrect.append(list(t[t['Name']==variable]['Score'])[0][i] + list(t[t['Name']==variable]['ydidnttipdidntwin'])[0][i])
                listwrong.append(list(t[t['Name']==variable]['ytippedbutdidntwin'])[0][i] + list(t[t['Name']==variable]['ydidnttipbutwon'])[0][i])

    elif variable in teams:
        teamidx = teams.index(variable)
        x_ax = np.arange(len(tipstername))
        plt.title(variable+" Across All Tipsters\n Location - "+location, fontsize=18)
        plt.xlabel('Tipsters', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        for name in tipstername:
            if detailed:
                listcorrect.append(list(t[t['Name']==name]['Score'])[0][teamidx])#, barwidth, color='blue', label="Tipped and team won", align='center', edgecolor='black')
                listcorrect2.append(list(t[t['Name']==name]['ydidnttipdidntwin'])[0][teamidx])#, barwidth, color='deepskyblue', label="Didn't tip and team lost/drew", align='center', edgecolor='black')
                listwrong.append(list(t[t['Name']==name]['ydidnttipbutwon'])[0][teamidx])#, barwidth, color='pink', label="Didn't tip and team won", align='center', edgecolor='black')
                listwrong2.append(list(t[t['Name']==name]['ytippedbutdidntwin'])[0][teamidx])#, barwidth, color='red', label="Tipped and team lost/drew", align='center', edgecolor='black')
            else:
                listcorrect.append(list(t[t['Name']==name]['Score'])[0][teamidx] + list(t[t['Name']==name]['ydidnttipdidntwin'])[0][teamidx])
                listwrong.append(list(t[t['Name']==name]['ytippedbutdidntwin'])[0][teamidx] + list(t[t['Name']==name]['ydidnttipbutwon'])[0][teamidx])
            
    else:
        raise Exception("Can't find the requested tipster or team. Please check spelling.")
        
    for i in range(len(listcorrect)):
        if detailed:
            listtotal.append(listcorrect[i] + listcorrect2[i] + listwrong[i] + listwrong2[i])
        else:    
            listtotal.append(listcorrect[i] + listwrong[i])
        
    totalidx = sorted(range(len(listtotal)), key=lambda k: listtotal[k], reverse=True)
    listtotal = sorted(listtotal, reverse=True)
    listcorrect = rearrange(listcorrect, totalidx)
    listwrong = rearrange(listwrong, totalidx)
    if detailed: listcorrect2 = rearrange(listcorrect2, totalidx)
    if detailed: listwrong2 = rearrange(listwrong2, totalidx)


    if detailed:
        plt.bar(x_ax-0.5*barwidth, listcorrect, barwidth, color='blue', label="Tipped and team won", align='center', edgecolor='black')
        plt.bar(x_ax+0.5*barwidth, listcorrect2, barwidth, color='deepskyblue', label="Didn't tip and team lost/drew", align='center', edgecolor='black')
        plt.bar(x_ax+0.5*barwidth, listwrong, barwidth, color='pink', label="Didn't tip and team won", align='center', edgecolor='black')
        plt.bar(x_ax-0.5*barwidth, listwrong2, barwidth, color='red', label="Tipped and team lost/drew", align='center', edgecolor='black')
        
    else:
        plt.bar(x_ax-0.5*barwidth, listcorrect, label="Correctly tipped \n(inc. not tipping the defeated team)")
        #plt.hlines(y['yteamwinsdraws'][0], xmin=0, xmax=len(tipsters)-1, color='grey', label=chosenteam+" Wins (& Draws) \nTotal: "+str(y['yteamwinsdraws'][0]))
        plt.bar(x_ax-0.5*barwidth, listwrong, label="Incorrectly tipped", color='tomato')
        plt.bar(x_ax-0.5*barwidth, listtotal, color='black', alpha=0.5, label="Net score")

    if variable in tipstername:
        if detailed: plt.hlines(0, xmin=0, xmax=len(teamshort)-1, color='black', linewidth=1)
        teamshort = rearrange(teamshort, totalidx)
        plt.xticks(x_ax, teamshort, rotation=90, fontsize=8)
        # plt.xlabel('Teams', fontsize=12)
    
    elif variable in teams:
        if detailed: plt.hlines(0, xmin=0, xmax=len(tipstername)-1, color='black', linewidth=1)
        tipstername = rearrange(tipstername, totalidx)
        plt.xticks(x_ax, tipstername, rotation=90, fontsize=8)
        # plt.ylabel('Score', fontsize=12)

    plt.locator_params(axis='y', integer=True, tight=True)
    plt.grid(axis='y', linewidth=0.5)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=8)
    plt.tight_layout()
    plt.show() 

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = None
        self.setWindowTitle('Tipping App')
        self.setGeometry(100, 100, 400, 400)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        # show the window
        self.show()
        
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
    
        # # create a grid layout
        # layout = QVBoxLayout()
        # self.setLayout(layout)
    
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(400,400)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Compare Tipsters/Teams")
        self.tabs.addTab(self.tab2,"Rank by Position")
        self.tabs.addTab(self.tab3,"Rank by Margin")
        self.tabs.addTab(self.tab4,"What If? Ladder")

        # Tab 1 - Compare Tipsters/Teams

        # Radio buttons to decide between choosing tipster or team
        self.radiobutton1 = QRadioButton("Compare Tipsters", self)
        self.radiobutton2 = QRadioButton("Compare Teams", self)
        self.radiobutton1.move(10, 20)
        self.radiobutton2.move(10, 45)
        self.radiobutton1.resize(150, 25)
        self.radiobutton2.resize(150, 25)
        self.radiobutton1.toggled.connect(self.radiobutton1_pushed)
        self.radiobutton2.toggled.connect(self.radiobutton2_pushed)
        self.radiobutton1.setChecked(True)
        
        # create a checkbox, button
        self.checkbox = QCheckBox('Detail', self)
        self.checkbox.move(125, 180)
        self.checkbox.setChecked(False)
        
        # Execute Button to run bar plots
        self.buttonrun = QPushButton('Run!', self)
        self.buttonrun.move(5, 180)

        # # Tipster ComboBox
        self.tipstercombobox = QComboBox(self)
        for name in tipstername:
            self.tipstercombobox.addItems([name])
        self.tipstercombobox.move(105, 110)
        self.tipstercombobox.resize(150, 25)
        
        self.tipstercombobox.currentTextChanged.connect(self.tipsterselected)
        
        # Team ComboBox
        self.teamcombobox = QComboBox(self)
        for i in range(len(sorted(list(fixture['Home Team'].unique())))):
            self.teamcombobox.addItems([sorted(list(fixture['Home Team'].unique()))[i]])
        self.teamcombobox.move(105, 80)
        self.teamcombobox.resize(150, 25)
        
        self.teamcombobox.currentTextChanged.connect(self.teamselected)

        # Location ComboBox
        self.loccombobox = QComboBox(self)
        self.loccombobox.addItems(['All','Home','Away'])
        for i in range(len(fixture['Location'].unique().tolist())):
            self.loccombobox.addItems([sorted(fixture['Location'].unique().tolist())[i]])
        self.loccombobox.move(105, 140)
        self.loccombobox.resize(150, 25)
        
        self.loccombobox.currentTextChanged.connect(self.locselected)

        # Label for tipster input box.
        self.nameLabel = QLabel(self)
        self.nameLabel.resize(100, 25)
        self.nameLabel.setText('Select Tipster: ')
        self.nameLabel.move(5, 110)
        
        # Label for team input box.
        self.teamLabel = QLabel(self)
        self.teamLabel.resize(100, 25)
        self.teamLabel.setText('Select Team: ')
        self.teamLabel.move(5, 80)
        
        # Label for input box.
        self.locLabel = QLabel(self)
        self.locLabel.resize(100, 25)
        self.locLabel.setText('Select Location:')
        self.locLabel.move(5, 140)
        
        # Tab 2 - Pos by rank.
        
        self.label = QLabel("To see specific tipster margin worms, tick their respective box.\nNo ticked boxes will highlight everyone.")
        self.listCheckBox = tipstername
        self.myLabel = ['','','','','','','','','','','','','','','','','','','','','','','','']

        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.myLabel[i] = QLabel()
            self.listCheckBox[i].stateChanged.connect(self.tipsterSelected)
    
        self.launchposbyrank = QPushButton('Go!', self)
        self.launchposbyrank.move(5, 180)
        self.launchposbyrank.clicked.connect(self.ladder)
        # #################### ACTION COMMANDS ###########################
        self.buttonrun.clicked.connect(self.button_pushed)        
        self.checkbox.stateChanged.connect(self.state_changed)
        
        # Tab 1

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.nameLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.tipstercombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.teamLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.teamcombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.locLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.loccombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.radiobutton1)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.radiobutton2)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.checkbox)#, Qt.AlignmentFlag.AlignCenter)
        self.tab1.layout.addWidget(self.buttonrun)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.setLayout(self.tab1.layout)

        # Tab 2
        
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.label)
        self.tab2.layout.addWidget(self.launchposbyrank)#, Qt.AlignmentFlag.AlignRight)
        for i, v in enumerate(self.listCheckBox):
            self.tab2.layout.addWidget(self.listCheckBox[i])#, i)#, Qt.AlignmentFlag.AlignLeft)
            self.tab2.layout.addWidget(self.myLabel[i])#, i)#, Qt.AlignmentFlag.AlignLeft)
            self.listCheckBox[i].stateChanged.connect(self.tipsterSelected)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        # show the window
        # self.show()
        
    def tipsterSelected(self):
        self.chosentipsters = []
        for i in range(len(self.listCheckBox)):
            if (self.listCheckBox[i].isChecked()):
                self.chosentipsters.append(self.listCheckBox[i].text())
                
        return(self.chosentipsters)

    def ladder(self):
        generateladder(tips, fixture)
        position_per_round(self.chosentipsters)
        
    def WhatIfLadder(self):
        plotwhatifladder(whatifscore, self.tipstercombobox.currentText())

    # def ladderposbyrank(self):
    #     if self.w is None:
    #         self.w = LadderWindow()
    #         self.w.show()
            
    #     else:
    #         self.w.close()
    #         self.w = None
        
    # def ladderposbymarg(self):
    #     if self.w is None:
    #         self.w = MarginWindow()
    #         self.w.show()
            
    #     else:
    #         self.w.close()
    #         self.w = None
    
    def tipsterselected(self, s):
        print()
        
    def teamselected(self, s):
        print()
        
    def locselected(self, s):
        print(self.loccombobox.currentText())

    def button_pushed(self):
        print(str(self.loccombobox.currentText()))
        t, y = rundata(str(self.loccombobox.currentText()))
        if self.radiobutton2.isChecked():
            plotbar(t, teams, teamshort, tipstername, str(self.loccombobox.currentText()), str(self.tipstercombobox.currentText()), self.checkbox.isChecked())
        else:
            plotbar(t, teams, teamshort, tipstername, str(self.loccombobox.currentText()), str(self.teamcombobox.currentText()), self.checkbox.isChecked())

    def state_changed(self, int):
        print()
    
    # Tipsters!
    def radiobutton1_pushed(self, rb1):
        print()
        #return(rb1)
        
    # Teams!
    def radiobutton2_pushed(self, rb2):
        print()


# class MarginWindow(QWidget):
#     """

#     """
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(100, 100, 400, 400)
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.label = QLabel("To see specific tipster margin worms, tick their respective box.\nNo ticked boxes will highlight everyone.")
#         layout.addWidget(self.label)

#         self.listCheckBox = tipstername
#         self.myLabel = ['','','','','','','','','','','','','','','','','','','','','','','','']

#         for i, v in enumerate(self.listCheckBox):
#             self.listCheckBox[i] = QCheckBox(v)
#             #self.listCheckBox[i].move(125, 20)
#             #self.listCheckBox[i].setStyleSheet("QCheckBox::indicator { width: 10px; height: 2px;}")
#             self.myLabel[i] = QLabel()
#             layout.addWidget(self.listCheckBox[i], i, Qt.AlignmentFlag.AlignLeft)
#             layout.addWidget(self.myLabel[i],    i, Qt.AlignmentFlag.AlignLeft)
            
#             self.listCheckBox[i].stateChanged.connect(self.tipsterSelected)
    
#         self.launchmargbyrank = QPushButton('Go!', self)
#         #self.launchposbyrank.move(5, 180)
#         layout.addWidget(self.launchmargbyrank, Qt.AlignmentFlag.AlignRight)
#         self.launchmargbyrank.clicked.connect(self.ladder)


#     def tipsterSelected(self):
#         self.chosentipsters = []
#         for i in range(len(self.listCheckBox)):
#             if (self.listCheckBox[i].isChecked()):
#                 self.chosentipsters.append(self.listCheckBox[i].text())

#     def ladder(self):
#         generateladder(tips, fixture)
#         margin_per_round(self.chosentipsters)

# class LadderWindow(QWidget):
#     """

#     """
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(100, 100, 400, 400)
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.label = QLabel("To see specific tipster margin worms, tick their respective box.\nNo ticked boxes will highlight everyone.")
#         layout.addWidget(self.label)

#         self.listCheckBox = tipstername
#         self.myLabel = ['','','','','','','','','','','','','','','','','','','','','','','','']

#         for i, v in enumerate(self.listCheckBox):
#             self.listCheckBox[i] = QCheckBox(v)
#             #self.listCheckBox[i].move(125, 20)
#             #self.listCheckBox[i].setStyleSheet("QCheckBox::indicator { width: 10px; height: 2px;}")
#             self.myLabel[i] = QLabel()
#             layout.addWidget(self.listCheckBox[i], i, Qt.AlignmentFlag.AlignLeft)
#             layout.addWidget(self.myLabel[i],    i, Qt.AlignmentFlag.AlignLeft)
            
#             self.listCheckBox[i].stateChanged.connect(self.tipsterSelected)
    
#         self.launchposbyrank = QPushButton('Go!', self)
#         #self.launchposbyrank.move(5, 180)
#         layout.addWidget(self.launchposbyrank, Qt.AlignmentFlag.AlignRight)
#         self.launchposbyrank.clicked.connect(self.ladder)


#     def tipsterSelected(self):
#         self.chosentipsters = []
#         for i in range(len(self.listCheckBox)):
#             if (self.listCheckBox[i].isChecked()):
#                 self.chosentipsters.append(self.listCheckBox[i].text())

#     def ladder(self):
#         generateladder(tips, fixture)
#         position_per_round(self.chosentipsters)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())




# Comparing Teams across one tipster - Breakdown of all four possible tip outcomes per team
# i.e Tipped and team won, Tipped and team lost, Not tipped and team won and Not tipped and team lost.
# x_ax = np.arange(len(teamshort))
# barwidth = 0.20
# plt.figure(figsize=(16,9))
# plt.hlines(0, xmin=0, xmax=len(teamshort)-1, color='black', linewidth=1)
# plt.bar(x_ax-0.5*barwidth, list(t[t['Name']==tipster]['Score'])[0], barwidth, color='blue', label="Tipped and team won", align='center', edgecolor='black')
# plt.bar(x_ax+0.5*barwidth, list(t[t['Name']==tipster]['ydidnttipdidntwin'])[0], barwidth, color='deepskyblue', label="Didn't tip and team lost/drew", align='center', edgecolor='black')
# plt.bar(x_ax+0.5*barwidth, list(t[t['Name']==tipster]['ydidnttipbutwon'])[0], barwidth, color='pink', label="Didn't tip and team won", align='center', edgecolor='black')
# plt.bar(x_ax-0.5*barwidth, list(t[t['Name']==tipster]['ytippedbutdidntwin'])[0], barwidth, color='red', label="Tipped and team lost/drew", align='center', edgecolor='black')
# plt.title(tipster+" Across All Teams\n Location - "+location, fontsize=20)
# plt.xticks(x_ax, teamshort, rotation=90)
# plt.locator_params(axis='y', integer=True, tight=True)
# plt.grid(axis='y', linewidth=0.5)
# plt.xlabel('Teams', fontsize=16)
# plt.ylabel('Score', fontsize=16)
# plt.legend(loc=(1.04, 0.5))
# plt.show() 


# Simplified breakdown of correct vs incorrect tips across all tipsters for one team. 
#x_ax = np.arange(len(y))
# barwidth = 0.25
# plt.figure(figsize=(16,9))
# plt.bar(x_ax-0.5*barwidth, totalcorrectpertipster, label="Correctly tipped \n(inc. not tipping the defeated team)")
# #plt.hlines(y['yteamwinsdraws'][0], xmin=0, xmax=len(tipsters)-1, color='grey', label=chosenteam+" Wins (& Draws) \nTotal: "+str(y['yteamwinsdraws'][0]))
# plt.bar(x_ax-0.5*barwidth, totalwrongpertipster, label="Incorrectly tipped", color='tomato')
# plt.bar(x_ax-0.5*barwidth, totalpertipster, color='black', alpha=0.5, label="Net score")
# plt.title(team+" Across All Tipsters\n Location - "+location, fontsize=20)
# plt.xticks(x_ax, tipstername, rotation=90)
# plt.locator_params(axis='y', integer=True, tight=True)
# plt.grid(axis='y', linewidth=0.5)
# plt.xlabel('Tipsters', fontsize=16)
# plt.ylabel('Score', fontsize=16)
# plt.legend(loc=(1.04, 0.5))
# plt.show()   

   
    


     

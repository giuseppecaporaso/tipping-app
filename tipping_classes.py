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
# from tkinter import *
import qdarktheme
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QGridLayout, QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox, QRadioButton, QButtonGroup, QTabWidget
sns.set()

tips, fixture = loaddf('.\\')
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
    # variable = 'Adam Slimming'
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
def plotbar(t, teams, teamshort, tipstername, location, variable, detailed, full_name_flag):
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
        plt.bar(x_ax-0.5*barwidth, listcorrect, barwidth, color='blue', label="Tipped and team won/drew", align='center', edgecolor='black')
        plt.bar(x_ax+0.5*barwidth, listcorrect2, barwidth, color='deepskyblue', label="Didn't tip and team lost", align='center', edgecolor='black')
        plt.bar(x_ax+0.5*barwidth, listwrong, barwidth, color='pink', label="Didn't tip and team won/drew", align='center', edgecolor='black')
        plt.bar(x_ax-0.5*barwidth, listwrong2, barwidth, color='red', label="Tipped and team lost", align='center', edgecolor='black')
        
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
        if full_name_flag:
            fullname = []
            for name in tipstername:
                fullname.append(dict_user_names[name])
      
            fullname = rearrange(fullname, totalidx)
            plt.xticks(x_ax, fullname, rotation=90, fontsize=8)
        else:
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
        self.setWindowTitle('2024 Aurizn Tipping Analysis GUI')
        self.setGeometry(100, 100, 400, 400)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        # show the window
        self.show()
        
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
    
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(400,400)
        
        self.chosentipsters = []
        
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
        
        # create a checkbox, button
        self.checkbox = QCheckBox('Detail', self)
        self.checkbox.move(125, 180)
        self.checkbox.setChecked(False)
        
        # create a checkbox, button
        self.realnamebox = QCheckBox('Show full names', self)
        self.realnamebox.setChecked(False)
        
        # Execute Button to run bar plots
        self.buttonrun = QPushButton('Run!', self)
        self.buttonrun.move(5, 180)

        # # Tipster ComboBox
        self.tipstercombobox = QComboBox(self)
        for name in tipstername:
            self.tipstercombobox.addItems([name])
        self.tipstercombobox.move(105, 110)
        self.tipstercombobox.resize(150, 25)

        # Tipster ComboBox with real names
        self.tipstercombobox_realname = QComboBox(self)
        for name in dict_names_user:
            self.tipstercombobox_realname.addItems([name])
        self.tipstercombobox_realname.move(105, 110)
        self.tipstercombobox_realname.resize(150, 25)
        self.tipstercombobox_realname.setVisible(False)
        
        # # Tipster ComboBox
        self.tipsterwhatif = QComboBox(self)
        for name in tipstername:
            self.tipsterwhatif.addItems([name])
        self.tipsterwhatif.move(105, 110)
        self.tipsterwhatif.resize(150, 25)
        
        self.tipsterwhatif_realname = QComboBox(self)
        for name in dict_names_user:
            self.tipsterwhatif_realname.addItems([name])
        self.tipsterwhatif_realname.move(105, 110)
        self.tipsterwhatif_realname.resize(150, 25)
        self.tipsterwhatif_realname.setVisible(False)
        
        self.tipsterwhatif.currentTextChanged.connect(self.tipsterselected)
        self.tipsterwhatif.currentTextChanged.connect(self.tipsterselected)
        
        # Team ComboBox
        self.teamcombobox = QComboBox(self)
        for i in range(len(sorted(list(fixture['Home Team'].unique())))):
            self.teamcombobox.addItems([sorted(list(fixture['Home Team'].unique()))[i]])
        self.teamcombobox.move(105, 80)
        self.teamcombobox.resize(150, 25)     
        self.teamcombobox.currentTextChanged.connect(self.teamselected)

        self.tipstercombobox.setDisabled(True)
        if self.radiobutton2.isChecked():
            self.teamcombobox.setDisabled(True)
            self.tipstercombobox.setDisabled(False)

        if self.radiobutton1.isChecked():
            self.teamcombobox.setDisabled(False)
            self.tipstercombobox.setDisabled(True)
            
        self.radiobutton1.setChecked(True)

        # Location ComboBox
        self.loccombobox = QComboBox(self)
        self.loccombobox.addItems(['All','Home','Away'])
        for i in range(len(fixture['Location'].unique().tolist())):
            self.loccombobox.addItems([sorted(fixture['Location'].unique().tolist())[i]])
        self.loccombobox.move(105, 140)
        self.loccombobox.resize(150, 25)
        
        # self.loccombobox.currentTextChanged.connect(self.locselected)

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
        self.label2 = QLabel("To see specific tipster margin worms, tick their respective box.\nNo ticked boxes will highlight everyone.")
        self.label3 = QLabel("What would the ladder look like if every tip you made was correct?\n(Missed tips will be counted as draws.)")
        
        
        self.tipsterposCheckBox1 = QCheckBox(tipstername[0], self)
        self.tipsterposCheckBox1.setChecked(False)
        self.tipsterposCheckBox1.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox2 = QCheckBox(tipstername[1], self)
        self.tipsterposCheckBox2.setChecked(False)
        self.tipsterposCheckBox2.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox3 = QCheckBox(tipstername[2], self)
        self.tipsterposCheckBox3.setChecked(False)
        self.tipsterposCheckBox3.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox4 = QCheckBox(tipstername[3], self)
        self.tipsterposCheckBox4.setChecked(False)
        self.tipsterposCheckBox4.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox5 = QCheckBox(tipstername[4], self)
        self.tipsterposCheckBox5.setChecked(False)
        self.tipsterposCheckBox5.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox6 = QCheckBox(tipstername[5], self)
        self.tipsterposCheckBox6.setChecked(False)
        self.tipsterposCheckBox6.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox7 = QCheckBox(tipstername[6], self)
        self.tipsterposCheckBox7.setChecked(False)
        self.tipsterposCheckBox7.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox8 = QCheckBox(tipstername[7], self)
        self.tipsterposCheckBox8.setChecked(False)
        self.tipsterposCheckBox8.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox9 = QCheckBox(tipstername[8], self)
        self.tipsterposCheckBox9.setChecked(False)
        self.tipsterposCheckBox9.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox10 = QCheckBox(tipstername[9], self)
        self.tipsterposCheckBox10.setChecked(False)
        self.tipsterposCheckBox10.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox11 = QCheckBox(tipstername[10], self)
        self.tipsterposCheckBox11.setChecked(False)
        self.tipsterposCheckBox11.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox12 = QCheckBox(tipstername[11], self)
        self.tipsterposCheckBox12.setChecked(False)
        self.tipsterposCheckBox12.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox13 = QCheckBox(tipstername[12], self)
        self.tipsterposCheckBox13.setChecked(False)
        self.tipsterposCheckBox13.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox14 = QCheckBox(tipstername[13], self)
        self.tipsterposCheckBox14.setChecked(False)
        self.tipsterposCheckBox14.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox15 = QCheckBox(tipstername[14], self)
        self.tipsterposCheckBox15.setChecked(False)
        self.tipsterposCheckBox15.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox16 = QCheckBox(tipstername[15], self)
        self.tipsterposCheckBox16.setChecked(False)
        self.tipsterposCheckBox16.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox17 = QCheckBox(tipstername[16], self)
        self.tipsterposCheckBox17.setChecked(False)
        self.tipsterposCheckBox17.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox18 = QCheckBox(tipstername[17], self)
        self.tipsterposCheckBox18.setChecked(False)
        self.tipsterposCheckBox18.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox19 = QCheckBox(tipstername[18], self)
        self.tipsterposCheckBox19.setChecked(False)
        self.tipsterposCheckBox19.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox20 = QCheckBox(tipstername[19], self)
        self.tipsterposCheckBox20.setChecked(False)
        self.tipsterposCheckBox20.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox21 = QCheckBox(tipstername[20], self)
        self.tipsterposCheckBox21.setChecked(False)
        self.tipsterposCheckBox21.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox22 = QCheckBox(tipstername[21], self)
        self.tipsterposCheckBox22.setChecked(False)
        self.tipsterposCheckBox22.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox23 = QCheckBox(tipstername[22], self)
        self.tipsterposCheckBox23.setChecked(False)
        self.tipsterposCheckBox23.stateChanged.connect(self.tipsterSelected)
        
        self.tipsterposCheckBox24 = QCheckBox(tipstername[23], self)
        self.tipsterposCheckBox24.setChecked(False)
        self.tipsterposCheckBox24.stateChanged.connect(self.tipsterSelected)
        
        self.tipstermargCheckBox1 = QCheckBox(tipstername[0], self)
        self.tipstermargCheckBox1.setChecked(False)
        self.tipstermargCheckBox1.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox2 = QCheckBox(tipstername[1], self)
        self.tipstermargCheckBox2.setChecked(False)
        self.tipstermargCheckBox2.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox3 = QCheckBox(tipstername[2], self)
        self.tipstermargCheckBox3.setChecked(False)
        self.tipstermargCheckBox3.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox4 = QCheckBox(tipstername[3], self)
        self.tipstermargCheckBox4.setChecked(False)
        self.tipstermargCheckBox4.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox5 = QCheckBox(tipstername[4], self)
        self.tipstermargCheckBox5.setChecked(False)
        self.tipstermargCheckBox5.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox6 = QCheckBox(tipstername[5], self)
        self.tipstermargCheckBox6.setChecked(False)
        self.tipstermargCheckBox6.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox7 = QCheckBox(tipstername[6], self)
        self.tipstermargCheckBox7.setChecked(False)
        self.tipstermargCheckBox7.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox8 = QCheckBox(tipstername[7], self)
        self.tipstermargCheckBox8.setChecked(False)
        self.tipstermargCheckBox8.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox9 = QCheckBox(tipstername[8], self)
        self.tipstermargCheckBox9.setChecked(False)
        self.tipstermargCheckBox9.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox10 = QCheckBox(tipstername[9], self)
        self.tipstermargCheckBox10.setChecked(False)
        self.tipstermargCheckBox10.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox11 = QCheckBox(tipstername[10], self)
        self.tipstermargCheckBox11.setChecked(False)
        self.tipstermargCheckBox11.stateChanged.connect(self.tipsterSelectedmargin)

        self.tipstermargCheckBox12 = QCheckBox(tipstername[11], self)
        self.tipstermargCheckBox12.setChecked(False)
        self.tipstermargCheckBox12.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox13 = QCheckBox(tipstername[12], self)
        self.tipstermargCheckBox13.setChecked(False)
        self.tipstermargCheckBox13.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox14 = QCheckBox(tipstername[13], self)
        self.tipstermargCheckBox14.setChecked(False)
        self.tipstermargCheckBox14.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox15 = QCheckBox(tipstername[14], self)
        self.tipstermargCheckBox15.setChecked(False)
        self.tipstermargCheckBox15.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox16 = QCheckBox(tipstername[15], self)
        self.tipstermargCheckBox16.setChecked(False)
        self.tipstermargCheckBox16.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox17 = QCheckBox(tipstername[16], self)
        self.tipstermargCheckBox17.setChecked(False)
        self.tipstermargCheckBox17.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox18 = QCheckBox(tipstername[17], self)
        self.tipstermargCheckBox18.setChecked(False)
        self.tipstermargCheckBox18.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox19 = QCheckBox(tipstername[18], self)
        self.tipstermargCheckBox19.setChecked(False)
        self.tipstermargCheckBox19.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox20 = QCheckBox(tipstername[19], self)
        self.tipstermargCheckBox20.setChecked(False)
        self.tipstermargCheckBox20.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox21 = QCheckBox(tipstername[20], self)
        self.tipstermargCheckBox21.setChecked(False)
        self.tipstermargCheckBox21.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox22 = QCheckBox(tipstername[21], self)
        self.tipstermargCheckBox22.setChecked(False)
        self.tipstermargCheckBox22.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox23 = QCheckBox(tipstername[22], self)
        self.tipstermargCheckBox23.setChecked(False)
        self.tipstermargCheckBox23.stateChanged.connect(self.tipsterSelectedmargin)
        
        self.tipstermargCheckBox24 = QCheckBox(tipstername[23], self)
        self.tipstermargCheckBox24.setChecked(False)
        self.tipstermargCheckBox24.stateChanged.connect(self.tipsterSelectedmargin)
    
        self.launchposbyrank = QPushButton('Go!', self)
        self.launchposbyrank.move(5, 180)
        self.launchposbyrank.resize(150, 25)
        self.launchposbyrank.clicked.connect(self.ladder)
        
        self.launchposbymarg = QPushButton('Go!', self)
        self.launchposbymarg.move(5, 180)
        self.launchposbymarg.resize(150, 25)
        self.launchposbymarg.clicked.connect(self.margin)
        
        # Execute Button to run what if table
        self.runwhatif = QPushButton('Run!', self)
        self.runwhatif.move(5, 180)
        # #################### ACTION COMMANDS ###########################
        self.buttonrun.clicked.connect(self.button_pushed)   
        self.realnamebox.clicked.connect(self.realnames_pushed)   
        self.runwhatif.clicked.connect(self.WhatIfLadder)        
        self.checkbox.stateChanged.connect(self.state_changed)
        
        # Tab 1

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.radiobutton1)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.radiobutton2)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.nameLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.tipstercombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.tipstercombobox_realname)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.teamLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.teamcombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.locLabel)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.loccombobox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.checkbox)#, Qt.AlignmentFlag.AlignCenter)
        self.tab1.layout.addWidget(self.realnamebox)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(self.buttonrun)#, Qt.AlignmentFlag.AlignLeft)
        self.tab1.setLayout(self.tab1.layout)
     
        # Tab 2
        
        self.tab2.layout = QGridLayout(self)
        self.tab2.layout.addWidget(self.label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.tab2.layout.addWidget(self.tipsterposCheckBox1, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox2, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox3, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox4, 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox5, 5, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox6, 6, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox7, 7, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox8, 8, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox9, 9, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox10, 10, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox11, 11, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox12, 12, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox13, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox14, 2, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox15, 3, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox16, 4, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox17, 5, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox18, 6, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox19, 7, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox20, 8, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox21, 9, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox22, 10, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox23, 11, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.tipsterposCheckBox24, 12, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab2.layout.addWidget(self.launchposbyrank, 13, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab2.setLayout(self.tab2.layout)
        
        # Tab 3
        
        self.tab3.layout = QGridLayout(self)
        self.tab3.layout.addWidget(self.label2, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.tab3.layout.addWidget(self.tipstermargCheckBox1, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox2, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox3, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox4, 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox5, 5, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox6, 6, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox7, 7, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox8, 8, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox9, 9, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox10, 10, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox11, 11, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox12, 12, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox13, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox14, 2, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox15, 3, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox16, 4, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox17, 5, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox18, 6, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox19, 7, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox20, 8, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox21, 9, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox22, 10, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox23, 11, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.tipstermargCheckBox24, 12, 1, Qt.AlignmentFlag.AlignLeft)
        self.tab3.layout.addWidget(self.launchposbymarg, 13, 0, Qt.AlignmentFlag.AlignLeft)
        self.tab3.setLayout(self.tab3.layout)
        
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.layout.addWidget(self.label3)
        self.tab4.layout.addWidget(self.tipsterwhatif)
        self.tab4.layout.addWidget(self.tipsterwhatif_realname)
        self.tab4.layout.addWidget(self.runwhatif)
        
        self.tab4.setLayout(self.tab4.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # show the window
        # self.show()
        
    def tipsterSelected(self):
        self.chosentipsters = []
        if (self.tipsterposCheckBox1.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox1.text())
        if (self.tipsterposCheckBox2.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox2.text())
        if (self.tipsterposCheckBox3.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox3.text())
        if (self.tipsterposCheckBox4.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox4.text())
        if (self.tipsterposCheckBox5.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox5.text())
        if (self.tipsterposCheckBox6.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox6.text())
        if (self.tipsterposCheckBox7.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox7.text())
        if (self.tipsterposCheckBox8.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox8.text())
        if (self.tipsterposCheckBox9.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox9.text())
        if (self.tipsterposCheckBox10.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox10.text())
        if (self.tipsterposCheckBox11.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox11.text())
        if (self.tipsterposCheckBox12.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox12.text())
        if (self.tipsterposCheckBox13.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox13.text())
        if (self.tipsterposCheckBox14.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox14.text())
        if (self.tipsterposCheckBox15.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox15.text())
        if (self.tipsterposCheckBox16.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox16.text())
        if (self.tipsterposCheckBox17.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox17.text())
        if (self.tipsterposCheckBox18.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox18.text())
        if (self.tipsterposCheckBox19.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox19.text())
        if (self.tipsterposCheckBox20.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox20.text())
        if (self.tipsterposCheckBox21.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox21.text())
        if (self.tipsterposCheckBox22.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox22.text())
        if (self.tipsterposCheckBox23.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox23.text())
        if (self.tipsterposCheckBox24.isChecked()):
            self.chosentipsters.append(self.tipsterposCheckBox24.text())
                
        return(self.chosentipsters)
            
    def tipsterSelectedmargin(self):
        self.chosentipsters = []
        if (self.tipstermargCheckBox1.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox1.text())
        if (self.tipstermargCheckBox2.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox2.text())
        if (self.tipstermargCheckBox3.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox3.text())
        if (self.tipstermargCheckBox4.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox4.text())
        if (self.tipstermargCheckBox5.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox5.text())
        if (self.tipstermargCheckBox6.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox6.text())
        if (self.tipstermargCheckBox7.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox7.text())
        if (self.tipstermargCheckBox8.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox8.text())
        if (self.tipstermargCheckBox9.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox9.text())
        if (self.tipstermargCheckBox10.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox10.text())
        if (self.tipstermargCheckBox11.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox11.text())
        if (self.tipstermargCheckBox12.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox12.text())
        if (self.tipstermargCheckBox13.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox13.text())
        if (self.tipstermargCheckBox14.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox14.text())
        if (self.tipstermargCheckBox15.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox15.text())
        if (self.tipstermargCheckBox16.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox16.text())
        if (self.tipstermargCheckBox17.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox17.text())
        if (self.tipstermargCheckBox18.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox18.text())
        if (self.tipstermargCheckBox19.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox19.text())
        if (self.tipstermargCheckBox20.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox20.text())
        if (self.tipstermargCheckBox21.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox21.text())
        if (self.tipstermargCheckBox22.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox22.text())
        if (self.tipstermargCheckBox23.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox23.text())
        if (self.tipstermargCheckBox24.isChecked()):
            self.chosentipsters.append(self.tipstermargCheckBox24.text())
                
        return(self.chosentipsters)

    def ladder(self):
        generateladder(tips, fixture)
        self.dummy = []
        if self.realnamebox.isChecked():
            for name in self.chosentipsters:
                if name not in tipstername:
                    self.dummy.append(dict_names_user[name])
                else:
                    self.dummy.append(name)
        
        self.chosentipsters = self.dummy
        position_per_round(self.chosentipsters, self.realnamebox.isChecked())
        
    def margin(self):
        generateladder(tips, fixture)
        self.dummy = []
        if self.realnamebox.isChecked():
            for name in self.chosentipsters:
                if name not in tipstername:
                    self.dummy.append(dict_names_user[name])
                else:
                    self.dummy.append(name)
        
        self.chosentipsters = self.dummy
        margin_per_round(self.chosentipsters, self.realnamebox.isChecked())
        
    def WhatIfLadder(self):
        if self.realnamebox.isChecked():
            name_input_whatif = dict_names_user[self.tipsterwhatif_realname.currentText()]
        else:
            name_input_whatif = str(self.tipsterwhatif.currentText())
        
        plotwhatifladder(whatifscore, name_input_whatif)

    
    def tipsterselected(self, s):
        print()
        
    def teamselected(self, s):
        print()
        
    def locselected(self, s):
        print()
        
    def realnames_pushed(self):
        if self.realnamebox.isChecked():
            self.tipstercombobox_realname.setVisible(True)
            self.tipstercombobox.setVisible(False)
            
            self.tipsterwhatif_realname.setVisible(True)
            self.tipsterwhatif.setVisible(False)
            
            self.tipsterposCheckBox1.setText(dict_user_names[self.tipsterposCheckBox1.text()])
            self.tipsterposCheckBox2.setText(dict_user_names[self.tipsterposCheckBox2.text()])
            self.tipsterposCheckBox3.setText(dict_user_names[self.tipsterposCheckBox3.text()])
            self.tipsterposCheckBox4.setText(dict_user_names[self.tipsterposCheckBox4.text()])
            self.tipsterposCheckBox5.setText(dict_user_names[self.tipsterposCheckBox5.text()])
            self.tipsterposCheckBox6.setText(dict_user_names[self.tipsterposCheckBox6.text()])
            self.tipsterposCheckBox7.setText(dict_user_names[self.tipsterposCheckBox7.text()])
            self.tipsterposCheckBox8.setText(dict_user_names[self.tipsterposCheckBox8.text()])
            self.tipsterposCheckBox9.setText(dict_user_names[self.tipsterposCheckBox9.text()])
            self.tipsterposCheckBox10.setText(dict_user_names[self.tipsterposCheckBox10.text()])
            self.tipsterposCheckBox11.setText(dict_user_names[self.tipsterposCheckBox11.text()])
            self.tipsterposCheckBox12.setText(dict_user_names[self.tipsterposCheckBox12.text()])
            self.tipsterposCheckBox13.setText(dict_user_names[self.tipsterposCheckBox13.text()])
            self.tipsterposCheckBox14.setText(dict_user_names[self.tipsterposCheckBox14.text()])
            self.tipsterposCheckBox15.setText(dict_user_names[self.tipsterposCheckBox15.text()])
            self.tipsterposCheckBox16.setText(dict_user_names[self.tipsterposCheckBox16.text()])
            self.tipsterposCheckBox17.setText(dict_user_names[self.tipsterposCheckBox17.text()])
            self.tipsterposCheckBox18.setText(dict_user_names[self.tipsterposCheckBox18.text()])
            self.tipsterposCheckBox19.setText(dict_user_names[self.tipsterposCheckBox19.text()])
            self.tipsterposCheckBox20.setText(dict_user_names[self.tipsterposCheckBox20.text()])
            self.tipsterposCheckBox21.setText(dict_user_names[self.tipsterposCheckBox21.text()])
            self.tipsterposCheckBox22.setText(dict_user_names[self.tipsterposCheckBox22.text()])
            self.tipsterposCheckBox23.setText(dict_user_names[self.tipsterposCheckBox23.text()])
            self.tipsterposCheckBox24.setText(dict_user_names[self.tipsterposCheckBox24.text()])
            
            self.tipstermargCheckBox1.setText(dict_user_names[self.tipstermargCheckBox1.text()])
            self.tipstermargCheckBox2.setText(dict_user_names[self.tipstermargCheckBox2.text()])
            self.tipstermargCheckBox3.setText(dict_user_names[self.tipstermargCheckBox3.text()])
            self.tipstermargCheckBox4.setText(dict_user_names[self.tipstermargCheckBox4.text()])
            self.tipstermargCheckBox5.setText(dict_user_names[self.tipstermargCheckBox5.text()])
            self.tipstermargCheckBox6.setText(dict_user_names[self.tipstermargCheckBox6.text()])
            self.tipstermargCheckBox7.setText(dict_user_names[self.tipstermargCheckBox7.text()])
            self.tipstermargCheckBox8.setText(dict_user_names[self.tipstermargCheckBox8.text()])
            self.tipstermargCheckBox9.setText(dict_user_names[self.tipstermargCheckBox9.text()])
            self.tipstermargCheckBox10.setText(dict_user_names[self.tipstermargCheckBox10.text()])
            self.tipstermargCheckBox11.setText(dict_user_names[self.tipstermargCheckBox11.text()])
            self.tipstermargCheckBox12.setText(dict_user_names[self.tipstermargCheckBox12.text()])
            self.tipstermargCheckBox13.setText(dict_user_names[self.tipstermargCheckBox13.text()])
            self.tipstermargCheckBox14.setText(dict_user_names[self.tipstermargCheckBox14.text()])
            self.tipstermargCheckBox15.setText(dict_user_names[self.tipstermargCheckBox15.text()])
            self.tipstermargCheckBox16.setText(dict_user_names[self.tipstermargCheckBox16.text()])
            self.tipstermargCheckBox17.setText(dict_user_names[self.tipstermargCheckBox17.text()])
            self.tipstermargCheckBox18.setText(dict_user_names[self.tipstermargCheckBox18.text()])
            self.tipstermargCheckBox19.setText(dict_user_names[self.tipstermargCheckBox19.text()])
            self.tipstermargCheckBox20.setText(dict_user_names[self.tipstermargCheckBox20.text()])
            self.tipstermargCheckBox21.setText(dict_user_names[self.tipstermargCheckBox21.text()])
            self.tipstermargCheckBox22.setText(dict_user_names[self.tipstermargCheckBox22.text()])
            self.tipstermargCheckBox23.setText(dict_user_names[self.tipstermargCheckBox23.text()])
            self.tipstermargCheckBox24.setText(dict_user_names[self.tipstermargCheckBox24.text()])
            
        else:
            self.tipstercombobox_realname.setVisible(False)
            self.tipstercombobox.setVisible(True)
            
            self.tipsterwhatif_realname.setVisible(False)
            self.tipsterwhatif.setVisible(True)

            self.tipsterposCheckBox1.setText(dict_names_user[self.tipsterposCheckBox1.text()])
            self.tipsterposCheckBox2.setText(dict_names_user[self.tipsterposCheckBox2.text()])
            self.tipsterposCheckBox3.setText(dict_names_user[self.tipsterposCheckBox3.text()])
            self.tipsterposCheckBox4.setText(dict_names_user[self.tipsterposCheckBox4.text()])
            self.tipsterposCheckBox5.setText(dict_names_user[self.tipsterposCheckBox5.text()])
            self.tipsterposCheckBox6.setText(dict_names_user[self.tipsterposCheckBox6.text()])
            self.tipsterposCheckBox7.setText(dict_names_user[self.tipsterposCheckBox7.text()])
            self.tipsterposCheckBox8.setText(dict_names_user[self.tipsterposCheckBox8.text()])
            self.tipsterposCheckBox9.setText(dict_names_user[self.tipsterposCheckBox9.text()])
            self.tipsterposCheckBox10.setText(dict_names_user[self.tipsterposCheckBox10.text()])
            self.tipsterposCheckBox11.setText(dict_names_user[self.tipsterposCheckBox11.text()])
            self.tipsterposCheckBox12.setText(dict_names_user[self.tipsterposCheckBox12.text()])
            self.tipsterposCheckBox13.setText(dict_names_user[self.tipsterposCheckBox13.text()])
            self.tipsterposCheckBox14.setText(dict_names_user[self.tipsterposCheckBox14.text()])
            self.tipsterposCheckBox15.setText(dict_names_user[self.tipsterposCheckBox15.text()])
            self.tipsterposCheckBox16.setText(dict_names_user[self.tipsterposCheckBox16.text()])
            self.tipsterposCheckBox17.setText(dict_names_user[self.tipsterposCheckBox17.text()])
            self.tipsterposCheckBox18.setText(dict_names_user[self.tipsterposCheckBox18.text()])
            self.tipsterposCheckBox19.setText(dict_names_user[self.tipsterposCheckBox19.text()])
            self.tipsterposCheckBox20.setText(dict_names_user[self.tipsterposCheckBox20.text()])
            self.tipsterposCheckBox21.setText(dict_names_user[self.tipsterposCheckBox21.text()])
            self.tipsterposCheckBox22.setText(dict_names_user[self.tipsterposCheckBox22.text()])
            self.tipsterposCheckBox23.setText(dict_names_user[self.tipsterposCheckBox23.text()])
            self.tipsterposCheckBox24.setText(dict_names_user[self.tipsterposCheckBox24.text()])
            
            self.tipstermargCheckBox1.setText(dict_names_user[self.tipstermargCheckBox1.text()])
            self.tipstermargCheckBox2.setText(dict_names_user[self.tipstermargCheckBox2.text()])
            self.tipstermargCheckBox3.setText(dict_names_user[self.tipstermargCheckBox3.text()])
            self.tipstermargCheckBox4.setText(dict_names_user[self.tipstermargCheckBox4.text()])
            self.tipstermargCheckBox5.setText(dict_names_user[self.tipstermargCheckBox5.text()])
            self.tipstermargCheckBox6.setText(dict_names_user[self.tipstermargCheckBox6.text()])
            self.tipstermargCheckBox7.setText(dict_names_user[self.tipstermargCheckBox7.text()])
            self.tipstermargCheckBox8.setText(dict_names_user[self.tipstermargCheckBox8.text()])
            self.tipstermargCheckBox9.setText(dict_names_user[self.tipstermargCheckBox9.text()])
            self.tipstermargCheckBox10.setText(dict_names_user[self.tipstermargCheckBox10.text()])
            self.tipstermargCheckBox11.setText(dict_names_user[self.tipstermargCheckBox11.text()])
            self.tipstermargCheckBox12.setText(dict_names_user[self.tipstermargCheckBox12.text()])
            self.tipstermargCheckBox13.setText(dict_names_user[self.tipstermargCheckBox13.text()])
            self.tipstermargCheckBox14.setText(dict_names_user[self.tipstermargCheckBox14.text()])
            self.tipstermargCheckBox15.setText(dict_names_user[self.tipstermargCheckBox15.text()])
            self.tipstermargCheckBox16.setText(dict_names_user[self.tipstermargCheckBox16.text()])
            self.tipstermargCheckBox17.setText(dict_names_user[self.tipstermargCheckBox17.text()])
            self.tipstermargCheckBox18.setText(dict_names_user[self.tipstermargCheckBox18.text()])
            self.tipstermargCheckBox19.setText(dict_names_user[self.tipstermargCheckBox19.text()])
            self.tipstermargCheckBox20.setText(dict_names_user[self.tipstermargCheckBox20.text()])
            self.tipstermargCheckBox21.setText(dict_names_user[self.tipstermargCheckBox21.text()])
            self.tipstermargCheckBox22.setText(dict_names_user[self.tipstermargCheckBox22.text()])
            self.tipstermargCheckBox23.setText(dict_names_user[self.tipstermargCheckBox23.text()])
            self.tipstermargCheckBox24.setText(dict_names_user[self.tipstermargCheckBox24.text()])


        return()

    def button_pushed(self):
        t, y = rundata(str(self.loccombobox.currentText()))       
        if self.radiobutton2.isChecked():
            if self.realnamebox.isChecked():
                name_input = dict_names_user[self.tipstercombobox_realname.currentText()]
            else:
                name_input = str(self.tipstercombobox.currentText())
            plotbar(t, teams, teamshort, tipstername, str(self.loccombobox.currentText()), name_input, self.checkbox.isChecked(), self.realnamebox.isChecked())
        else:
            plotbar(t, teams, teamshort, tipstername, str(self.loccombobox.currentText()), str(self.teamcombobox.currentText()), self.checkbox.isChecked(), self.realnamebox.isChecked())

    def state_changed(self, int):
        print()
    
    # Tipsters!
    def radiobutton1_pushed(self):
        if self.radiobutton2.isChecked():
            self.teamcombobox.setDisabled(True)
            self.tipstercombobox.setDisabled(False)
            self.tipstercombobox_realname.setDisabled(False)

        if self.radiobutton1.isChecked():
            self.teamcombobox.setDisabled(False)
            self.tipstercombobox.setDisabled(True)
            self.tipstercombobox_realname.setDisabled(True)

        self.teamcombobox.currentTextChanged.connect(self.teamselected)
        self.tipstercombobox.currentTextChanged.connect(self.tipsterselected)

        return()
        
    # Teams!
    def radiobutton2_pushed(self):
        if self.radiobutton2.isChecked():
            self.teamcombobox.setDisabled(True)
            self.tipstercombobox.setDisabled(False)

        if self.radiobutton1.isChecked():
            self.teamcombobox.setDisabled(False)
            self.tipstercombobox.setDisabled(True)
            
        self.teamcombobox.currentTextChanged.connect(self.teamselected)
        self.tipstercombobox.currentTextChanged.connect(self.tipsterselected)
        return()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainWindow()
    sys.exit(app.exec())



   
    


     

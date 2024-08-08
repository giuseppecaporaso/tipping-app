# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:21:15 2024

Core functions for the tipping.py script

@author: giuseppe.caporaso
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loaddf(directory):
    tips = pd.DataFrame()
    fixture = pd.DataFrame()
    #resultperround = pd.DataFrame()
    
    # Sourced from the ESPN website. One .csv per round required. 
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                temp = pd.read_csv(directory+file)
                # Concat to one pd for ease
                tips = pd.concat([tips, temp], axis=0)
            if file.endswith("UTC.xlsx"):
                fixture = pd.read_excel(directory+file)
                
    return(tips, fixture)

def calc_margin(tips, rounds, no_users):
    margin_profile, margin_per_user, dummy = [[] for _ in range(3)]
    # Go through each round (as opposed to tipster for position)
    for j in rounds:
        margin_profile.append(tips[['NAME','TOTAL MARGIN']][0+no_users*j:no_users+no_users*j].sort_values(by='TOTAL MARGIN', ascending=True))
        margin_profile[j].insert(0, "RANK", list(range(1, no_users+1)))
    
    for user in range(no_users):
        for j in rounds:
            dummy.append(int(margin_profile[j][margin_profile[j]['NAME']==margin_profile[-1].iloc[user][1]]['RANK']))    
        margin_per_user.append(dummy)
        # Clear dummy to prevent repeating data when appending
        dummy = []
    
    return(margin_per_user, margin_profile)

def list_input(tipster, df, no_users):
    save_tipster = []
    for i in tipster:
        # Would be nice to warn the user that they've entered a tipsters name wrong. Maybe
        if (df['NAME'].eq(i).any()):
            # Negative so we only look at the most recent round which is at the end of the dataframe, and is the only round ordered correctly/up to date.
            for j in range(-no_users, 0):
                # If the names match, which it should because how else did we pass the first if statement, save the index to refer to later. 
                if (i==df.iloc[j][1]):
                    save_tipster.append(j)
                    
    return(save_tipster)

def plot_settings(no_users, rounds, margin):
    plt.gca().invert_yaxis()
    plt.xticks(np.arange(min(rounds), max(rounds)+1,1))
    plt.yticks(np.arange(1, no_users+1,1))
    plt.xlabel('Round', fontsize=16)
    plt.ylabel('Position', fontsize=16)
    # Need to adjust title aswell
    if margin:
        plt.title('AURIZN Tipping 2024 \nMargin per round', fontsize=18)
    else:
        plt.title('AURIZN Tipping 2024 \nPosition per round', fontsize=18)
    plt.legend(title='Current Ladder', loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 6}, fontsize=8) 
    plt.show()  

def bar_settings(tick, xlabel, x_ax):
    
    plt.xticks(x_ax, tick, rotation=90)
    plt.locator_params(axis='y', integer=True, tight=True)
    plt.grid(axis='y', linewidth=0.25)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel('Score', fontsize=16)
    plt.legend(loc=(1.0, 0.5))
    plt.tight_layout()
    plt.show()
    
def checktip(fixture, name, index):
    
    homescore = int(fixture['Result'][index][0:3])
    awayscore = int(fixture['Result'][index][-3:])
    
    if (homescore > awayscore) & (int(fixture[name].loc[index]==1)):
        result = 1
    elif (homescore > awayscore) & (int(fixture[name].loc[index]==0)):
        result = 0
    elif (homescore < awayscore) & (int(fixture[name].loc[index]==1)):
        result = 0
    elif (homescore < awayscore) & (int(fixture[name].loc[index]==0)):
        result = 1
    elif (int(fixture[name].loc[index]) not in [0, 1]):
          result = 0 # The tipster did not tip the game!
    else:
        result = 1 # i.e it was a draw
        
    return(result)     
    
def rearrange(list1, order):
    return ([list1[j] for j in order])   
    
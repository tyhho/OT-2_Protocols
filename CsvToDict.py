# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:08:12 2019

@author: Trevor Ho

This script converts plate consolidation information from a csv file into
a text file, which will contain a dictionary that can be copy and pasted into
an Opentrons API file

"""

import pandas as pd

csvData = pd.read_csv('BM004_Screen5_RearrangingDict.csv')

finalLine = ''
for index, row in csvData.iterrows():
    line = '\'' + str(row['source_plate']) + '_' + str(row['source_well']) + '\':\'' \
        + str(row['dest_plate']) + '_' + str(row['dest_well']) + '\',\n'
    finalLine = finalLine + line
    
finalLine = finalLine[:-2]

f = open("BM004_Screen4_RearrangingDict.txt", "w+")
f.write(finalLine)
f.close()
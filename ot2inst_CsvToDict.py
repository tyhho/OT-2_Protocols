# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:08:12 2019

@author: Trevor Ho

This script converts plate consolidation information from a csv file into
a text file, which will contain a dictionary that can be copy and pasted into
an Opentrons API file

"""
import os
import pandas as pd

# TODO: Specify folder location
rootDir = r'W:\Data storage & Projects\PhD Project_Trevor Ho\3_Intein-assisted Bisection Mapping'
folderDir = r'BM005\Screen2_Gain 1000'

# TODO: Specify the csv filemane
csv_fn = 'BM005_Screen2_1000_RearrangingDict_2.csv'

csv_dir = os.path.join(rootDir,folderDir,csv_fn)

csvData = pd.read_csv(csv_dir)

finalLine = ''
for index, row in csvData.iterrows():
    line = '\'' + str(row['source_plate']) + '_' + str(row['source_well']) + '\':\'' \
        + str(row['dest_plate']) + '_' + str(row['dest_well']) + '\',\n'
    finalLine = finalLine + line
    
finalLine = finalLine[:-2]

output_fn = csv_fn.split('.')[0] + '.txt'
outputDir = os.path.join(rootDir,folderDir,output_fn)
f = open(outputDir, "w+")
f.write(finalLine)
f.close()
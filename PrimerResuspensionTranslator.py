# -*- coding: utf-8 -*-
"""
Created on Tue May 14 19:43:42 2019

@author: s1635543
"""
import pandas as pd

# TODO: Specify folder location
#dataRootDir=r'W:\Data storage & Projects\PhD Project_Trevor Ho\3_Intein-assisted Bisection Mapping'
#dataFolderDir='FC014'

#inst_Dir = os.path.join(dataRootDir,dataFolderDir,metafilename)

instDir = 'ot2inst_PrimerResuspension.xlsx'
outputDir = "ot2inst_PrimerResuspension.txt"

# TODO: Define the source slot
source_slot = '5'
source_well = 'A3'

inst_xls= pd.ExcelFile(instDir)
dict_of_inst = {sheet:inst_xls.parse(sheet) for sheet in inst_xls.sheet_names}

# Search for destination sheet & generate instruction lines
dest_df = dict_of_inst.get('destination')

finalLine = ''

for index, dest_property in dest_df.iterrows():
    dest_slot = dest_property['slot']
    dest_well = dest_property['well']
    dest_vol = dest_property['volume']

    line = '\'' + str(source_slot) + '_' + str(source_well) + '->' \
        + str(dest_slot) + '_' + str(dest_well) + '_' + str(dest_vol) + '\',\n'
    finalLine = finalLine + line
    
finalLine = finalLine[:-2]
        
#%% Export instructions as a text file for copying into
        
f = open(outputDir, "w+")
f.write(finalLine)
f.close()
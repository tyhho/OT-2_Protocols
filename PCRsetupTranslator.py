# -*- coding: utf-8 -*-
"""
Created on Fri May 24 21:14:06 2019

@author: Trevor Ho
"""

import pandas as pd

def rearrange_layout(df,row_index_list):
    '''Rearrange a 96-well layout into a DataFrame format'''
    new_slot_df = empty_df
    for char in row_index_list:
        new_slot_row = df.transpose()[char].to_frame('content')
        
        # Retrieve information of well and set it as index
        indexList = new_slot_row.index.tolist()
        for columnIndex in range(len(indexList)):
            indexList[columnIndex] = char + str(indexList[columnIndex])
        new_slot_row['well']=indexList

        # Append to major dataframe of the single metadata
        new_slot_df = new_slot_df.append(new_slot_row,sort=False)
        
    new_slot_df = new_slot_df.dropna()
    return new_slot_df

# General function to convert any 96 / 24-well plate layout to a simple df
    # Key = metadata field
    # Value = metadata dataframes
empty_df = pd.DataFrame(columns = [])

# TODO: Specify folder location

instDir = 'ot2inst_PCRsetup.xlsx'
outputDir = 'ot2inst_PCRsetup.txt'


inst_xls= pd.ExcelFile(instDir)
dict_of_inst = {sheet:inst_xls.parse(sheet) for sheet in inst_xls.sheet_names}

# Search for "slot_setup" file that defines layout of labware
slots_df = dict_of_inst.get('slot_setup')
slots_df.set_index('slot', inplace = True)

# Search for "slot_setup" file that defines layout of labware
slots_df = dict_of_inst.get('slot_setup')
slots_df.set_index('slot', inplace = True)

# Base on labware layout, rearrange all slots into basic df for handling

labware_layout = {
        '96-well plate':['A','B','C','D','E','F','G','H'],
        '1.5 mL tube rack': ['A','B','C','D'],
        '15_50 mL tube rack':['A','B','C'],
        '15 mL tube rack':['A','B','C'],
        '50 mL tube rack':['A','B']
        }

slots_list = {}

for slot in slots_df.itertuples():
    slot_name_str = str(slot.Index)
    slot_labware_type = slot.labware
    slot_row_index_list = labware_layout.get(slot_labware_type)
    slot_content_df = dict_of_inst.get(slot_name_str)
    
    # only perform rearrangement if the slot role was source    
    if slot.role == 'source':
        slot_content_df = rearrange_layout(slot_content_df,slot_row_index_list)
    slots_list.update({slot_name_str:slot_content_df})


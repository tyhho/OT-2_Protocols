# -*- coding: utf-8 -*-
"""
Created on Wed May  8 22:10:09 2019

@author: s1635543
"""


import pandas as pd

# General function to convert any 96 / 24-well plate layout to a simple df
    # Key = metadata field
    # Value = metadata dataframes
empty_df = pd.DataFrame(columns = [])

def rearrange_layout(df,row_index_list):
    '''Rearrange an intuitive 96-well layout into a DataFrame format'''
    new_slot_df = empty_df
    for char in row_index_list:
        new_slot_row = df.transpose()[char].to_frame('content')
        
        # Retrieve information of well and set it as index
        indexList = new_slot_row.index.tolist()
        for columnIndex in range(len(indexList)):
            indexList[columnIndex] = char + str(indexList[columnIndex])
        new_slot_row['well']=indexList
#        new_slot_row.set_index('well', inplace=True)
        
        # Append to major dataframe of the single metadata
        new_slot_df = new_slot_df.append(new_slot_row,sort=False)
        
    new_slot_df = new_slot_df.dropna()
    return new_slot_df

def addMachineLine(existing_inst_line,dest_slot,dest_well,source_df,item_name,item_vol):
    '''Find where the item is, create machine readable instruction line and add to existing line'''
    # Find where the source material was
    # FIXME: missing alerts / solutions for multiple or distributed source wells
    source_record = source_df[source_df['content']==item_name]
    source_slot = source_record['slot'].item()
    source_well = source_record['well'].item()
    
    # Create a new line of machine readable instruction
    new_inst_line = '\'' + item_vol + '$' + source_slot + '_' + source_well + '->' \
    + dest_slot + '_' + dest_well + '\',\n'
    
    # Add line to original line
    updated_inst_lines = existing_inst_line + new_inst_line
    return updated_inst_lines

# TODO: Specify folder location
instDir = 'ot2inst_sequencing_preparation.xlsx'
outputDir = "ot2inst_sequencing_preparation.txt"

inst_xls= pd.ExcelFile(instDir)
dict_of_inst = {sheet:inst_xls.parse(sheet) for sheet in inst_xls.sheet_names}

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

slots_dict = {}

for slot in slots_df.itertuples():
    slot_name_str = str(slot.Index)
    slot_labware_type = slot.labware
    slot_row_index_list = labware_layout.get(slot_labware_type)
    slot_content_df = dict_of_inst.get(slot_name_str)
    # only perform rearrangement if the slot role was source    
    if slot.format == 'intuitive':
        slot_content_df = rearrange_layout(slot_content_df,slot_row_index_list)
    slots_dict.update({slot_name_str:slot_content_df})

# Compile all slots for sources into a single df
source_df = empty_df
source_slots_list = slots_df[slots_df['role']=='source'].index.astype(str).values.tolist()
for source_slot in source_slots_list:
    a_source_df = slots_dict.get(source_slot)
    a_source_df['slot'] = source_slot
    source_df = source_df.append(a_source_df, ignore_index=True)

# Retrieve df containining destination slots and formats
dest_info = slots_df[slots_df['role']=='destination']

# erase variables
del slot_name_str, slot_labware_type, slot_row_index_list
del slot, slots_df, slot_content_df, source_slots_list

finalLine = ''

# Loop through every destination slot and decide case by case the pipetting instructions
for dest_slot_info in dest_info.itertuples():
    dest_slot = str(dest_slot_info.Index)
    dest_slot_df = slots_dict.get(dest_slot)
    
    for request_line in dest_slot_df.itertuples():
        dest_well = request_line.well
        request_items = request_line._asdict()
        del request_items['Index'], request_items['well']
        
        if dest_slot_info.format == 'intuitive':
            item_list = request_items['content'].split('+')
            item_list = list(filter(None,item_list))
            item_vol = str(int(dest_slot_info.global_volume))
            for item in item_list:
                item_name = item.strip()
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
            
        elif dest_slot_info.format == 'df_variable_content':
            for item_info, item_name in request_items.items():
                item_info = item_info.strip()
                item_name = item_name.strip()
                item_vol = item_info.split('_')[1]
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
        
        elif dest_slot_info.format == 'df_variable_volume':
            for item_name, item_vol in request_items.items():
                item_name = item_name.strip()
                item_vol = item_vol.strip()
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)

#%% Export instructions as a text file for copying into
# FIXME: Turn this part into a script writer
        
finalLine = finalLine[:-2]

f = open(outputDir, "w+")
f.write(finalLine)
f.close()
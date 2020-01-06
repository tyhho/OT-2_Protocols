# -*- coding: utf-8 -*-
"""
Created on Wed May  8 22:10:09 2019

@author: Trevor Ho

This instruction translator takes an Excel file (.xlsx) that specifies what the
source plates/racks look like and what the destination wells need to contain.
For each sample/elements that needs to go into a destination well, the script
searches where that sample/elements is among the source plates/racks, and then construct
a machine-parsable line for that sample. All machine-parsable lines are then concataneted
into a .txt file, in which the contents should be directly copy-pasted into the [] of a
list "inst_list" in an accompanying ot2code script.

Input:
    See the example Excel file.
    The Excel file must have a sheet named "slot_setup", which provides the starting
    point for this script to locate where the source and destination slots are.
    "_", "$", and "->" are forbidden characters in any of the inputs.
    
    The "slot_setup" is a table with the header:
        |slot|labware|role|format|global_volume|
    
    slot: int [1-12]. Must be unique. Do not enter strings.
    
    labware: str. Must be one of the following options:
        96-well plate
        1.5 mL tube rack
        15_50 mL tube rack (note that this can be tricky, see the Opentrons labware for well locations)
        15 mL tube rack
        50 mL tube rack
    Strictly speaking, labware can be omitted as long as "format" != "intuitive",
    but it is always a good practice to put it down. Note that this labware is NOT the 
    labware specification to be used in the accompanying ot2code.
    
    role: Either "source" or "destination". No other input accepted.
    
    format: str. Must be one of the following options:
        intuitive
            User-friendly. Good for source with single sample. BAD for destination with
            multiple samples or elements to be consolidated.
            If used for destination, "global_volume" in "slot_setup" sheet must be provided,
            field value should be:
               + sample1 + sample2 + sample3
            Currently, different sample with different volumes not supported for destination,
            and it is strongly discouraged.
        
        df_variable_sample
            Most helpful when all destination wells must receive different samples but
            of the same volume.
            Table must follow the format below:
                |well  |sample1Category_sample1Vol1|sample2Category_sample2Vol2|
                |wellID|sample1                    |sample2                    |
            Example:
                |well|primer1_5|primer2_5|
                |A1  |primer001|primer002|
            The sampleCategory (in the e.g., primer1) is not important and can be anything,
            but it must be separated from the volume by a "_".
                
        df_variable_volume
            Most helpful when all destination wells must receive same sets of samples but
            variable volumes.    
            Table must follow the format below:
                |well  |sample1|sample2|
                |wellID|vol1   |vol2   |
            Example:
                |well|primer001|primer002|
                |A1  |5        |10       |
        
        df_variable_sample_n_volume
            Recommended solution when both the sample and the volume vary among destination wells.
            Table must follow the format below:
                |well  |sample1|vol1|sample2|vol2|sample3|vol3|  <-- note that the header is merely a placeholder
                |wellID|sample1|vol1|sample2|vol2|sample3|vol3|  <-- actual sample name and volume to input
            Example:
                |well|sample1|vol1|sample2  |vol2|sample3  |vol3|sample4  |vol4|
                |A1  |buffer |10  |primer001|5   |primer002|5   |dNTP     |1   |
            The script reads the items as sample1->vol1->sample2->vol2, therefore, the
            order of the columns MUST NOT be changed in the excel file.
    
    global_volume: int. Must be provided if role="destination" and format="intuitive"
    
Output:
    Each machine-parsable line (str) looks like the following:
        vol$sourceSlot_sourceWell->destSlot_destWell
    
    "$" is the delimiter between the volume and the actual transfer movement
    "_" is the delimiter between the slot and the well
    "->" is the delimiter between the source and the destination.
    
    Sometimes, a global volume is specified by the user in the ot2code. In that case,
    the line simplifies to:
        sourceSlot_sourceWell->destSlot_destWell
    However, this would require users to customize the accompanying ot2code.

Limitations: Currently, it is impossible to have the same plate / rack for being
both the source and the destination. Most input checks are missing.

"""

import pandas as pd

def rearrange_layout(df,row_index_list):
    '''Rearrange an intuitive 96-well / 24-well / 6-well layout into a DataFrame format'''
    
    new_slot_df = pd.DataFrame()
    for char in row_index_list:
        new_slot_row = df.transpose()[char].to_frame('sample')
        
        # Retrieve information of well and set it as index
        indexList = new_slot_row.index.tolist()
        for columnIndex in range(len(indexList)):
            indexList[columnIndex] = char + str(indexList[columnIndex])
        new_slot_row['well']=indexList
        
        # Append to major dataframe of the single metadata
        new_slot_df = new_slot_df.append(new_slot_row,sort=False)
        
    new_slot_df = new_slot_df.dropna()
    return new_slot_df

def addMachineLine(existing_inst_line,dest_slot,dest_well,source_df,item_name,item_vol):
    '''Performs the actual mapping of source to destination, then create machine 
    readable instruction line and add to an existing line
    '''
    # Find where the source sample was
    # FIXME: missing alerts / solutions for multiple or distributed source wells
    source_record = source_df[source_df['sample']==item_name]
    source_slot = source_record['slot'].item()
    source_well = source_record['well'].item()
    
    # The item_vol variable is an optional argument for this function.
    # The if-clause below handles such situation by directly omitting it.
    if item_vol:
        item_vol_line = str(item_vol) + '$'
    else:
        item_vol_line = ''
    
    # Create a new line of machine readable instruction
    new_inst_line = '\'' + item_vol_line + source_slot + '_' + source_well + '->' \
    + dest_slot + '_' + dest_well + '\',\n'
    
    # Add the new line to the exisiting line
    updated_inst_lines = existing_inst_line + new_inst_line
    return updated_inst_lines

#%%
# TODO: Specify input and output files location
# Currently, the input files must be under the same directory as that of InstructionTranslator.py
instFile = 'ot2inst_transfer_glycerolstock.xlsx'
outputFile = "ot2inst_transfer_glycerolstock.txt"

inst_xls= pd.ExcelFile(instFile)
dict_of_inst = {sheet:inst_xls.parse(sheet) for sheet in inst_xls.sheet_names}

# Search for "slot_setup" file that defines layout of labware
slots_df = dict_of_inst.get('slot_setup')
slots_df.set_index('slot', inplace = True)

# FIXME: Validation of correct inputs from Excel file

# Base on the labware layout, rearrange all slots into basic df for future processing
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
        slot_content_df.set_index('row', inplace=True)
        slot_content_df = rearrange_layout(slot_content_df,slot_row_index_list)
    slots_dict.update({slot_name_str:slot_content_df})

# Compile all slots for sources into a single df
source_df = pd.DataFrame(columns = [])
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

#%%

# Loop through every destination slot and decide case by case the pipetting instructions
for dest_slot_info in dest_info.itertuples():
    dest_slot = str(dest_slot_info.Index)
    dest_slot_df = slots_dict.get(dest_slot)
    
    for request_line in dest_slot_df.itertuples():
        dest_well = request_line.well
        request_items = request_line._asdict()
        del request_items['Index'], request_items['well']
        
        if dest_slot_info.format == 'intuitive':
            item_list = request_items['sample'].split('+')
            item_list = list(filter(None,item_list))
            item_vol = str(int(dest_slot_info.global_volume))
            for item in item_list:
                item_name = item.strip()
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
            
        elif dest_slot_info.format == 'df_variable_sample':
            for item_info, item_name in request_items.items():
                item_info = str(item_info).strip()
                item_name = str(item_name).strip()
                if item_info.find('_')>0:
                    item_vol = item_info.split('_')[1]
                else:
                    item_vol = ''
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
        
        elif dest_slot_info.format == 'df_variable_volume':
            for item_name, item_vol in request_items.items():
                item_name = item_name.strip()
                item_vol = item_vol.strip()
                finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
                
        elif dest_slot_info.format == 'df_variable_sample_n_volume':
            request_items = list(request_items.values())
            if len(request_items) % 2 != 0:
                raise ValueError('Not all samples are paired with a volume, or vice versa')
            else:
                remaining_items = request_items
                while len(remaining_items) > 0:
                    item_name = remaining_items.pop(0)
                    item_vol = remaining_items.pop(0)
                    finalLine = addMachineLine(finalLine,dest_slot,dest_well,source_df,item_name,item_vol)
                
#%% Export instructions as a text file for copying into the accompanying ot2code        
finalLine = finalLine[:-2]
f = open(outputFile, "w+")
f.write(finalLine)
f.close()
import pandas as pd
import numpy as np
import sys, warnings

def check_source_dest_and_layout_matching(slot_num, role, layout):
    '''Check that the layout of the slots matches with the source or destination
    
    Acceptable source layouts:
    - intuitive
    - dataframe
    Acceptable destination layouts:
    - intuitive
    - df_variable_sample_n_volume,
    - df_variable_sample
    - df_variable_volume
    '''
    
    role_layout_options = {
        "source": ["intuitive", "dataframe"],
        "destination": ["intuitive", "df_variable_sample_n_volume",
                        "df_variable_sample", "df_variable_volume"]
        }
    
    if layout not in role_layout_options[role]:
        raise ValueError('Mismatch between acceptable source/destination roles \
                         with layout for slot ' + str(slot_num) +
                         ' in "slot_setup" sheet. \n'
                         + 'Check that the acceptable layout is used. \n'
                         + 'Acceptable source layouts: \n'
                         + ' - intuitive \n'
                         + ' - dataframe \n'
                         + 'Acceptable destination layouts: \n'
                         + ' - intuitive \n'
                         + ' - df_variable_sample_n_volume, \n'
                         + ' - df_variable_sample \n'
                         + ' - df_variable_volume \n'
                         )

def remove_comments(df):
    '''Remove all columns in a df that starts with a "#", no automatic trim'''
    column_list = list(df.columns)
    comment_free_column_list = [column_name for column_name in column_list \
                                if str(column_name)[0] != '#']
    df = df[comment_free_column_list]
    return df

def check_intuitive_layout(slot_contents, slot_num):
    '''Check any slot tables with layout marked as "intuitive"
    
    Check whether number of rows and columns match any of the acceptable formats:
    
    Acceptable number of rows and columns:
    96-well: 8 rows * 12 columns
    48-well: 6 rows * 8 columns
    24-well or 1.5 / 2 mL tube rack: 4 rows * 6 columns
    15 mL tube rack: 3 rows * 5 columns
    15 & 50 mL tube rack: 3 rows * 4 columns
    6-well or 50 mL tube rack: 2 rows * 3 columns
    1-well: 1 row * 1 column
    
    Then check whether the row indices start with A and in ascending order,
    and whether the column indices start with 1 and in ascending order.
    '''
    
    acceptable_sizes = [
        (8, 12),
        (6, 8),
        (4, 6),
        (3, 5),
        (3, 4),
        (2, 3),
        (1, 1)
        ]
    
    # Note that first column is the row label
    slot_content_dimensions = (len(slot_contents), len(slot_contents.columns)-1)
    
    if slot_content_dimensions not in acceptable_sizes:
        raise ValueError('Incorret grid size for "intutitve" layout in slot '
                + str(slot_num) + '\n'
                + 'Acceptable number of rows and columns: \n'
                + '96-well: 8 rows * 12 columns \n'
                + '24-well or 1.5 / 2 mL tube rack: 4 rows * 6 columns \n'
                + '15 mL tube rack: 3 rows * 5 columns \n'
                + '15 & 50 mL tube rack: 3 rows * 4 columns \n'
                + '6-well or 50 mL tube rack: 2 rows * 3 columns \n'
                + '1-well: 1 row * 1 column'
                )
    
    # Verify left corner = 'row'
    if tuple(slot_contents.columns)[0] != 'row':
        raise ValueError('Column name "Row" is missing from table for \
                         "intutitve" layout in slot ' + str(slot_num) )
    
    # Check if column numbers are in order and matches
    # the intended size of the layout
    for i, column_index in enumerate(tuple(slot_contents.columns)[1:]):
        if i+1 != int(column_index):
            raise ValueError('Column numbers in wrong order or incorrectly \
                             formatted for "intutitve" layout in slot '
                             + str(slot_num) )
                             
    # Check if row indices are in order and matches
    # the intended size of the layout
    for i in range(len(slot_contents)):
        row_index = slot_contents.iloc[i]['row']
        if i+65 != ord(row_index):
            raise ValueError('Row indices in wrong order or incorrectly \
                             formatted for "intutitve" layout in slot '
                             + str(slot_num) )

def check_dataframe_layout(slot_contents, slot_num):
    '''Check any slot tables with layout marked as "dataframe"
    Check that slot tables have one column named "well",
    and one column named "sample". The order does not matter.
    '''
    column_names = tuple(slot_contents.columns)
    check_conditions = [
        len(column_names) == 2,
        "well" in column_names,
        "sample" in column_names
        ]
    
    if False in check_conditions:
        raise ValueError('Incorret layout for "dataframe layout in slot '
                         + str(slot_num) + '.\n'
                         + 'Check that only "well" and "sample" columns '
                         +'are present.')

def rearrange_intuitive_layout(slot_contents):
    '''Rearrange an intuitive layout into a DataFrame format'''
    
    row_indices = tuple(slot_contents['row'])
    slot_contents.set_index('row', inplace=True)
    
    new_slot_content = pd.DataFrame()
    
    # Convert each row into a column (series),
    # and attach the well name to each sample
    for row_index in row_indices:
        slot_contents_row = slot_contents.transpose()[row_index].to_frame('sample')
        slot_contents_row.insert(1, 'well', row_index 
                                 + slot_contents_row.index.astype(str))
        
        # Append to major dataframe of the single metadata
        new_slot_content = new_slot_content.append(slot_contents_row,sort=False)
        
    new_slot_content = new_slot_content.dropna()
    
    return new_slot_content

def try_global_vol_as_sample_vol(global_vol):
    '''Uses global volume if given and return 0 if not'''
    if not(np.isnan(global_vol)):
        return global_vol
    else:
        return 0

def add_machine_line(existing_inst_line, dest_slot_num, dest_well, source_df,
                   sample_name, sample_vol):
    '''Performs the actual mapping of source to destination, then create 
    machine readable instruction line and add to an existing line
    '''

    # Find where the source sample was
    source_record = source_df[source_df['sample']==sample_name]
    
    if len(source_record) == 0:
        raise ValueError('Sample "' + sample_name + '" from slot '
                     + dest_slot_num + ' not present among "source" sheets')
    
    source_slot = source_record.iloc[0]['slot']
    source_well = source_record.iloc[0]['well']

    # Create a new line of machine readable instruction
    new_inst_line = "'" + str(sample_vol) + '$' + source_slot + '_' + source_well \
    + '->' + dest_slot_num + '_' + dest_well + "',\n"
    
    # Add the new line to the exisiting line
    updated_inst_lines = existing_inst_line + new_inst_line
    return updated_inst_lines

def write_instructions(input_file):
    
    # if not input_file.lower().endswith('.xlsx'):
    #     print('Input file or path should be one Excel file ending with .xlsx')
    #     sys.exit(2)
    
    # Code for debugging
    
    # =============================================================================
    # import os
    # pwd = os.getcwd()
    # os.chdir(pwd)
    # input_file = r'./instructions_io/example_primer_resuspension.xlsx'
    # =============================================================================
    
    input_xlsx= pd.ExcelFile(input_file)
    sheets = {sheet:input_xlsx.parse(sheet) for sheet in input_xlsx.sheet_names}
    
    
    # Search for "slot_setup" file that defines layout of labware
    slot_setup = sheets.get('slot_setup')
    if slot_setup is None:
        raise ValueError('Sheet "slot_setup" not found')
    
    slot_setup = slot_setup.dropna(0, 'all')
    
    # Check that no duplicated slot numbers are present
    if True in slot_setup.duplicated(subset=['slot']).to_list():
        duplicated_slots = slot_setup[slot_setup['slot'].duplicated(
            keep=False)==True]['slot'].drop_duplicates().to_list()
        
        raise ValueError(
            'One or more slots were duplicated in the "slot_setup" sheet. \n'
            + 'Each slot can only be designated for "source" or "destination". \n'
            + 'Duplicated slots: \n'
            + str(duplicated_slots)
            )
    
    
    for i in range(len(slot_setup)):
                
        for col in ['slot', 'role', 'layout']:
            if not slot_setup.iloc[i][col]:
                raise ValueError('Parameter "' + col + '" is missing on row' +
                                 str(i+1) + "in slot_setup")
                
        slot_num = int(slot_setup.iloc[i]['slot'])
        
                
        if slot_num < 1 or slot_num > 11:
            raise ValueError('Slot number should be an integer between 1 to 11')
        
        check_source_dest_and_layout_matching(slot_num,
                                              role=slot_setup.iloc[i]['role'],
                                              layout=slot_setup.iloc[i]['layout'])
    
        slot_contents = sheets.get(str(slot_num))
        if slot_contents is None:
            raise ValueError('Sheet for slot ' +  str(slot_num) + ' not found.')
        
        # Columns with headings that starts with '#' are treated as comment
        # columns and are removed
        slot_contents = remove_comments(slot_contents)
        slot_contents = slot_contents.dropna(0, 'all')
        named_col_names = [col for col in slot_contents.columns if not("Unnamed:" in str(col))]
        slot_contents = slot_contents[named_col_names]
        sheets.update({
            str(slot_num): slot_contents
            })
    
        if slot_setup.iloc[i]['layout'] == "intuitive":
            check_intuitive_layout(slot_contents, slot_num)
            # replace the intuitive table with the rearranged dataframe
            sheets.update({
                str(slot_num): rearrange_intuitive_layout(slot_contents)
                    })
            
        elif slot_setup.iloc[i]['layout'] == "dataframe":
            check_dataframe_layout(slot_contents, slot_num)
            
    # Compile all slots for sources into a single dataframe
    source_df = pd.DataFrame()
    
    # Get a list of all slots marked as "source"
    source_slots_list = slot_setup[slot_setup['role']=='source']\
        ['slot'].astype('int').astype('str').tolist()
        # after filtering na values, pandas converted "slot" from int to float
        
    for slot_num in source_slots_list:
        source_slot_df = sheets.get(slot_num)
        source_slot_df.insert(1, 'slot', slot_num)
        source_df = source_df.append(source_slot_df, ignore_index=True)
        
    source_df['sample'] = source_df['sample'].str.strip()
    
    if True in source_df.duplicated(subset=['sample']).to_list():
        duplicated_samples = source_df[source_df['sample'].duplicated(keep=False)==True]\
            ['sample'].drop_duplicates().to_list()
            
        raise ValueError('One or more "source" samples have > 1 locations on deck.\n'
                         + 'This is currently not supported.\n'
                         + 'Source samples with multiple locations: \n'
                         + str(duplicated_samples)
                         )
    
    # Retrieve df containining destination slots and formats
    dest_info = slot_setup[slot_setup['role']=='destination']
        
    instructions = ''
        
    # Loop through every destination slot and decide case by case
    #  the pipetting instructions
    for i in range(len(dest_info)):
        dest_slot_num = dest_info.iloc[i]['slot'].astype('int').astype('str')
        layout = dest_info.iloc[i]['layout']
        dest_slot_df = sheets.get(dest_slot_num)
        global_vol = float(dest_info.iloc[i]['global_volume'])
        
        if layout == 'intuitive':
            
            # For "intuitive" destination slots, if "global_vol" is provided it
            # will be the sample_vol. Otherwise, volume will be set to 0
            
            sample_vol = try_global_vol_as_sample_vol(global_vol)
                 
            # Note that at this stage destination slot talbes of "intuitive" 
            # would have been converted to dataframe format
            for i in range(len(dest_slot_df)):
                dest_well = dest_slot_df.iloc[i]['well']
                dest_samples = dest_slot_df.iloc[i]['sample']
                requested_samples = dest_samples.split('+')
                
                # in case " + {empty} + sth" was written
                requested_samples = list(filter(None, requested_samples))
                
                for sample_name in requested_samples:
                    sample_name = sample_name.strip()
                    instructions = add_machine_line(instructions, dest_slot_num,
                                               dest_well, source_df,
                                               sample_name, sample_vol)
                
                
                
                
        else:
    
            for request_line in dest_slot_df.itertuples():
                request_line = request_line._asdict() # Convert named tuple to dict
                dest_well = request_line['well']
                
                requested_samples = {key: request_line[key] \
                                     for key in request_line.keys() \
                                     if key not in ['Index', 'well']}
                    
    
                if layout == 'df_variable_sample':
                    for requested_sample_info, sample_name in requested_samples.items():
                        
                        if type(sample_name)==float and np.isnan(sample_name):
                            continue
                        
                        sample_name = sample_name.strip()
                        
                        # For "df_variable_sample", try finding the desingated volume.
                        # If not provided, then use global volume if given
                        # If no global volume, volume will be set to 0
                        try:
                            sample_vol = requested_sample_info.split('_')[1]
                            if sample_vol == '':
                                sample_vol = try_global_vol_as_sample_vol(global_vol)
                            else:
                                sample_vol = float(sample_vol)
                        except IndexError:
                            sample_vol = try_global_vol_as_sample_vol(global_vol)
        
                        instructions = add_machine_line(instructions, dest_slot_num,
                                                   dest_well, source_df,
                                                   sample_name, sample_vol)
    
                elif layout == 'df_variable_volume':
                    
                    # For "df_variable_volume", if empty volume is given, 
                    # global volume will be used if available
                    # If no global volume, volume will be set to 0
                        
                    for sample_name, sample_vol in requested_samples.items():
                        
                        if np.isnan(sample_vol):
                            sample_vol = try_global_vol_as_sample_vol(global_vol)
                        
                        if sample_name[0] == '_':
                            raise ValueError('Sample name cannot start with "_" or'
                    + ' not given in "df_variable_volume" layout in slot '
                    + dest_slot_num)
                        
                        sample_name = sample_name.strip()
                        sample_vol = float(sample_vol)
                        
                        instructions = add_machine_line(instructions, dest_slot_num,
                                                   dest_well, source_df,
                                                   sample_name, sample_vol)
                
                
                elif layout == 'df_variable_sample_n_volume':
                    
                    
                    if global_vol:
                        warnings.warn('Global volume is given for slot '
                                      + dest_slot_num
                                      + ' but df_variable_sample_n_volume'
                                      + ' will not use it'
                                      )
                    
                    requested_sample_info = tuple(requested_samples.values())
                    
                    # Remove any blank (nan) values
                    requested_sample_info = [info for info in requested_sample_info
                         if not (type(info)==float and np.isnan(info))]
                    
                    if len(requested_sample_info) % 2 != 0:
                        raise ValueError('Not all samples are paired with a volume'
                                         + ' or vice versa for '
                                         + '"df_variable_sample_n_volume" layout '
                                         + 'in slot ' + dest_slot_num)
                    
                    remaining_items = requested_sample_info.copy()
                    
                    while len(remaining_items) > 0:
                        sample_name = remaining_items.pop(0)
                        sample_vol = remaining_items.pop(0)
                        
                        instructions = add_machine_line(instructions, dest_slot_num,
                                                   dest_well, source_df,
                                                   sample_name, sample_vol)
                
    instructions = instructions[:-2]
    
    return instructions

if __name__ == '__main__':
    
    args = sys.argv
    
    if len(args) != 2 or not args[1].lower().endswith('.xlsx'):
        print('Input file or path should be one Excel file ending with .xlsx')
        sys.exit(2)
    
    input_file = sys.argv[1]
    instructions = write_instructions(input_file)
    
    output_file = input_file.split(".xlsx")[0] + "_instructions.txt"
    
    f = open(output_file, "w+")
    f.write(instructions)
    f.close()
    
    print("Output file successfully created: " + output_file)
    
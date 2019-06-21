# -*- coding: utf-8 -*-
"""
Created on Fri May 24 20:24:59 2019

@author: Trevor Ho
"""

import pandas as pd

# initialize list of lists 
data = [['tom', 10, 'M'], ['nick', 15, 'M'], ['juli', 14, 'F']] 
  
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Name', 'Age', 'Gender'])

for row in df.itertuples():
    for field, value in row._asdict().items():
        print(field)
        print(value)
    
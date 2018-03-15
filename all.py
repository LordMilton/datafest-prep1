# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:10:35 2018

@author: Bradley Dufour
"""

import pandas as pd

df = pd.read_csv("CPSCFeedback.csv")
print(df['Q5'])
df['Q5'].hist();
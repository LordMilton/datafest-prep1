
import pandas as pd
import matplotlib.pyplot as plt

cpsc = pd.read_csv("CPSCFeedback.csv")

# First row has question description, which we'll condense and put in a 
# column name for analysis. Second row has outright crap.
cpsc = cpsc.drop(cpsc.index[0:2])

# Two kinds of data: coded (multiple choice) and free-text. Put into two
# different DataFrames since we'll treat them very differently.
coded = cpsc[['Q5','Q6','Q7','Q13','Q10','Q13.1','Q12']]
coded.columns = ['Why','Styles','Collaborate','Honor','Time','Level',
    'Programming']
text = cpsc[['Q5_3_TEXT','Q6_4_TEXT','Q11']]
text.columns = ['Why','Styles','Classes']

# Don't need the original DataFrame now.
del cpsc


# Recoding.
replacements = {
    'The love of programing and the subject':'love',
    'To get a good job and make money':'money',
    'Periodic quizzes instead of a midterm':'quizzes',
    'Incremental labs that connect to larger projects':'incremental',
    'Experience Points':'XP',
}

for old, new in replacements.items():
    coded.replace(old, new, regex=True,inplace=True)

# Add an ID column.
coded['id'] = range(len(coded))


# Separate "why" multi-choice question into separate DataFrame.
why_ids = []
why_vals = []

for i in range(len(coded)):
    whys = coded.iloc[i].Why.split(",") if type(coded.iloc[i].Why) is str \
                                                                    else []
    for why in whys:
        why_ids.append(i)
        why_vals.append(why)

whys = pd.DataFrame({'id':why_ids,'why':why_vals})


# Separate "style" multi-choice question into separate DataFrame.
style_ids = []
style_vals = []

for i in range(len(coded)):
    styles = coded.iloc[i].Styles.split(",") if type(coded.iloc[i].Styles) is str \
                                                                    else []
    for style in styles:
        style_ids.append(i)
        style_vals.append(style)

styles = pd.DataFrame({'id':style_ids,'style':style_vals})


# Recode the Programming values as integers, for order/comparison.
replacements = {
    'Above Average':2,
    'Below Average':0,
    'Average':1
}
for old, new in replacements.items():
    coded.replace(old, new, regex=True,inplace=True)

newlevel = coded.Level.copy()
newlevel[newlevel.isnull()] = 0
newlevel = newlevel.astype(int)
coded['Level'] = newlevel

newprogramming = coded.Programming.copy()
newprogramming[newprogramming.isnull()] = 0
newprogramming = newprogramming.astype(int)
coded['Programming'] = newprogramming

# Recode the Time values as integers, for order/comparison.
replacements = {
    'More than 8':8,
    '6-8':6,
    '4-6':4,
    '2-4':2,
    'Less than 2':0
}

for old, new in replacements.items():
    coded.replace(old, new, regex=True,inplace=True)

newtime = coded.Time.copy()
newtime[newtime.isnull()] = 0
newtime = newtime.astype(int)
coded['Time'] = newtime

# Okay, now the coded DataFrame can drop the other stuff that we put in "whys"
# and "styles."
coded = coded[['id','Collaborate','Honor','Time','Level','Programming']]

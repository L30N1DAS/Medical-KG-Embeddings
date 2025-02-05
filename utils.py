import pandas as pd

def read_all_save_unique(df):

    tmp = df.copy().drop('File', axis = 1)
    tmp = tmp.drop_duplicates()

    #jk duplicates can be on different days
    #fdf = tmp.merge(df, how = 'left', on = ['Subject', 'Predicate', 'Object'])
    return tmp  
import pandas as pd

#In the acquisition moment, drop duplicates. Sep default = ","

def acquisition(path_file,separator=","):
    dataframe = pd.read_csv(path_file,sep=separator).drop_duplicates()
    return dataframe
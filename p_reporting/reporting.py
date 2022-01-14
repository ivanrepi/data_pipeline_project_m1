import pandas as pd

#Create CSV function
def create_csv(df,path):
    df.to_csv(path, index=False)
    return print("CSV created properly")

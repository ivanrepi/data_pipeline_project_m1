import pandas as pd
import sys
sys.path.insert(0,'/Volumes/GoogleDrive/Mi unidad/IRONHACK/bootcamp/projects/data_pipeline_project_m1/modules')
from geo_calculations import to_mercator
from geo_calculations import distance_meters_simplified



def calculate_mercator(df,lat,long,new_col):
    df[new_col]=df.apply(lambda x: to_mercator (x[lat], x[long]),axis=1)
    return df

    
def distance_meters1(mercator1, mercator2):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    return mercator1.distance(mercator2)


def general_table(df1,df2):
    main_table = df1.assign(key=0).merge(df2.assign(key=0), how='outer', on ='key')
    main_table["distance"]= main_table.apply(lambda x: distance_meters_simplified(x["mercator1"], x["mercator2"]),axis=1)
    main_table2=main_table.groupby('title')['distance'].min().reset_index()
    result_general=main_table2.merge(main_table, how="left")
    return result_general


def nearest_bicimad_station(df1):
    nearest_bicimad_station= df1[["title","address.street-address","name","address"]] #We take just the columns we need for the final result table
    nearest_bicimad_station.rename(columns={"title":"Place of interest","address.street-address":"Station location","name":"BiciMAD station","address":"Station location"}, inplace=True)
    return nearest_bicimad_station


 
def bicimad_station(place,df):
    return df.loc[df["Place of interest"] == place]



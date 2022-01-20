import pandas as pd
from fuzzywuzzy import fuzz
import sys

#Import local path file 
from dotenv import load_dotenv
import os
load_dotenv()



sys.path.insert(0,os.getenv('path')+'modules')
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


def get_url_maps(ins_latitude,ins_longitude,bicimad_latitude,bicimad_longitude):
    ins_latitude=str(ins_latitude)
    ins_longitude=str(ins_longitude)
    bicimad_latitude=str(bicimad_latitude)
    bicimad_longitude=str(bicimad_longitude)
    url='https://www.google.com/maps/dir/'+ins_latitude+','+ins_longitude+'/'+bicimad_latitude+','+bicimad_longitude+'/@'+ins_latitude+','+ins_longitude+',17z/data=!3m1!4b1!4m7!4m6!1m3!2m2!1d'+ins_longitude+'!2d'+ins_latitude+'!1m0!3e2'
    return url


def nearest_bicimad_station(df1):
    nearest_bicimad_station= df1[["title","address.street-address","name","address","google_maps_url"]] #We take just the columns we need for the final result table
    nearest_bicimad_station.rename(columns={"title":"Place of interest","address.street-address":"Station location","name":"BiciMAD station","address":"Station location","google_maps_url":"Indications"}, inplace=True)
    return nearest_bicimad_station


 
def bicimad_station(place,df):
    return df.loc[df["Place of interest"] == place]


def similarity_ratio(result_general,input,ratio):

    result_general["similarity_ratio"]=result_general.apply(lambda x: fuzz.ratio (x["title"], input),axis=1)
    similarity=result_general.loc[result_general['similarity_ratio']>ratio]
    if len(similarity)>1:
        similarity.sort_values(by=['similarity_ratio'], inplace=True, ascending=False)
        if similarity["similarity_ratio"].iloc[0]>90:
            return (similarity.iloc[0]['title'])
    del result_general["similarity_ratio"]
    return similarity
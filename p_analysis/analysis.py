import pandas as pd
from fuzzywuzzy import fuzz
import sys

#Import local path file 
from dotenv import load_dotenv
import os
load_dotenv()


#Import functions from geo_calculations module
sys.path.insert(0,os.getenv('path')+'modules') #Get the path of the file from env 
from geo_calculations import to_mercator
from geo_calculations import distance_meters_simplified



def calculate_mercator(df,lat,long,new_col): #Giving 2 coordinates from 2 places, calculate the mercator projection value
    df[new_col]=df.apply(lambda x: to_mercator (x[lat], x[long]),axis=1)
    return df


def general_table(df1,df2):
    main_table = df1.assign(key=0).merge(df2.assign(key=0), how='outer', on ='key') #Merge 2 dataframes (place of interest + bicimads)
    main_table["distance"]= main_table.apply(lambda x: distance_meters_simplified(x["mercator1"], x["mercator2"]),axis=1) #Calculate the distance between each place of interest and all bicimad stations
    main_table2=main_table.groupby('title')['distance'].min().reset_index() #Group by place of interest, but we want only the minimum value in distance column
    result_general=main_table2.merge(main_table, how="left") #We merge the result with the main table, in order to get all detailed information but only with the result of table before
    return result_general


def get_url_maps(ins_latitude,ins_longitude,bicimad_latitude,bicimad_longitude): #Function to create the URL to see how to arrive to the bicimad station
    ins_latitude=str(ins_latitude)
    ins_longitude=str(ins_longitude)
    bicimad_latitude=str(bicimad_latitude)
    bicimad_longitude=str(bicimad_longitude)
    url='https://www.google.com/maps/dir/'+ins_latitude+','+ins_longitude+'/'+bicimad_latitude+','+bicimad_longitude+'/@'+ins_latitude+','+ins_longitude+',17z/data=!3m1!4b1!4m7!4m6!1m3!2m2!1d'+ins_longitude+'!2d'+ins_latitude+'!1m0!3e2'
    return url


def nearest_bicimad_station(df1): #We take just the columns we need for the final result table and rename the columns
    nearest_bicimad_station= df1[["title","address.street-address","name","address","google_maps_url"]] 
    nearest_bicimad_station.rename(columns={"title":"Place of interest","address.street-address":"Station location","name":"BiciMAD station","address":"Station location","google_maps_url":"Indications"}, inplace=True)
    return nearest_bicimad_station


 
def bicimad_station(place,df): #To return only the row of the place of Interest that user has choose
    return df.loc[df["Place of interest"] == place]


def similarity_ratio(result_general,input,ratio): #Function to find similar results

    result_general["similarity_ratio"]=result_general.apply(lambda x: fuzz.ratio (x["title"], input),axis=1) #Create a new columns with ratio value between word inserted by user, and all place of interest of the table
    similarity=result_general.loc[result_general['similarity_ratio']>ratio] #We maintain only the results when the ratio is more than X
    if len(similarity)>1: #If we have more than 1 result
        similarity.sort_values(by=['similarity_ratio'], inplace=True, ascending=False) #Order from highest to lower value
        if similarity["similarity_ratio"].iloc[0]>90: #If the first one position has a ratio over 90 (probably it is the correct word)
            return (similarity.iloc[0]['title']) #Return that row
    del result_general["similarity_ratio"] #Remove the similarity column for future 
    return similarity 
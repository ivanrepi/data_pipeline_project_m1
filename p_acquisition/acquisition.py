import pandas as pd
import requests
import sys

#Import local path file 
from dotenv import load_dotenv
import os
load_dotenv()


sys.path.insert(0,os.getenv('path')+'p_reporting')
from reporting import create_csv


#In the CSV acquisition moment, drop duplicates. Sep default = ","

def acquisition_csv(path_file,separator=","):
    dataframe = pd.read_csv(path_file,sep=separator).drop_duplicates()
    return dataframe


#We call to the API Instalaciones Madrid, and save the result as a CSV. In case connection fails, we work with CSV saved other times before.

def acquisition_json(path):
    try:
        df=requests.get(path).json()
        df = pd.json_normalize(df['@graph'])
        df.dropna(subset = ["location.latitude","location.longitude"], inplace=True) #Drop the rows where we have not latitude and longitude of the Sports installation
        create_csv(df,"data/raw/instalaciones.csv") #Save the result table in csv
        return df
    except:
        df=pd.read_csv("data/raw/instalaciones.csv", sep=";").drop_duplicates()
        return df


def get_station_details(df,place):
    instalacion_n= df.loc[df["title"] == place]
    station_id = instalacion_n["id_y"].to_string(index=False)
    header={'email':os.getenv('emt_madrid_email'),'password':os.getenv('emt_madrid_pwd')}
    url='https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/'
    get_token=requests.get(url, headers=header).json()
    accessToken=get_token['data'][0]['accessToken']
    url='https://openapi.emtmadrid.es/v1/transport/bicimad/stations/'+str(station_id)
    header = {'accessToken': str(accessToken) }
    my_dataset=requests.get(url, headers=header).json()
    return (my_dataset['data'][0])


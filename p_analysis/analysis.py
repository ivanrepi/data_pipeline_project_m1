import pandas as pd
import sys
sys.path.insert(0,'/Volumes/GoogleDrive/Mi unidad/IRONHACK/bootcamp/projects/data_pipeline_project_m1/modules')
from geo_calculations import distance_meters



def nearest_station(instalaciones,bicimad_stations):
    nearest_distance=pd.DataFrame(columns=["pk_ins","nombre_ins","ins_latitude","ins_longitude","bicimad_latitude","bicimad_longitude","distance","name_station","address_station","id"])

    for i in instalaciones.index:
        a=(float(instalaciones["LATITUD"][i]))
        b=(float(instalaciones["LONGITUD"][i]))
        pk=instalaciones["PK"][i]
        nombre=instalaciones["NOMBRE"][i]

        distance=pd.DataFrame(columns=["distance","latitude","longitude"])

        for j in bicimad_stations.index:
            c=(float(bicimad_stations["latitude"][j]))
            d=(float(bicimad_stations["longitude"][j]))
            name=bicimad_stations["name"][j]
            address=bicimad_stations["address"][j]
            id_station=bicimad_stations["id"][j]
            e=distance_meters(a, b, c, d)

            distance=distance.append({"distance":e[0],"latitude":c,"longitude":d,"name":name,"address":address,"id":id_station},ignore_index=True)

        nearest_station=distance.iloc[distance["distance"].idxmin()]
        nearest_distance=nearest_distance.append({"pk_ins":pk,"nombre_ins":nombre,"ins_latitude":a,"ins_longitude":b,"bicimad_latitude":nearest_station[1],"bicimad_longitude":nearest_station[2],"distance":nearest_station[0],"name_station":nearest_station[3],"address_station":nearest_station[4],"id":nearest_station[5]},ignore_index=True)

    #Eliminar esta primera fila cuando haya corregido el error del nombre de las columnas
    nearest_distance.rename(columns={"nombre_ins":"Place of interest","name_station":"Station location","address_station":"Station ID","id":"BiciMAD station"}, inplace=True)

    return nearest_distance
    

def get_general_table(instalaciones,nearest_distance):
    ins_nearest_stations=instalaciones.merge(nearest_distance,left_on="PK",right_on="pk_ins") #Merge instalaciones with the table obtained in the previous step, to get the address and the rest of information from instalaciones table
    ins_nearest_stations.dropna(subset = ["LATITUD","LONGITUD"], inplace=True) #Drop the rows where we have not latitude and longitude of the Sports installation
    return ins_nearest_stations


def result_table(ins_nearest_stations):
    nearest_bicimad_station= ins_nearest_stations[["Place of interest","CLASE-VIAL","NOMBRE-VIA","NUM","BiciMAD station","Station location"]] #We take just the columns we need for the final result table
    nearest_bicimad_station["Place address"]=ins_nearest_stations["CLASE-VIAL"]+" "+ins_nearest_stations["NOMBRE-VIA"] +" "+ ins_nearest_stations["NUM"].fillna("s/n") #Put all address information in 1 column
    result_nearest_station = nearest_bicimad_station[nearest_bicimad_station.columns[[0,6,4,5]]] #Take only the columns we need for the final result, and order them as per initial requeriment
    return result_nearest_station

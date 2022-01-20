import pandas as pd

#We need to seprate coordinates in two columns (latitude and longitude)
def get_coordinates(table):
    coordinates_stations = [i.split(",") for i in table["geometry_coordinates"]] #Split values by comma
    longitud = [float(j[0].replace("[","").strip()) for j in coordinates_stations] #Pos. 0 is the longitude
    latitud = [float(j[1].replace("]","").strip()) for j in coordinates_stations] #Pos. 1 is the latitude
    table["latitude"]=latitud
    table["longitude"]=longitud

    table["latitude"]=pd.to_numeric(table["latitude"])
    table["longitude"]=pd.to_numeric(table["longitude"])

    return table



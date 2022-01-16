from p_acquisition import acquisition as ac
from p_wrangling import wrangling as wr
from p_analysis import analysis as an
from p_reporting import reporting as rp

import warnings;
warnings.filterwarnings('ignore');

# DATA PIPELINE

def main():

    #Get bicimad_stations dataset from repo as well as sports installations from API
    bicimad_stations=ac.acquisition_csv("data/raw/bicimad_stations.csv")
    instalaciones=ac.acquisition_json("https://datos.madrid.es/egob/catalogo/200215-0-instalaciones-deportivas.json")

    #Separate coordinates from bicimad_stations dataset
    bicimad_stations = wr.get_coordinates(bicimad_stations)

    #Calculate mercator for both instalaciones and bicimad_stations
    instalaciones=an.calculate_mercator(instalaciones,"location.latitude","location.longitude","mercator1")
    bicimad_stations=an.calculate_mercator(bicimad_stations,"latitude","longitude","mercator2")

    #Get general table (both instalaciones and bicimad_station information) only with nearest bicimad station
    result_general=an.general_table(instalaciones,bicimad_stations) 
    rp.create_csv(result_general,"data/processed/result_general.csv")

    #Get result table:
    nearest_bicimad_station= an.nearest_bicimad_station(result_general)
    rp.create_csv(nearest_bicimad_station,"data/results/nearest_bicimad_station.csv")
    print("Result table created properly")

if __name__ == '__main__':
    main()
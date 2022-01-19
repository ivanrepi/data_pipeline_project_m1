from p_acquisition import acquisition as ac
from p_wrangling import wrangling as wr
from p_analysis import analysis as an
from p_reporting import reporting as rp
import random

import warnings;
warnings.filterwarnings('ignore');

# DATA PIPELINE

def main():

    security_number = random.randint(1000,9999) #Create a random securty number
    rp.send_email(security_number) #Send the code to the verification email

    print('\n')
    terminal_number=int(input("Enter your validation code: "))
    if terminal_number==security_number: #In case the number sent is the same entered in the terminal, ok to run admin functions
        print('\n')
        print("--//--- Be patient... We are preparing the results ---//--")
        print('\n')

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

        #Adding url of google maps indications to the general table
        result_general["google_maps_url"]=result_general.apply(lambda x: an.get_url_maps (x["location.latitude"], x["location.longitude"],x["latitude"],x["longitude"]),axis=1)
        rp.create_csv(result_general,"data/processed/result_general.csv")


        #Get result table:
        nearest_bicimad_station= an.nearest_bicimad_station(result_general)
        rp.create_csv(nearest_bicimad_station,"data/results/nearest_bicimad_station.csv")
        print("Result table created properly")
        print('\n')
        
    else:
        print('\n')
        print("You are not the fucking admin!!!")
        print('\n')


if __name__ == '__main__':
    main()
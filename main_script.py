from p_acquisition import acquisition as ac
from p_wrangling import wrangling as wr
from p_analysis import analysis as an
from p_reporting import reporting as rp


# DATA PIPELINE
if __name__ == "__main__":

    #Get bicimad_stations dataset as well as sport installations from repo
    bicimad_stations=ac.acquisition("data/raw/bicimad_stations.csv")
    instalaciones=ac.acquisition("data/raw/instalaciones_deportivas_madrid.csv",separator=";")

    #Separate coordinates from bicimad_stations dataset
    bicimad_stations = wr.get_coordinates(bicimad_stations)

    #Get a table with the nearest bicimad station for each Sports installation, and save it as a CSV
    nearest_distance=an.nearest_station(instalaciones,bicimad_stations)
    rp.create_csv(nearest_distance,"data/processed/nearest_distance.csv")

    #Create a general table with all detailed information from Sports installations (address, transport, coordinates, etc.)
    ins_nearest_stations=an.get_general_table(instalaciones,nearest_distance)

    result_nearest_station=an.result_table(ins_nearest_stations)
    rp.create_csv(result_nearest_station,"data/results/nearest_distance.csv") #Save the result table in csv

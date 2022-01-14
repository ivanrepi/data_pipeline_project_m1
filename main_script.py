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

    rp.create_csv(bicimad_stations,"data/processed/bicimad_stations.csv")




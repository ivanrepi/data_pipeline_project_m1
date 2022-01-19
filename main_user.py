from p_acquisition import acquisition as ac
from p_analysis import analysis as an
from p_reporting import reporting as rp
import argparse
import pandas as pd
import webbrowser as wb
import os
import warnings;
warnings.filterwarnings('ignore');
pd.options.display.max_colwidth = 10000

# DATA PIPELINE

# Argument parser function

def argument_parser():
    print('--//--- starting application ---//--')
    print('\n')
    parser = argparse.ArgumentParser(description='Set operation type')
    parser.add_argument("-i", "--choice", help="Choose a Place of Interest" , type=str)
    args = parser.parse_args()
    return args


def main(arguments):
    #Import dataframe where we have stroed all nearest bicimad stations
    nearest_station=ac.acquisition_csv("data/results/nearest_bicimad_station.csv")

    if arguments.choice is None:
        rp.create_html(nearest_station)
        url = '/Users/ivan.repilado/Google Drive/Mi unidad/IRONHACK/bootcamp/projects/data_pipeline_project_m1/nearest_bicimad_station.html'
        wb.open_new_tab("file://"+url)
   

    elif arguments.choice!="":
        result_general=ac.acquisition_csv("data/processed/result_general.csv")
        similarity=an.similarity_ratio(result_general,arguments.choice,50)

        if isinstance(similarity, pd.DataFrame) and len(similarity)>1:  
            print("We have found next results: \n")
            print(similarity["title"].to_string(index=False))
            print("\n")
            print("Please, select an option and enter the correct name")

        elif len(similarity)==0:
            print("There is no results for your search. Please, enter a correct name and try it again.")
            
        else:
            bicimad_station=an.bicimad_station(similarity,nearest_station)
            print(f'For {arguments.choice} the nearest BiciMAD station is ==> {bicimad_station["BiciMAD station"].to_string(index=False)} , Address: {bicimad_station["Station location"].to_string(index=False)}')
            try:
                free_bikes=ac.get_station_details(result_general,similarity)["dock_bikes"]
                print('\n')
                print(f'There are {free_bikes} free bikes in this station')
                print('\n')
                input("Press Enter to get the indications...")
                wb.open(bicimad_station["Indications"].to_string(index=False))
            except:
                print("Free Bikes: Information not available")

    print('\n')
    print('--//--- closing application ---//--')

if __name__ == '__main__':
    main(argument_parser())
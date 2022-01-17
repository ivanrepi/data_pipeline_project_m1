from p_acquisition import acquisition as ac
from p_analysis import analysis as an
from p_reporting import reporting as rp
import argparse
import pandas as pd
import webbrowser as wb
import os

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
        bicimad_station=an.bicimad_station(arguments.choice,nearest_station)
        print(f'For {arguments.choice} the nearest BiciMAD station is ==> {bicimad_station["BiciMAD station"][0]} , ADDRESS: {bicimad_station["Station location"][0]}')
        
        #Create a link for each position and put it here as a variable:
        wb.open("https://www.google.com/maps/dir/'40.479033,-3.708264'/40.463028,-3.69733/@40.479033,-3.708264,17z/data=!3m1!4b1!4m7!4m6!1m3!2m2!1d-3.708264!2d40.479033!1m0!3e2")

    print('\n')
    print('--//--- closing application ---//--')

if __name__ == '__main__':
    main(argument_parser())
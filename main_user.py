from p_acquisition import acquisition as ac
from p_analysis import analysis as an
import argparse
import pandas as pd


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
    nearest_station=ac.acquisition("data/results/result_nearest_distance.csv")
    if arguments.choice is None:
        print(nearest_station.to_string())

    elif arguments.choice!="":
        bicimad_station=an.bicimad_station(arguments.choice,nearest_station)
        print(f'For {arguments.choice} the nearest BiciMAD station is ==> {bicimad_station["BiciMAD station"][0]} , ADDRESS: {bicimad_station["Station location"][0]}')


    print('\n')
    print('--//--- closing application ---//--')

if __name__ == '__main__':
    main(argument_parser())
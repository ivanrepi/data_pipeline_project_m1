from p_acquisition import acquisition as ac
from p_analysis import analysis as an
from p_reporting import reporting as rp
import argparse
import pandas as pd
import webbrowser as wb
import os
import warnings;
warnings.filterwarnings('ignore'); #To hide the erros to the user
pd.options.display.max_colwidth = 10000 #To display the longest strings in the terminal 


#Import path from the env file
from dotenv import load_dotenv
import os
load_dotenv()


# DATA PIPELINE

# Argument parser function

def argument_parser():
    print('--//--- starting application ---//--')
    print('\n')
    parser = argparse.ArgumentParser(description='Set the result')
    parser.add_argument("-i", "--choice", help="Please, type (1) to get the table for every 'Place of interest' , or (2) To get the table for a specific 'Place of interest'" , type=str)
    args = parser.parse_args()
    return args


def main(arguments):
    #Import dataframe where we have stroed all nearest bicimad stations
    nearest_station=ac.acquisition_csv("data/results/nearest_bicimad_station.csv")

    if arguments.choice is None:
        print("Please, when starting the app, set the flag -i and type (1) to get the table for every 'Place of interest' , or (2) To get the table for a specific 'Place of interest' \n Press -h for more information")

    if arguments.choice == "1":
        rp.create_html(nearest_station.iloc[:,0:4])
        wb.open_new_tab("file://"+(os.getenv('path')+"nearest_bicimad_station.html"))
   

    elif arguments.choice=="2":
        place=str(input("Please, enter a specific 'Place of interest' and press ENTER: "))
        result_general=ac.acquisition_csv("data/processed/result_general.csv")
        similarity=an.similarity_ratio(result_general,place,50)

        if isinstance(similarity, pd.DataFrame) and len(similarity)>1:  
            print("We have found next results: \n")
            print(similarity["title"].to_string(index=False))
            print("\n")
            print("Please, select an option and enter the correct name")

        elif len(similarity)==0:
            print("There is no results for your search. Please, enter a correct name and try it again.")
            
        else:
            bicimad_station=an.bicimad_station(similarity,nearest_station)
            print('\n')
            print(f'For {place} the nearest BiciMAD station is ==> {bicimad_station["BiciMAD station"].to_string(index=False)} , Address: {bicimad_station["Station location"].to_string(index=False)}')
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
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
    print('--//--- starting application ---//-- \n')
    parser = argparse.ArgumentParser(description='Set the result')
    parser.add_argument("-i", "--choice", help="Please, type (1) to get the table for every 'Place of interest' , or (2) To get the table for a specific 'Place of interest'" , type=str)
    args = parser.parse_args()
    return args


def main(arguments):
    #Import dataframe where we have stroed all nearest bicimad stations
    nearest_station=ac.acquisition_csv("data/results/nearest_bicimad_station.csv")

    if arguments.choice is None: #We must use argparse. So we if user doesn't use it, he cannot continue
        print("Please, when starting the app, set the flag -i and type (1) to get the table for every 'Place of interest' , or (2) To get the table for a specific 'Place of interest' \n Press -h for more information")

    if arguments.choice == "1": #If user decide to see the complete tamble
        rp.create_html(nearest_station.iloc[:,0:4]) #Create htm of the complete table
        wb.open_new_tab("file://"+(os.getenv('path')+"nearest_bicimad_station.html")) #Open it in the browser
   

    elif arguments.choice=="2": #If user decide for an specific value
        place=str(input("Please, enter a specific 'Place of interest' and press ENTER: ")) #Type the place of Interest the user are interested in
        result_general=ac.acquisition_csv("data/processed/result_general.csv") #Import the result table
        similarity=an.similarity_ratio(result_general,place,70) #We find for similaritues. Ratio value set in 50 (we can change it)
        if isinstance(similarity, pd.DataFrame) and len(similarity)>1:  #If we have a list of similar results (more than 1), user should chose for someone
            print("We have found next results: \n")
            print(similarity["title"].to_string(index=False))
            print("\nPlease, select an option and enter the correct name")

        elif len(similarity)==0: #If there is not similar results
            print("\nThere is no results for your search. Please, enter a correct name and try it again.")
            
        else: #If we have only 1 similar result
            bicimad_station=an.bicimad_station(similarity,nearest_station) #Get the row of the result table with that similar result
            print(f'\nFor {place} the nearest BiciMAD station is ==> {bicimad_station["BiciMAD station"].to_string(index=False)} , Address: {bicimad_station["Station location"].to_string(index=False)}')
            try: #Try to get the available Bikes from BiciMad API
                free_bikes=ac.get_station_details(result_general,similarity)["dock_bikes"]
                print(f'\nThere are {free_bikes} free bikes in this station')
                input("\nPress Enter to get the indications...")
                wb.open(bicimad_station["Indications"].to_string(index=False))
            except: #If API does'nt work, show the error

                print("\nFree Bikes: Information not available")

    print('\n --//--- closing application ---//--')

if __name__ == '__main__':
    main(argument_parser())
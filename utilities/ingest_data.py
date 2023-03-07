"""
In this file, we are creating a utility to ingest data and store it in a MySQL DB.

Directions to use: python ingest_data.py --weather weather_data_location --crop crop_data_location
"""
import os
import argparse, sys
import pandas as pd
import numpy as np
import logging
import sqlite3

from numpy import nansum, nanmean

logging.basicConfig(filename='logs/ingestion.log',
                    filemode='w', 
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.info("Started execution of ingest_data.py")


def get_weather_data(weather_dir:str) -> pd.DataFrame:
    """
        Function to read weather dataset.

        Arguments:
            weather_dir (str): Directory location for weather data files

        Returns:
            Dataframe with all weather data read.
    """
    # Final DF
    final_df = pd.DataFrame()

    # Iterate over each file in the director
    for filename in os.listdir(weather_dir)[:5]:
        logging.info("Reading " + filename)
        # Check if it is txt file
        if filename.endswith('.txt'):
            # Get location of file
            location = os.path.join(weather_dir, filename)

            # Read data
            data = pd.read_csv(location, sep='\t', header=None)

            # Get ID from filename
            data['Station_id'] = os.path.splitext(filename)[0]

            # Append to final df
            if len(final_df) == 0:
                final_df = data
            else:
                final_df = pd.concat([final_df, data])

    final_df.columns = ["Date", "Maxtemp", "Mintemp", "Precipitation", "Station_id"]
    logging.info("All files read. Total records: " + str(final_df.shape[0]))

    return final_df

def get_crop_data(crop_dir:str) -> pd.DataFrame:
    """
        Function to read crop dataset.

        Arguments:
            crop_dir (str): Directory location for crop data files

        Returns:
            Dataframe with all crop data read.
    """
    # Final DF
    final_df = pd.DataFrame()

    # Iterate over each file in the director
    for filename in os.listdir(crop_dir)[:5]:
        logging.info("Reading " + filename)
        # Check if it is txt file
        if filename.endswith('.txt'):
            # Get location of file
            location = os.path.join(crop_dir, filename)

            # Read data
            data = pd.read_csv(location, sep='\t', header=None)

            # Append to final df
            if len(final_df) == 0:
                final_df = data
            else:
                final_df = pd.concat([final_df, data])

    final_df.columns = ["Date", "Yield"]
    logging.info("All files read. Total records: " + str(final_df.shape[0]))

    return final_df


if __name__ == '__main__':
    # Parse input arguments
    parser=argparse.ArgumentParser()
    parser.add_argument("--weather", help="Location of weather data.")
    parser.add_argument("--crop", help="Location of crop data.")
    args=parser.parse_args()
    logging.info("Parsed command line arguments")

    if args.weather is None and args.crop is None:
        logging.error("Couldn't find either --weather or --crop flag.")
        raise Exception("You must provide either --weather or --crop flag.")
    
    weather_location = args.weather
    crop_location = args.crop

    logging.info("Creating DB connection.")
    connection = sqlite3.connect('src/weather_app_api/python_test_db.sqlite3')
    logging.info("DB connected.")

    if crop_location is not None:
        logging.info("Reading crop data.")
        crop_data = get_crop_data(crop_location)

        crop_data.to_sql('crop_data', connection, if_exists='replace', index=True, index_label='id')
        logging.info("Crop data stored in DB.")

    if weather_location is not None:
        logging.info("Reading weather data.")
        weather_data = get_weather_data(weather_location)

        weather_data.to_sql('weather_data', connection, if_exists='replace', index=True, index_label='id')
        logging.info("Weather data stored in DB.")

        logging.info("Computing statistics: Average maximum temperature, Average Minimum Temperature and Total Accumulated Precipitation.")

        # Replace -9999 with NaNs
        weather_data = weather_data.replace(-9999, np.nan)

        # Get year from Date
        weather_data['Year'] = weather_data['Date'].astype(str).apply(lambda x: x[:4])

        # Now we can compute statistics while ignoring missing values
        weather_stats = weather_data.groupby(['Year', 'Station_id']).agg({
            'Maxtemp': nanmean,
            'Mintemp': nanmean,
            'Precipitation': nansum
        }).reset_index()
        weather_stats.columns = ['Year', 'Station_id', 'Average_Maxtemp', 'Average_Mintemp', 'Sum_Precipitation']
        weather_stats.to_sql('weather_stats', connection, if_exists='replace', index=True, index_label='id')
        logging.info("Weather statistics stored.")

    logging.info("Closing DB connection.")
    connection.close()
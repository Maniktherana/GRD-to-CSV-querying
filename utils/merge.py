import pandas as pd
import os


def merge_location_csvs():
    # Read the CSV files into DataFrames
    df_locations_max = pd.read_csv("../data/csv/locations_max.csv")
    df_locations_rain = pd.read_csv("../data/csv/locations_rain.csv")
    df_locations_min = pd.read_csv("../data/csv/locations_min.csv")

    # Concatenate the DataFrames
    dfs = [df_locations_max, df_locations_rain, df_locations_min]
    merged_df = pd.concat(dfs)

    # Sort the merged DataFrame by the first two columns: long, lat
    merged_df = merged_df.sort_values(by=["Latitude", "Longitude"])

    # Drop empty rows
    merged_df = merged_df.dropna()

    # Remove rows where the name column contains "India"
    merged_df = merged_df[~merged_df["Name"].str.contains("India")]

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv("../data/csv/all_locations.csv", index=False)


merge_location_csvs()

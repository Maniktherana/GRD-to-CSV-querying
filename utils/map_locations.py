import pandas as pd
import os


def map_locations_to_datasets():
    # Read the all_locations.csv file
    all_locations_df = pd.read_csv("../data/csv/all_locations.csv")

    # Get the latitude, longitude, city, and state columns
    all_locations_df = all_locations_df[["Latitude", "Longitude", "Name", "State"]]

    # Directories to process
    directories = ["max_temp", "min_temp", "rainfall"]

    # Iterate over the directories and files
    for directory in directories:
        directory_path = os.path.join("../data/csv/", directory)

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Check if the file is a CSV file
                if file.endswith(".csv"):
                    # Get the file path
                    file_path = os.path.join(root, file)

                    # Read the CSV file
                    csv_df = pd.read_csv(file_path)

                    # Merge with the all_locations_df based on latitude and longitude
                    merged_df = pd.merge(
                        csv_df,
                        all_locations_df,
                        on=["Latitude", "Longitude"],
                        how="left",
                    )

                    # Reorder the columns to place the city and state columns at the beginning
                    columns = merged_df.columns.tolist()
                    columns = ["Name", "State"] + [
                        column for column in columns if column not in ["Name", "State"]
                    ]
                    merged_df = merged_df[columns]

                    # Save the merged dataframe back to the file
                    merged_df.to_csv(file_path, index=False)
                    print(f"Merged locations to {file_path}")

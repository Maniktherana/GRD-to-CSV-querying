import os
import pandas as pd


def clean_datasets(start_year=1990, end_year=2023):
    # Directory paths
    base_directory = "../data/csv"
    directories = {
        "min_temp": "Mintemp_MinT_{}_wide.csv",
        "max_temp": "Maxtemp_MaxT_{}_wide.csv",
        "rainfall": "Rainfall_ind{}_rfp25_wide.csv",
    }

    # Iterate over the years
    for year in range(start_year, end_year):
        print(year)
        for directory, file_format in directories.items():
            print(directory)
            # Get the file path
            file_path = os.path.join(
                base_directory, directory, file_format.format(year)
            )

            # Check if the file exists
            if os.path.isfile(file_path):
                # Read the CSV file
                csv_df = pd.read_csv(file_path)

                # Remove rows without a name or state
                csv_df = csv_df.dropna(subset=["Name", "State"], how="all")

                # Save the modified dataframe back to the file
                csv_df.to_csv(file_path, index=False)

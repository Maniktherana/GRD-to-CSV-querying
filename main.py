import os
import pandas as pd

data_dir = "data/csv"
dataset_dir_mapping = {"min": "min_temp", "max": "max_temp", "rainfall": "rainfall"}


def get_data_file_path(dataset, year):
    dataset_dir = dataset_dir_mapping.get(dataset)
    if not dataset_dir:
        raise ValueError(f"Invalid dataset: {dataset}")

    if dataset == "rainfall":
        file_name = f"Rainfall_ind{year}_rfp25_wide.csv"
    else:
        file_name = (
            f"{dataset.capitalize()}temp_{dataset.capitalize()}T_{year}_wide.csv"
        )

    return os.path.join(data_dir, dataset_dir, file_name)


def query_data(dataset, start_date, end_date, place):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    dfs = []

    for year in range(start_year, end_year + 1):
        file_path = get_data_file_path(dataset, year)
        if not os.path.isfile(file_path):
            print(f"No data available for {year}")
            continue

        df = pd.read_csv(file_path)
        df_filtered = df[
            (df["Name"].str.lower() == place.lower())
            | (df["State"].str.lower() == place.lower())
        ]

        date_columns = [
            col for col in df_filtered.columns if start_date <= col <= end_date
        ]

        if year == start_year:
            columns_to_select = [
                "Name",
                "State",
                "Longitude",
                "Latitude",
            ] + date_columns
        else:
            columns_to_select = date_columns

        data = df_filtered[columns_to_select]

        dfs.append(data)

    if len(dfs) > 0:
        output_file_path = f"./data/csv/results/{dataset}_filtered.csv"
        result_df = pd.concat(dfs, axis=1)
        result_df.to_csv(output_file_path, index=False)
        print(f"All filtered data saved to {output_file_path}")
    else:
        print("No data available for the specified range and place")


def main():
    dataset = input("Enter the dataset you want to query (min, max, or rainfall): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    place = input("Enter the place (city or state): ")

    query_data(dataset, start_date, end_date, place)


if __name__ == "__main__":
    main()

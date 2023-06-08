import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import set_constants


def convert_grd_to_csv(type, start_year=1990, end_year=2023):
    # Check for correct type
    (
        file_start,
        file_end,
        save_start,
        save_end,
        NUM_LAT,
        NUM_LON,
    ) = set_constants.set_constants(type, "convert")
    if file_start is None:
        return
    # Iterate over years
    for year in range(start_year, end_year):
        START_DATE = datetime(year, 1, 1)

        # Check if the year is a leap year
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            NUM_DAYS = 366
        else:
            NUM_DAYS = 365

        # Read binary data using numpy
        print(f"Converting grd to csv for {file_start}{year}{file_end}")
        data = np.fromfile(f"{file_start}{year}{file_end}", dtype=np.float32)

        data = data.reshape((NUM_DAYS, NUM_LAT, NUM_LON))

        # Create date range
        dates = pd.date_range(START_DATE, periods=NUM_DAYS).strftime("%Y-%m-%d")

        # Create latitude and longitude indices
        if type == "rainfall":
            latitude_index = np.arange(6.5, 6.5 + NUM_LAT * 0.25, 0.25)
            longitude_index = np.arange(66.5, 66.5 + NUM_LON * 0.25, 0.25)
        else:
            latitude_index = np.arange(7.5, 7.5 + NUM_LAT)
            longitude_index = np.arange(67.5, 67.5 + NUM_LON)

        # Create empty list to collect rows
        rows = []

        # Populate rows list
        for lat in range(NUM_LAT):
            latitude = latitude_index[lat]
            for lon in range(NUM_LON):
                longitude = longitude_index[lon]
                row_data = [latitude, longitude] + list(data[:, lat, lon])
                rows.append(row_data)

        # Convert list of rows to DataFrame
        df = pd.DataFrame(rows, columns=["Latitude", "Longitude"] + list(dates))

        # Save DataFrame to CSV
        df.to_csv(f"{save_start}{year}{save_end}", index=False)

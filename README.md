# Convert GRD to CSV and Query Climate Data

These python scripts take gridded Rainfall, Max Temperature and Min Temperature from [Climate Research & Services, Pune](https://www.imdpune.gov.in/lrfindex.php) and converts them into csv data. The scripts can also be used to query csv data by city/state, dataset (max temp, min temp or rainfall) and time.

## Table of contents

- [Setup and Installation](#setup-and-installation)
- [Quering Data](#querying-data)
- [Converting Data](#converting-data)
- [How it works](#how-it-works)
  - [Data Directory Structure](#data-directory-structure)
  - [Converting Data](#converting-data)
  - [Converting longitudes and latitudes to cities](#converting-longitudes-and-latitudes-to-cities)
  - [Manipulating Data](#manipulating-data)


## Setup and Installation

1. Clone this repository
```bash
git clone https://github.com/Maniktherana/GRD-to-CSV-querying.git
```
2. Create a virtual environment 
```bash
python3 -m venv grdToCsv
source grdToCsv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Querying Data

The entrypoint is main.py
```bash
python main.py
```

Example Query:
```bash
Enter the dataset you want to query (min, max, or rainfall): min
Enter the start date (YYYY-MM-DD): 2001-01-01
Enter the end date (YYYY-MM-DD): 2001-01-02
Enter the place (city or state): Greater Noida
              Name          State  Longitude  Latitude  2001-01-01  2001-01-02
768  Greater Noida  Uttar Pradesh       77.5      28.5        11.2        7.37
769  Greater Noida  Uttar Pradesh       77.5      28.5        11.2        7.37
770  Greater Noida  Uttar Pradesh       77.5      28.5        11.2        7.37
All filtered data saved to ./data/csv/results/min_filtered.csv
```

## Converting Data

1. Preparing data requires the use of the [Open Weather Reverse geocoding API](https://openweathermap.org/api/geocoding-api#reverse). Simply sign up for an account to get the API key.

2. Create a `.env` at the root level:
```bash
touch .env
```

3. Add your API key:
```.env
API_KEY=<Your API Key>
```

4. In order to convert grd data to csv, run `prepare_data.py`
```bash
python prepare_data.py
```

## How it works

### Data Directory Structure

The data has to be kept in a specific format:
```bash
data/
├─ csv/
│  ├─ min_temp/
│  ├─ max_temp/
│  ├─ rainfall/
│  ├─ results/
├─ grd/
│  ├─ min_temp_grd/
│  ├─ max_temp_grd/
│  ├─ rainfall_grd/
```
All gridded data must be stored under the `/grd` directory and in the respective subdirectory. The data can be downloaded by year from the [Climate Research & Services, Pune](https://www.imdpune.gov.in/lrfindex.php).

The csv files get generated by running 
```bash
python prepare_data.py
```

### Converting Data

Converting the data is relatively straightforward as sample code is provided on their website:

```c
/* This program reads binary data for 365/366 days and writes in ascii file. */ #include

main() {
  float rf[135][129], rainfall;
  float lo[135], la[129];
  int i, j, k, year, year1, month, date, nd;
  FILE * fptr1, * fptr2;
  int nd1[13] = {
    0,
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
  };
  int nd2[13] = {
    0,
    31,
    29,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
  };
  year = 2013;
  printf("Year = %d", year);
  fptr1 = fopen("g:\\data\\ind2013_rfp25.grd", "rb"); // input file
  fptr2 = fopen("g:\\data\\ind2013_rfp25.prt", "w");
  if (fptr1 == NULL) {
    printf("Can't open file");
    return 0;
  }
  if (fptr2 == NULL) {
    printf("Can't open file");
    return 0;
  }
  for (j = 0; j < 135; j++) lo[j] = 66.5 + j * 0.25;
  for (j = 0; j < 129; j++) la[j] = 6.5 + j * 0.25;
  year1 = year / 4;
  year1 = year1 * 4;
  for (month = 1; month < 13; month++) {
    nd = nd1[month];
    if (year == year1) nd = nd2[month];
    for (date = 1; date <= nd; date++) {
      fprintf(fptr2, "\n%02d%02d%04d", date, month, year);
      for (j = 0; j < 135; j++) fprintf(fptr2, "%7.2f", lo[j]);
      for (i = 0; i < 129; i++) {
        fprintf(fptr2, "\n%8.2f", la[i]);
        for (j = 0; j < 135; j++) {
          if (fread( & rainfall, sizeof(rainfall), 1, fptr1) != 1) return 0;
          rf[j][i] = rainfall;
          fprintf(fptr2, "%7.1f", rf[j][i]);
        }
      }
      printf("%4d %02d %02d \n", year, month, date);
    }
  }
  fclose(fptr1);
  fclose(fptr2);
  printf("Year = %d", year);
  return 0;
} /* end of main */
```

However, **this approach is significantly slow** when dealing with rainfall data due to the sheer size of the datasets. Hence, I chose to use pandas as it provides a powerful and efficient way to handle and manipulate tabular data. 

[convert.py](https://github.com/Maniktherana/GRD-to-CSV-querying/blob/master/utils/convert.py)
```python
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
```

In this code, I utilized pandas to convert the collected gridded data into a DataFrame. By appending the data to a list of rows and specifying the column names, I was able to create a structured and organized representation of the gridded data. The resulting DataFrame allows for convenient analysis, processing, and export of the data in various formats, such as converting it to a csv file in this case.

The data gets parsed into a **wide dataset** where 99.9 (for temperature) or -999.0 (for rainfall) represents no data collected:
<table class="table table-bordered table-hover table-condensed">
  <thead>
    <tr>
      <th title="Field #1">Latitude</th>
      <th title="Field #2">Longitude</th>
      <th title="Field #3">1990-01-01</th>
      <th title="Field #4">1990-01-02</th>
      <th title="Field #5">1990-01-03</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">7.5</td>
      <td align="right">67.5</td>
      <td align="right">99.9</td>
      <td align="right">99.9</td>
      <td align="right">99.9</td>
    </tr>
    <tr>
      <td align="right">7.5</td>
      <td align="right">68.5</td>
      <td align="right">99.9</td>
      <td align="right">99.9</td>
      <td align="right">99.9</td>
    </tr>
  </tbody>
</table>


### Converting longitudes and latitudes to cities

I chose to use the reverse geocoding API provided by Open Weather in order to map Longitude and Latitude values to a city and state in India. I utilized asyncio and aiohttp to run the requests concurrently, hence speeding up the api calls. While the API has a rate limit of 60 calls/minute for the free plan, I used `asyncio.Semaphore(60)` to get by this restriction:
```python
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
```
```python
async with aiohttp.ClientSession() as session:
    try:
        response = await fetch(session, url)
```
```python
# Create an event loop
loop = asyncio.get_event_loop()

# Run the asynchronous tasks
tasks = [fetch_data(row) for _, row in df.iterrows()]
loop.run_until_complete(asyncio.gather(*tasks))
```

This results in 3 csv files with location data for all longitudes and latitudes. They then get merged into a single `all_locations.csv` file using basic pandas.
<table class="table table-bordered table-hover table-condensed">
  <thead>
    <tr>
      <th title="Field #1">Name</th>
      <th title="Field #2">State</th>
      <th title="Field #3">Latitude</th>
      <th title="Field #4">Longitude</th>
      <th title="Field #5">1990-01-01</th>
      <th title="Field #6">1990-01-02</th>
      <th title="Field #7">1990-01-03</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Nanguneri</td>
      <td>Tamil Nadu</td>
      <td align="right">8.5</td>
      <td align="right">77.5</td>
      <td align="right">31.99</td>
      <td align="right">31.84</td>
      <td align="right">32.34</td>
    </tr>
  </tbody>
</table>

### Manipulating Data

All location data gets saved to `/data/csv/all_locations.csv`. I then use this file to append all locations to all of the csv datasets with `map_locations.py`:
```python3
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
```



Once that is done, querying for data becomes relatively straightforward and can be done with pandas. 

### Querying Data

The function `query_data` queries data based on specified criteria such as the start and end dates and the place. It reads CSV files corresponding to the specified dataset and years, filters the data based on the provided criteria, and selects the relevant columns. It then appends the filtered data horizontally by concatenating the columns, excluding duplicate columns for subsequent years. Finally, it saves the resulting DataFrame as a CSV file and provides a message about the status of the operation.

```python
def query_data(dataset, start_date, end_date, place):
    # List to store filtered DataFrames for each year
    dfs = []

    for year in range(start_year, end_year + 1):
        # Get the file path for the dataset and year
        file_path = get_data_file_path(dataset, year)  

        df = pd.read_csv(file_path)
        
        # Filter the DataFrame based on the specified place (case-insensitive)
        df_filtered = df[
            (df["Name"].str.lower() == place.lower()) | (df["State"].str.lower() == place.lower())
        ]  
        
        # Select date columns that fall within the specified start and end dates
        date_columns = [
            col for col in df_filtered.columns if start_date <= col <= end_date
        ]

        # Include additional columns for the first year (start_year)
        if year == start_year:
            columns_to_select = [
                "Name",
                "State",
                "Longitude",
                "Latitude",
            ] + date_columns  
        else:
            # Only select date columns for subsequent years
            columns_to_select = date_columns
        
        # Select the desired columns from the filtered DataFrame
        data = df_filtered[columns_to_select]  

        dfs.append(data)  # Append the filtered DataFrame to the list


```



import pandas as pd
import asyncio
import aiohttp
from retrying import retry
import set_constants
import os
from dotenv import load_dotenv


# add api key from .env file
load_dotenv("../.env")

API_KEY = os.getenv("API_KEY")


def get_locations(type):
    # set constants
    (csv_start, csv_end, ignore, location_file_name) = set_constants.set_constants(
        type, "location"
    )

    if csv_start is None:
        return

    # Function to make an asynchronous API request
    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.json()

    # Read the locations.csv file into a DataFrame
    df = pd.read_csv(f"{csv_start}1991{csv_end}")

    # Create an empty DataFrame to store the fetched data
    names_df = pd.DataFrame(
        columns=["Latitude", "Longitude", "Name", "State", "Country"]
    )

    # Limit the API requests to 60 per minute
    rate_limit = asyncio.Semaphore(50)

    # Asynchronous function to fetch data for each row in the DataFrame
    async def fetch_data(row):
        lat = row["Latitude"]
        lon = row["Longitude"]
        # Skip rows with temperatures equal to ignore value
        if row.iloc[2:].eq(ignore).all():
            return

        # Construct the API URL
        url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={API_KEY}"

        async with rate_limit:
            async with aiohttp.ClientSession() as session:
                # Make the asynchronous API request
                try:
                    response = await fetch(session, url)
                    if len(response) > 0:
                        response = response[0]
                        # Extract the required data from the response
                        name = response["name"] if "name" in response else None
                        state = response["state"] if "state" in response else None
                        country = response["country"] if "country" in response else None
                        print(f"Adding {name}, {state}, {country}")
                        # Append the data to the names_df DataFrame
                        names_df.loc[len(names_df)] = [lat, lon, name, state, country]
                    else:
                        print(f"No data found for {lat}, {lon}")

                except Exception as e:
                    print(f"Failed to fetch data for {lat}, {lon}: {e}")
                    raise

    # Create an event loop
    loop = asyncio.get_event_loop()

    # Run the asynchronous tasks
    tasks = [fetch_data(row) for _, row in df.iterrows()]
    loop.run_until_complete(asyncio.gather(*tasks))

    # Save the names_df DataFrame to names.csv
    names_df.to_csv(f"../data/csv/{location_file_name}.csv", index=False)

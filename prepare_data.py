from utils import (
    append_location,
    clean_datasets,
    convert,
    get_locations,
    merge,
    map_locations,
)

start_year = int(input("Enter start year: "))
end_year = int(input("Enter end year: "))

convert.convert("rainfall", start_year, end_year)
convert.convert("min", start_year, end_year)
convert.convert("max", start_year, end_year)

get_locations.get_locations("rainfall")
get_locations.get_locations("min")
get_locations.get_locations("max")

merge.merge_location_csvs()

map_locations.map_locations_to_datasets()

clean_datasets.clean_datasets(start_year, end_year)

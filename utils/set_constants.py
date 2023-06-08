def set_constants(type, func):
    WRONG_TYPE_MESSAGE = "Invalid type, please enter min, max or rainfall"
    if type == "min":
        file_start = "../data/grd/min_temp_grd/Mintemp_MinT_"
        file_end = ".GRD"
        csv_start = "../data/csv/min_temp/Mintemp_MinT_"
        csv_end = "_wide.csv"
        NUM_LAT = 31
        NUM_LON = 31
        ignore = 99.9
        location_file_name = "locations_min"
        if func == "convert":
            return file_start, file_end, csv_start, csv_end, NUM_LAT, NUM_LON
        elif func == "location":
            return csv_start, csv_end, ignore, location_file_name
    elif type == "max":
        file_start = "../data/grd/max_temp_grd/Maxtemp_MaxT_"
        file_end = ".GRD"
        csv_start = "../data/csv/max_temp/Maxtemp_MaxT_"
        csv_end = "_wide.csv"
        NUM_LAT = 31
        NUM_LON = 31
        ignore = 99.9
        location_file_name = "locations_max"
        if func == "convert":
            return file_start, file_end, csv_start, csv_end, NUM_LAT, NUM_LON
        elif func == "location":
            return csv_start, csv_end, ignore, location_file_name
    elif type == "rainfall":
        file_start = "../data/grd/rainfall_grd/Rainfall_ind"
        file_end = "_rfp25.grd"
        csv_start = "../data/csv/rainfall/Rainfall_ind"
        csv_end = "_rfp25_wide.csv"
        NUM_LAT = 129
        NUM_LON = 135
        ignore = -999.0
        location_file_name = "locations_rain"
        if func == "convert":
            return file_start, file_end, csv_start, csv_end, NUM_LAT, NUM_LON
        elif func == "location":
            return csv_start, csv_end, ignore, location_file_name
    else:
        print(WRONG_TYPE_MESSAGE)
        return None, None, None, None, None, None

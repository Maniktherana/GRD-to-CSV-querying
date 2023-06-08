# Convert GRD to CSV 

These python scripts take gridded Rainfall, Max Temperature and Min Temperature from [Climate Research & Services, Pune](https://www.imdpune.gov.in/lrfindex.php) and converts them into csv data. The scripts can also be used to data by City or State, Dataset (max, min or rainfall) and Time.

## Setup and Installation

Clone this repository
```bash
git clone https://github.com/Maniktherana/GRD-to-CSV-querying.git
```

Create a virtual environment and install
```bash
python3 -m venv grdToCsv
source grdToCsv/bin/activate
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
Enter the end date (YYYY-MM-DD): 2003-01-01
Enter the place (city or state): Gujarat
All filtered data saved to ./data/csv/results/min_filtered.csv
```


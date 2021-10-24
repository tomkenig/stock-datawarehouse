"""
# API examples: https://alternative.me/crypto/fear-and-greed-index/
# Example URL: https://api.alternative.me/fng/
# Example URL: https://api.alternative.me/fng/?limit=10
# Example URL: https://api.alternative.me/fng/?limit=10&format=csv
# Example URL: https://api.alternative.me/fng/?limit=10&format=csv&date_format=us
 """

# todo: start and load into rdbms
# todo: first time get all historical periods
# todo: when first run is done, get only the newrst data

# Libs
import json
import requests
from datetime import datetime
from db_works import db_connect, db_tables

db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()

# how many periods need to be overwrite on every run
PERIODS_TO_OVERWRITE = 3

def get_fagi_data():
    url = "https://api.alternative.me/fng/?limit=10000"
    data = requests.get(url).json()
    return data

data = get_fagi_data()
print(data["data"][0:PERIODS_TO_OVERWRITE])


# todo: insert all periods at first run

def insert_overwrite_data_fagi_current():
    cursor.execute(
        "DELETE FROM " + db_schema_name + "."  + "fear_and_greed_index_data where open_time >= %s and market = %s and tick_interval = %s and data_granulation = %s  "
                                                                "and stock_type = %s and stock_exchange = %s and download_settings_id = %s",
        (download_settings_id))


# todo: delete last periods from database

# todo: insert new periods


if data["metadata"]["error"] == None:
    print("ok")
    for i in data["data"][0:PERIODS_TO_OVERWRITE]:
        print(i["value"])
        print(i["value_classification"])
        print(i["timestamp"])
        print(datetime.utcfromtimestamp(int(i["timestamp"])))

        try:



# print(data["metadata"]["error"])

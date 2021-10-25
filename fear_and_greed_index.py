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
# get settings from json
def get_fagi_settings_json():
    with open("global_config.json") as json_conf:
        fagi_conf = (json.load(json_conf))
    print("conf file opened")
    periods_to_overwrite = fagi_conf["periods_to_overwrite"]
    return periods_to_overwrite

periods_to_overwrite = get_fagi_settings_json()

print(periods_to_overwrite)

def check_is_firs_run():
    print("first run ever")

    print("next run with overwrite")


def get_fagi_data():
    url = "https://api.alternative.me/fng/?limit=10000"
    data = requests.get(url).json()
    return data

data = get_fagi_data()
print(data["data"][0:periods_to_overwrite])


# todo: insert all periods at first run

def insert_overwrite_data_fagi_current():
    #cursor.execute("DELETE FROM " + db_schema_name + "."  + "fear_and_greed", (download_settings_id))
    print("old rows deleted")
    print("new rows inserted")


# todo: delete last periods from database

# todo: insert new periods


if data["metadata"]["error"] == None:
    print("ok")
    for i in data["data"][0:periods_to_overwrite]:
        print(i["value"])
        print(i["value_classification"])
        print(i["timestamp"])
        print(datetime.utcfromtimestamp(int(i["timestamp"])))




# print(data["metadata"]["error"])

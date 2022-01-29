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


# get settings from json
def get_fagi_settings_json():
    with open("global_config.json") as json_conf:
        fagi_conf = (json.load(json_conf))
    print("conf file opened")
    periods_to_overwrite = fagi_conf["periods_to_overwrite"]
    db_fagi_schema_name = fagi_conf["db_fagi_schema_name"]
    db_fagi_table_name = fagi_conf["db_fagi_table_name"]
    return periods_to_overwrite, db_fagi_schema_name, db_fagi_table_name


def check_is_first_run():
    cursor.execute("SELECT max(timestamp), count(1) FROM " + db_fagi_schema_name + "." + db_fagi_table_name + " ")
    query_result = cursor.fetchall()
    max_timestamp = query_result[0][0]
    rec_cnt = query_result[0][1]
    if rec_cnt != 0:
        print("next run with overwrite")
        return max_timestamp
    else:
        print("first run ever")
        return 0


def get_periods_to_overwrite():
    if max_timestamp !=0:
        final_periods_to_overwrite = periods_to_overwrite
    else:
        final_periods_to_overwrite = 10000
    return final_periods_to_overwrite


def get_fagi_data():
    url = "https://api.alternative.me/fng/?limit=10000"
    data = requests.get(url).json()
    return data




if __name__ == "__main__":
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()

    periods_to_overwrite, db_fagi_schema_name, db_fagi_table_name = get_fagi_settings_json()
    print(periods_to_overwrite, db_fagi_schema_name, db_fagi_table_name)

    max_timestamp = check_is_first_run()
    print(check_is_first_run())

    final_periods_to_overwrite = get_periods_to_overwrite()

    data = get_fagi_data()

    data_short = (data["data"][0:final_periods_to_overwrite])

    print(data_short[-1]["timestamp"])


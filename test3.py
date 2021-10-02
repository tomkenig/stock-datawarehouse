

# libs
# import stockdwh_functions
import requests
import mysql.connector  # https://dev.mysql.com/doc/connector-python/en/
import json
from datetime import datetime, timedelta
import math
import zipfile
import csv

# get database connection credentials from JSON file
with open('db_credentials.json') as json_conf:
    sql_db_conn = (json.load(json_conf))

# db driver (MySQL) connection settings
cnxn = mysql.connector.connect(user=sql_db_conn["user"],
                               password=sql_db_conn["password"],
                               host=sql_db_conn["host"],
                               database=sql_db_conn["database"])

# destination
db_schema_name = sql_db_conn["db_schema_name"]  # schema_name
db_table_name = sql_db_conn["db_table_name"]  # table_name
db_settings_table_name = sql_db_conn["db_settings_table_name"]  # settings table name

# open db connection
cursor = cnxn.cursor()

cursor.execute("SELECT download_settings_id, market, tick_interval, stock_type, stock_exchange, current_range_to_overwrite, download_interval_sec, daily_update_from_files, monthly_update_from_files, start_download_ux_timestamp FROM " + db_schema_name + "." + db_settings_table_name + " WHERE daily_update_from_files = 1 and daily_hist_complete = 0 order by start_download_ux_timestamp asc limit 1")
download_setting = cursor.fetchall()
download_settings_id = download_setting[0][0]
market = download_setting[0][1]
tick_interval = download_setting[0][2]
stock_type = download_setting[0][3]
stock_exchange = download_setting[0][4]
range_to_download = download_setting[0][5]
download_interval_sec = download_setting[0][6]
daily_update_from_files = download_setting[0][7]
monthly_update_from_files = download_setting[0][8]
start_download_ux_timestamp = download_setting[0][9]


print(download_setting)
print(download_settings_id)

cursor.execute("UPDATE  " + db_schema_name + "." + db_settings_table_name + " SET start_download_ux_timestamp = %s where download_settings_id = %s", (str(999000), str(download_settings_id)))
cnxn.commit()

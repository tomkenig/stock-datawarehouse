# libs
import requests
import mysql.connector  # https://dev.mysql.com/doc/connector-python/en/
import json
import datetime
import math

# get database connection credentials from JSON file
with open('db_credentials.json') as json_conf:
    sql_db_conn = (json.load(json_conf))

# db driver (MySQL) connection settings
cnxn = mysql.connector.connect(user=sql_db_conn["user"],
                               password=sql_db_conn["password"],
                               host=sql_db_conn["host"],
                               database=sql_db_conn["database"])

ts = str(math.floor(datetime.datetime.now().timestamp()))
# destination
db_schema_name = sql_db_conn["db_schema_name"]  # schema_name
db_table_name = sql_db_conn["db_table_name"]  # table_name
db_settings_table_name = sql_db_conn["db_settings_table_name"]  # settings table name

# open db connection
cursor = cnxn.cursor()

cursor.execute("SELECT download_settings_id, market, tick_interval, stock_exchange, api_range_to_overwrite, download_interval_sec FROM " + db_schema_name + "." + db_settings_table_name + " WHERE next_download_timestamp <= " + ts + " order by next_download_timestamp asc limit 1")
download_setting = cursor.fetchall()

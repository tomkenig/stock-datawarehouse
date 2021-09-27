def get_settings():
    cursor = cnxn.cursor()

    cursor.execute( "SELECT download_settings_id, market, tick_interval, stock_type, stock_exchange, api_range_to_overwrite, download_interval_sec, daily_update_from_files, monthly_update_from_files FROM " + db_schema_name + "." + db_settings_table_name + "  order by start_download_ux_timestamp asc limit 1")
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


def get_connection():
    print("done")


def update_Settings():
    print("done") #  with parms!!!


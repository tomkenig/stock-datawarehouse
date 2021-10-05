from db_works import db_connect, db_tables
import datetime



def get_settings(interval_param_):
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()

    # interval parameter: current - API data; daily_hist - data from daily files; monthly_hist - data from monthly files
    if interval_param_ == "current":
        cursor.execute(
            "SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, "
            "current_range_to_overwrite, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp "
            "FROM " + db_schema_name + "." + db_settings_table_name + " WHERE current_update_from_api = 1 and "
                                                                      "download_setting_status_id = 0 and "
                                                                      "coalesce(next_download_ux_timestamp, 0) <= "
            + str(int(datetime.datetime.utcnow().timestamp())) + " order by next_download_ux_timestamp asc limit 1")
    elif interval_param_ == "daily_hist":
        cursor.execute("SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, "
                       "current_range_to_overwrite, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp "
                       "FROM " + db_schema_name + "." + db_settings_table_name + " WHERE daily_update_from_files = 1 and "
                                                                                 "download_setting_status_id = 0 and "
                                                                                 "daily_hist_complete = 0 AND "
                                                                                 "monthly_hist_complete = 1 AND "
                                                                                 "coalesce(start_hist_download_ux_timestamp, 0) <= "
                       + str(int(datetime.datetime.utcnow().timestamp())) + " order by start_hist_download_ux_timestamp asc limit 1")
    elif interval_param_ == "monthly_hist":
        cursor.execute("SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, "
                       "current_range_to_overwrite, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp "
                       "FROM " + db_schema_name + "." + db_settings_table_name + " WHERE monthly_update_from_files = 1 and "
                                                                                 "download_setting_status_id = 0 and "
                                                                                 "monthly_hist_complete = 0 AND "
                                                                                 "coalesce(start_hist_download_ux_timestamp, 0) <= "
                       + str(int(datetime.datetime.utcnow().timestamp())) + " order by start_hist_download_ux_timestamp asc limit 1")
    else:
         exit()

    download_setting = cursor.fetchall()
    if len(download_setting) > 0:
         download_settings_id = download_setting[0][0]
         market = download_setting[0][1]
         tick_interval = download_setting[0][2]
         data_granulation = download_setting[0][3]
         stock_type = download_setting[0][4]
         stock_exchange = download_setting[0][5]
         range_to_download = download_setting[0][6]
         download_api_interval_sec = download_setting[0][7]
         daily_update_from_files = download_setting[0][8]
         monthly_update_from_files = download_setting[0][9]
         start_hist_download_ux_timestamp = download_setting[0][10]

    else:
         print("no data to download")
         exit()

    # block current setting changing its status
    cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET download_setting_status_id = %s where download_settings_id = %s", (1, download_settings_id))
    cnxn.commit()
    print("settings blocked")
    return download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp


print()


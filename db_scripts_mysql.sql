-- DROP TABLE binance_download_settings;
CREATE TABLE binance_download_settings (
  `download_settings_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, -- unique setting identifier
  `market` varchar(10) DEFAULT NULL, -- market pair ie. BTCUSDT; ETHUSDT etc.
  `tick_interval` varchar(50) DEFAULT NULL, -- kline interval ie. 1m, 5m, 15m, 1h, 1M etc.
  `data_granulation`varchar(50) DEFAULT NULL, -- data granulation ie. klines, trades, aggregated trades
  `stock_type` varchar(255) DEFAULT NULL,  -- type of exchanege ie. spot
  `stock_exchange` varchar(255) DEFAULT NULL,  -- stock exchange name ie. Binance.com, ByBit.com etc.
  `current_range_to_overwrite` int(11) DEFAULT NULL,  -- how many intervals need to be overwrite/update when API module run
  `download_priority`int(11) NOT NULL,  -- priority, if there are many of settings records 
  `download_api_interval_sec`int(11) NOT NULL,  -- seconds to next overwrite current data from API
  `download_setting_status_id` int(11) DEFAULT NULL, -- download status 0-actual, 1-in progress
  `download_settings_desc` varchar(255) DEFAULT NULL, -- some text information about the setting, when you is needed
  `current_update_from_api`  int(1) DEFAULT 1, -- data for single setting is provided using API
  `daily_update_from_files`  int(1) DEFAULT 1, -- data for single setting is provided using daily files. Can be run once to get historical data
  `monthly_update_from_files`  int(1) DEFAULT 1, -- data for single setting is provided using monthly files. Can be run once to get historical data
  -- `daily_hist_first_run` int(1) DEFAULT 0, -- 
  -- `monthly_hist_first_run`  int(1) DEFAULT 0, --  
  `daily_hist_complete` int(1) DEFAULT 0, -- 
  `monthly_hist_complete`  int(1) DEFAULT 0,  --  
  `start_download_ux_timestamp` int(10) DEFAULT 1483225200, -- 2017/01/01 00:00:00
  `last_download_ux_timestamp` int(10) NULL, -- 
  `next_download_ux_timestamp` int(10) NULL, --
  `insert_ux_timestamp` int(10) NULL --
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- DROP TABLE binance_klines_data;
CREATE TABLE `binance_klines_data` (
  `open_time` bigint(20) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `close_time` bigint(20) DEFAULT NULL,
  `quote_asset_volume` double DEFAULT NULL,
  `number_of_trades` bigint(20) DEFAULT NULL,
  `taker_buy_base_asset_volume` double DEFAULT NULL,
  `taker_buy_quote_asset_volume` double DEFAULT NULL,
  `ignore` int(11) DEFAULT NULL,
  `market` varchar(10) DEFAULT NULL,
  `tick_interval` varchar(10) DEFAULT NULL,
  `stock_type` varchar(255) DEFAULT NULL,  
  `stock_exchange` varchar(255) DEFAULT NULL,  
  `update_ux_timestamp` int(10) NULL,
  `insert_ux_timestamp` int(10) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- DROP TABLE binance_hist_update_data_log;
CREATE TABLE binance_hist_update_data_log (
  `historical_data_log_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `market` varchar(10) DEFAULT NULL,
  `tick_interval` varchar(255) DEFAULT NULL,
  `stock_type` varchar(255) DEFAULT NULL,  
  `stock_exchange` varchar(255) DEFAULT NULL,
  `file_interval` varchar(255) DEFAULT NULL,
  `hist_date_name` varchar(255) DEFAULT NULL,
  `rec_count` bigint DEFAULT NULL,
  `historical_update_status` int DEFAULT NULL,
  `update_ux_timestamp` int(10) NULL,
  `insert_ux_timestamp` int(10) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- DROP VIEW `vw_binance_klines_anl`;
CREATE VIEW `vw_binance_klines_anl` AS
    SELECT 
        `a`.`open_time` AS `open_time`,
        `a`.`open` AS `open`,
        `a`.`high` AS `high`,
        `a`.`low` AS `low`,
        `a`.`close` AS `close`,
        `a`.`volume` AS `volume`,
        `a`.`close_time` AS `close_time`,
        `a`.`quote_asset_volume` AS `quote_asset_volume`,
        `a`.`number_of_trades` AS `number_of_trades`,
        `a`.`taker_buy_base_asset_volume` AS `taker_buy_base_asset_volume`,
        `a`.`taker_buy_quote_asset_volume` AS `taker_buy_quote_asset_volume`,
        `a`.`ignore` AS `ignore`,
        `a`.`market` AS `market`,
        `a`.`tick_interval` AS `tick_interval`,
        `a`.`stock_exchange` AS `stock_exchange`,
        `a`.`insert_ux_timestamp` AS `insert_timestamp`,
        FROM_UNIXTIME((`a`.`open_time` / 1000)) AS `open_datetime`,
        FROM_UNIXTIME((`a`.`close_time` / 1000)) AS `close_datetime`
    FROM
        `binance_klines_data` `a`;



-- some usefull data
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '1m', 'klines', 'spot', 'Binance.com', 20, 100, 120, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '5m', 'klines', 'spot', 'Binance.com', 10, 200, 120, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '15m', 'klines', 'spot', 'Binance.com', 10, 300, 120, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '30m', 'klines', 'spot', 'Binance.com', 10, 400, 120, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '1h', 'klines', 'spot', 'Binance.com', 5, 500, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '2h', 'klines', 'spot', 'Binance.com', 2, 600, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '4h', 'klines', 'spot', 'Binance.com', 2, 700, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '6h', 'klines', 'spot', 'Binance.com', 2, 700, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '8h', 'klines', 'spot', 'Binance.com', 2, 700, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '12h', 'klines', 'spot', 'Binance.com', 2, 700, 1200, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '1d', 'klines', 'spot', 'Binance.com', 2, 800, 12000, 1, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '1w', 'klines', 'spot', 'Binance.com', 2, 900, 12000, 0, 1, unix_timestamp());
INSERT INTO binance_download_settings (market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_priority, download_interval_sec, daily_update_from_files, monthly_update_from_files, insert_ux_timestamp) VALUES ('BTCUSDT', '1M', 'klines', 'spot', 'Binance.com', 2, 1000, 12000, 0, 1, unix_timestamp());




-- DROP TABLE download_settings;
CREATE TABLE download_settings (
  `download_settings_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `market` varchar(10) DEFAULT NULL,
  `tick_interval` varchar(10) DEFAULT NULL,
  `stock_exchange` varchar(255) DEFAULT NULL,  
  `api_range_to_overwrite` int(11) DEFAULT NULL,  
  `download_priority`int(11) NOT NULL,  
  `download_interval_sec`int(11) NOT NULL,  
  `download_setting_status_id` int(11) DEFAULT NULL,
  `download_settings_desc` varchar(255) DEFAULT NULL,
  `download_current_update_from_api`  int(11) DEFAULT NULL,
  `daily_update_from_files`  int(11) DEFAULT NULL,
  `monthly_update_from_files`  int(11) DEFAULT NULL,
  `start_download_timestamp`  int(11) DEFAULT NULL,
  `last_download_timestamp` bigint DEFAULT NULL,
  `next_download_timestamp` bigint DEFAULT NULL,
  `update_timestamp` timestamp NULL DEFAULT NULL,
  `insert_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- DROP TABLE klines_binance;
CREATE TABLE `klines_binance` (
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
  `stock_exchange` varchar(255) DEFAULT NULL,  
  `update_timestamp` timestamp NULL DEFAULT NULL,
  `insert_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- DROP TABLE historical_update_data_log;
CREATE TABLE historical_update_data_log (
  `historical_data_log_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `market` varchar(10) DEFAULT NULL,
  `tick_interval` varchar(10) DEFAULT NULL,
  `stock_exchange` varchar(255) DEFAULT NULL,
  `file_interval` varchar(255) DEFAULT NULL,
  `hist_date_name` varchar(255) DEFAULT NULL,
  `rec_count` bigint DEFAULT NULL,
  `historical_update_status` int DEFAULT NULL,
  `update_timestamp` timestamp NULL DEFAULT NULL,
  `insert_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- DROP VIEW `vw_klines_binance_anl`;
CREATE VIEW `vw_klines_binance_anl` AS
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
        `a`.`insert_timestamp` AS `insert_timestamp`,
        FROM_UNIXTIME((`a`.`open_time` / 1000)) AS `open_datetime`,
        FROM_UNIXTIME((`a`.`close_time` / 1000)) AS `close_datetime`
    FROM
        `klines_binance` `a`;



-- some usefull data
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '1m', 'Binance SPOT', 20, 100, 120, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '5m', 'Binance SPOT', 10, 200, 120, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '15m', 'Binance SPOT', 10, 300, 120, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '30m', 'Binance SPOT', 10, 400, 120, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '1h', 'Binance SPOT', 5, 500, 1200, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '2h', 'Binance SPOT', 2, 600, 1200, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '4h', 'Binance SPOT', 2, 700, 1200, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '1d', 'Binance SPOT', 2, 800, 12000, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '1w', 'Binance SPOT', 2, 900, 12000, 0);
INSERT INTO download_settings (market, tick_interval, stock_exchange, api_range_to_overwrite, download_priority, download_interval_sec, next_download_timestamp) VALUES ('BTCUSDT', '1M', 'Binance SPOT', 2, 1000, 12000, 0);

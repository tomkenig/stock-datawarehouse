#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Created on Wed Feb 12 08:43:52 2020
#@author: token
# version 0.2a
"""
info:
# json OAuth need to be generted under OAuth
# change raw_input to input (python3x)
# pickle require "config" catalog
oAuth:
todo:
json output
db insert
SITE_URL need to be dynamic generate from GSC data
Application need to collect all data after start date (ie. 2019-01-01), that are not in database
Application can be run under simple task
Application will be works once a day
pips:
pandas, google_auth_oauthlib, apiclient
pip install --upgrade google-api-python-client
pip install pyodbc
set interpreter as python on your system
"""
# tomkenig: import libs
import pickle
import pandas as pd
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
import pyodbc
import json
import time

# tomkenig: API authentication
OAUTH_SCOPE = ('https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/webmasters')
# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

try:
    credentials = pickle.load(open("config/credentials.pickle", "rb"))
except (OSError, IOError) as e:
    flow = InstalledAppFlow.from_client_secrets_file("json/client_secret_122350740012-tq24bkpfc93g6c2oc3qrbc2u3ka4mj2f.apps.googleusercontent.com.json", scopes=OAUTH_SCOPE)
    credentials = flow.run_console()
    pickle.dump(credentials, open("config/credentials.pickle", "wb"))

# Connect to Search Console Service using the credentials
webmasters_service = build('webmasters', 'v3', credentials=credentials)


# tomkenig: vars
start_date = datetime.strptime(str(datetime.now() - timedelta(days=3))[0:10], "%Y-%m-%d")
#end_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
#date = datetime.strptime("2020-02-01", "%Y-%m-%d")
date = datetime.strptime(str(datetime.now() - timedelta(days=3))[0:10], "%Y-%m-%d")
maxRows = 25000
i = 0
output_rows = []


# sql sever connecion
    # Specifying the ODBC driver, server name, database, etc. directly
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-OD9LPJP;DATABASE=google;UID=sa;PWD=r2wd8TW!@34')
    # Using a DSN, but providing a password as well
    #conn = pyodbc.connect('DSN=test;PWD=password')
    # Create a cursor from the connection
cursor = conn.cursor()

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# tomkenig: list od dates
def out_date_range(argStartDate, argEndDate):
    delta = argEndDate - argStartDate
    l = []
    for i in range(delta.days + 1):
        day = argStartDate + timedelta(days=i)
        l.insert(i, str(day))
        # print(day)
    return (l)

# test print(out_date_range(s_date,e_date))


# tomkenig: get verified siteUrl list
def get_verified_siteurl_list():
    site_list = webmasters_service.sites().list().execute()
    verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                           if s['permissionLevel'] != 'siteUnverifiedUser'
                           and s['siteUrl'][:4] == 'http']
    return verified_sites_urls

# tomkenig: check function
#print (get_verified_siteurl_list())
#or
#for site_url in get_verified_siteurl_list():
#    print (site_url)

# download google search console site data
def out_gsc_data(argUrl, argDate):
    i=0
    request = {
            "startDate": argDate,
            "endDate": argDate,
            "dimensions": ["query", "page", "country", "device"], "searchType": "Web",
            "rowLimit": maxRows,
            "startRow": i * maxRows
            }
    response = webmasters_service.searchanalytics().query(siteUrl=argUrl, body=request).execute()
    return response

# tomkenig: check function
#print(out_gsc_data('https://officeinside.org/', date.strftime("%Y-%m-%d")))


# tomkenig: Output as pandas dataFrame
def out_pandas_dataframe(argResponse):
    for row in argResponse['rows']:
        keyword = row['keys'][0]
        page = row['keys'][1]
        country = row['keys'][2]
        device = row['keys'][3]
        output_row = [keyword, page, country, device, row['clicks'], row['impressions'], row['ctr'],
                      row['position']]
        output_rows.append(output_row)
    df = pd.DataFrame(output_rows, columns=['query','page', 'country', 'device', 'clicks', 'impressions', 'ctr', 'avg_position'])
    return df
# test
#print( out_pandas_dataframe(out_gsc_data('https://officeinside.org/', date.strftime("%Y-%m-%d"))))

# tomkenig: Output as text file
def out_text_file(argDataframe, argPath):
    argDataframe.to_csv(argPath)
# test
#out_text_file(out_pandas_dataframe(out_gsc_data('https://officeinside.org/', date.strftime("%Y-%m-%d"))), 'gsc_output.csv')

# tomkenig: Output as JSON
# tomkenig: Output as insert JSON to database
# tomkenig: Output as insert rows and column to database

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
# insert JSON into database

for date in out_date_range(start_date, date):
    for site in get_verified_siteurl_list():
        cursor.execute("delete from dwhlite.gsc.dat_google_search_console where gscSiteUrl=? and gscDate=?", site, date)
        cursor.execute("insert into dwhlite.gsc.dat_google_search_console(gscData, gscSiteUrl, gscDate) values (?, ?, ?)", json.dumps(out_gsc_data(site, str(date)[0:10])), site, date)
        conn.commit()
        print(site)
    time.sleep(10)
    # x seconds sleep. Sometimes API response Rate Limit Exceeded
    print(date)

print('done')

#TODO:
# +++++valid json function
# +++++check "," and "'" if is needed to replace it
# +++++funkcja przeksztalcajaca str output na string, json, z poprawkami, zeby funkcje json na sql server dzialaly
# output web,images, other
# search by page, keayword etc
# starter
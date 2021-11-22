import requests
import json
import pandas as pd

# Constant variable functions
# URL for all: https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioni.php
# PARAMS for all: ?tipo=JSON
# At time of coding (22 Nov 2021) there were 3534 total associazioni listed
# URL for individual: https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioniDetail.php
# PARAMS for individual: ?tipo=JSON&numero=3
url = 'https://portale.comune.venezia.it/sites/all/modules/yui_venis/associazioniDetail.php'
params = {'tipo': 'JSON'}
rows = []


def scrapeCurrentData(itemNum=0, end=0):

    # Define the parameters
    params['numero'] = itemNum

    r = requests.get(url, params=params)
    r.encoding = 'utf-8'

    # Parse JSON file


            rows.append({'id': id,
                         'title': title,
                         'lat': lat,
                         'lon': lon})

        elif display_id == 'events':
            id = item.find('id').text
            title = item.find('title').text
            location = item.find('location').text
            location_id = item.find('location_id').text
            category = item.find('category').text
            start_date = item.find('start_date').text
            start_time = item.find('start_time').text
            end_date = item.find('end_date').text
            end_time = item.find('end_time').text

            rows.append({'id': id,
                         'title': title,
                         'location': location,
                         'location_id': location_id,
                         'category': category,
                         'start_date': start_date,
                         'start_time': start_time,
                         'end_date': end_date,
                         'end_time': end_time})

    if itemNum == end:
        # create column headers
        cols = ['id', 'title', 'location', 'location_id',
                'category', 'start_date', 'start_time',
                'end_date', 'end_time']

        # Make dataframe
        df = pd.DataFrame(rows, columns=cols)
        # write dataframe to csv
        df.to_csv('associazioni_utf-8.csv', encoding='utf-8-sig')
        print('associazioni_utf-8.csv has been made in the folder and can now be accessed.')
    else:
        itemNum += 1
        if itemNum % 20 != 0:
            print(str(itemNum) + " points logged")
        scrapeCurrentData(itemNum, end)


# 3534 at current time
scrapeCurrentData(end=3535)

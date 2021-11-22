import requests
import xml.etree.ElementTree as ET
import pandas as pd  

# Constant variable functions
url = 'https://evenice.it/exports/views/contents.xml'
params = dict()
rows = []

def scrapeCurrentData(display_id, page = 0, end = 0):
    
    # Define the parameters 
    params['display_id'] = display_id
    params['page'] = page
    
    r = requests.get(url, params=params)
    r.encoding = 'utf-8'

    # Parse XML file
    parser = ET.XMLParser(encoding='UTF-8')
    root = ET.fromstring(r.text, parser=parser)
    
    for item in root.find('items'):
        if display_id == 'locations':
            id = item.find('id').text
            title = item.find('title').text
            lat = item.find('lat').text
            lon = item.find('lon').text
            
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
    
    # Get the amount of results if the first time
    if end == 0:
        totalCount = root.find('totalCount')
        end = int(int(totalCount.text) / 50)
            
    if page == end:
        # create column headers
        if display_id == 'locations':
            cols = ['id', 'title', 'lat', 'lon']
        elif display_id == 'events':
            cols = ['id', 'title', 'location', 'location_id',
                    'category', 'start_date', 'start_time',
                    'end_date', 'end_time']

        # Make dataframe
        df = pd.DataFrame(rows, columns = cols) 
        # write dataframe to csv
        df.to_csv(display_id + '_utf-8.csv', encoding='utf-8-sig')
        print(display_id + '_utf-8.csv has been made in the folder and can now be accessed.')
    else:
        page += 1
        print(str(50*page) + " points logged")
        scrapeCurrentData(display_id, page, end)

 
scrapeCurrentData('locations')
# reset rows
rows = []
scrapeCurrentData('events')


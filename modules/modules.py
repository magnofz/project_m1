import pandas as pd
import requests
import json
from shapely.geometry import Point
import geopandas as gpd
from fuzzywuzzy import process

#########################################################################################################################################
## GEOCALCULATION FUNCTIONS
#########################################################################################################################################

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between two latitude/longitude pair points in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

#########################################################################################################################################
## API COM. MADRID - REQUEST/DATAFRAME
#########################################################################################################################################

def request_api_cmadrid(ep, place):
    #request info from com. madrid api and turn it into a dataframe
    monuments = requests.get(ep).json()
    dict_monuments = {'Place of interest' : [monuments['@graph'][t]['title'] for t in range(len(monuments['@graph']))],
                      'Type of place' : 'Monumento de la ciudad de Madrid',
                      'Place address' : [monuments['@graph'][a]['address']['street-address'] for a in range(len(monuments['@graph']))]}

    dict_monuments['mon_lat'] = []
    dict_monuments['mon_lon'] = []

    for i in range(len(monuments['@graph'])):
        try:
            dict_monuments['mon_lat'].append(monuments['@graph'][i]['location']['latitude'])
            dict_monuments['mon_lon'].append(monuments['@graph'][i]['location']['longitude'])
        except:
            dict_monuments['mon_lat'].append(None)
            dict_monuments['mon_lon'].append(None)
    
    df_monuments = pd.DataFrame(dict_monuments)
    df_monuments = df_monuments[df_monuments['mon_lat'].notna()]
    
    if place != '':
        choices = dict_monuments['Place of interest']
        fuzzy_name = process.extractOne(place, choices)[0]
        df_monuments = df_monuments[df_monuments['Place of interest'] == fuzzy_name]
    
    return df_monuments

#########################################################################################################################################
## API BICIMAD - REQUEST/DATAFRAME
#########################################################################################################################################

def request_api_bicimad(ep_1, ep_2, mail, pw, flag):
    #request info from bicimad api and turn it into a dataframe
    headers_login = {'email': mail, 'password' : pw}
    token = requests.get(ep_1, headers=headers_login).json()['data'][0]['accessToken']
    bici_json = requests.get(ep_2, headers={'accessToken' : token}).json()

    dict_bici = {'BiciMAD Station' : [bici_json['data'][b]['name'] for b in range(len(bici_json['data']))],
             'Station Location' : [bici_json['data'][l]['address'] for l in range(len(bici_json['data']))],
             'Bikes Available' : [bici_json['data'][d]['dock_bikes'] for d in range(len(bici_json['data']))],
             'bic_lat' : [bici_json['data'][y]['geometry']['coordinates'][1] for y in range(len(bici_json['data']))],
             'bic_lon' : [bici_json['data'][x]['geometry']['coordinates'][0] for x in range(len(bici_json['data']))]}
    
    df_bicimad = pd.DataFrame(dict_bici)
    
    if not flag:
        df_bicimad = df_bicimad[df_bicimad['Bikes Available'] > 0].reset_index()
        df_bicimad.drop(columns='index', inplace=True)

    return df_bicimad

#########################################################################################################################################
## FULL DATAFRAME CALCULATION
#########################################################################################################################################

def full_df_calc (df1, df2):
    #calculate the distances between monuments df and bicimad df and return a dataframe with the closest station per each monument
    full_df = df1.merge(df2, how='cross')
    full_df['pit'] = full_df.apply(lambda x : (x['mon_lat'] - x['bic_lat'])**2 + (x['mon_lon'] - x['bic_lon'])**2 , axis=1)
    bici_min = pd.DataFrame(full_df.groupby(['Place of interest', 'Place address', 'mon_lat', 'mon_lon'])['pit'].min())
    bici_min = bici_min.reset_index()
    mon_bici = bici_min.merge(full_df, how='left').sort_values(by=['Place of interest'])
    mon_bici['Distance (m)'] = mon_bici.apply(lambda x : distance_meters(x['mon_lat'], x['mon_lon'], x['bic_lat'], x['bic_lon']), axis=1)
    mon_bici['Walking time (min)'] = mon_bici.apply(lambda x : x['Distance (m)'] / 1000 * 12.5, axis=1)
    mon_bici['Distance (m)'], mon_bici['Walking time (min)'] = mon_bici['Distance (m)'].astype(int), mon_bici['Walking time (min)'].astype(int)
    final_df = mon_bici[['Place of interest', 'Type of place', 'Place address', 'BiciMAD Station', 'Station Location',
                         'Bikes Available', 'Distance (m)', 'Walking time (min)']]

    return final_df

#########################################################################################################################################
## SAVE CSV FILE
#########################################################################################################################################
def save_results(final_df, data_loc, data_file):
    #save final data into a csv file
    final_df.to_csv(data_loc + data_file)
    return
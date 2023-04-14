# import library

from modules import modules as m
import argparse

#argparse

def argument_parser():
    parser = argparse.ArgumentParser(description= 'Find the closest BiciMAD station')
    help_message_l ='Use -l to specify the point of interest of your choice' 
    help_message_f = 'Do not filter BiciMAD stations by bikes avaibility'
    parser.add_argument('-l', '--location', help=help_message_l, type=str, default='')
    parser.add_argument('-f', '--filter', help=help_message_f, action='store_true')
    args = parser.parse_args()
    return args


# Variables

base_url = 'https://datos.madrid.es/egob/'
resource = 'catalogo/300356-0-monumentos-ciudad-madrid.json'
endpoint = base_url + resource

bici_db_loc = './data/bicimad.db'
save_in = './data/'
save_name = 'mon_bici.csv'
place = argument_parser().location
unfilter = argument_parser().filter

# Pipeline execution

if __name__ == '__main__':
    DF_MON = m.request_api_cmadrid(endpoint, place)
    DF_BICI = m.request_api_bicimad(bici_db_loc, unfilter)
    DF_FINAL = m.full_df_calc (DF_MON, DF_BICI)
    m.save_results(DF_FINAL, save_in, save_name)
        
    print(f'Success: {save_name} file was saved in the {save_in} directory!')
#!/usr/bin/env python3

# Standard library imports
import os
from ast import literal_eval

# Local application imports
from .read_csv import get_columns as gc, get_header as gh

def get_bmc_creds(csv_file, bmc_sw, bmc_sw_header, bmc_mac_header, bmc_pass_header):
    
    bmc_sw_list = gc(csv_file, bmc_sw_header)
    bmc_mac_list = gc(csv_file, bmc_mac_header)
    bmc_pass_header = gc(csv_file, bmc_pass_header)

    # Define filename convention
    bmc_sw = bmc_sw_list[0]
    msw_switch = str(bmc_sw.replace('.packet.net',''))
    bmc_sw_file = f'{bmc_sw_header}.{msw_switch}'

    mac_list = []
    for m in bmc_mac_list:
        mac = m.lower()
        mac_list.append(mac)
    
    # Read file generated came frome msw
    with open(f'{bmc_sw_file}.txt', 'r') as sw_name:
        contents = sw_name.read()
        dictionary = literal_eval(contents)
       
    # Fetch the IP address and password and write into a file
    filePath = str(f'bmc_creds_{msw_switch}.txt')
    with open(filePath, 'w') as bmc_creds:
        for key, val in dictionary.items():
            for i in range(len(mac_list)):
                if f'{key}' in mac_list[i]:
                    bmc_password_value = bmc_pass_header[i]
                    bmc_creds.write(str(key) +" "+ str(val) +" " + str(bmc_password_value) + "\n")      


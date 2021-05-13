#!/usr/bin/env python3

# Standard library imports
import csv, os, json

# Local application imports
from .read_csv import get_columns as gc, get_csv_to_dict as gcsv_dict
from .utils import convert


def get_sw_info(csv_file, esr_sw, eth_sw_header, eth_swp_header):
    # print(f"\n - ESR - access test on {esr_sw}")
    esr_swp_list = gc(csv_file, eth_swp_header)
    
    port_desc = esr_swp_list[0]
    esr_ssh = None
    if "Ethernet" in port_desc:
        # print("ESR: Arista switch")
        esr_swp =','.join(esr_swp_list)
        esr_ssh = f'ssh -q {esr_sw} "show interfaces {esr_swp} description"'

    elif "xe" in port_desc:
        # print("ESR: Juniper switch")
        esr_swp ='|'.join(esr_swp_list)
        esr_ssh = f'ssh -q {esr_sw} \'show interfaces descriptions | match "{esr_swp}"\''
    # Define filename convention
    esr_switch = str(esr_sw.replace('.packet.net',''))
    tmp_file = f'tmp_{eth_sw_header}.{esr_switch}'
    eth_sw_file = f'{eth_sw_header}.{esr_switch}'

    tmp = f'{tmp_file}.txt'
    output = os.popen(esr_ssh)

    with open(tmp, 'w') as tmp_file:
        for o in output:
            tmp_file.write(o)

    # Getting the csv file converted into dictionary
    file_csv_to_dict = gcsv_dict(csv_file) 

    # Getting the rack position
    rack_dict = {}
    for rk in file_csv_to_dict:
        rk_position = "rack_position"
        eth_swp = eth_swp_header
        rack = { rk[rk_position]: rk[eth_swp]}
        rack_dict.update(rack)

    # Reading from file and create another file
    with open(tmp, 'r') as tmp_file:
        response = os.popen(f'cat {tmp} | awk '"'{print $1, $2}'"f' | tail -n +2')

        # Merge to single dictionary in a list
        eth_dict = {}
        if 'Ethernet' in port_desc: # For Arista switches   
            for r in response:
                o = r.split()
                orig_dict = convert(o)
                corrected_dict = {k.replace('Et', 'Ethernet'): v for k, v in orig_dict.items()}
                eth_dict.update(corrected_dict)
        else: # For Juniper switches
            for r in response:
                o = r.split()
                orig_dict = convert(o)
                eth_dict.update(orig_dict)
        
        rk_eth_dict = {}
        for rk_k, rk_v in rack_dict.items():
            rk_eth_dict[rk_k] = {}
            eth_rk = dict()
            for eth_k, eth_v in eth_dict.items():
                if eth_k == rk_v:
                    new_dict = {eth_k: eth_v}
                    eth_rk.update(new_dict)
            rk_eth_dict[rk_k].update(eth_rk)

    with open(f'{eth_sw_file}.txt', 'w') as eth_file:
        eth_file.write(str(rk_eth_dict))

 
# get_esrSw_info(csv_file, esr_sw, eth_sw_header, eth_swp_header)
# get_esrSw_info("rk09.p01.fr2.24-30_enrollment_data.csv", "esr1a.rk09.p01.fr2.packet.net", "eth0_switch", "eth0_switchport")

# Getting the rack postion definition

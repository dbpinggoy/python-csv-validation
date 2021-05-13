#!/usr/bin/env python3

# Standard library imports
import os

# Local application imports
from .read_csv import get_columns as gc
from .utils import convert

def get_bmcsw_info(csv_file, bmc_sw, bmc_sw_header, bmc_swp_header, bmc_mac_header):
    
    bmc_swp_list = gc(csv_file, bmc_swp_header)
    bmc_mac_list = gc(csv_file, bmc_mac_header)

   # Check msw if Arista or Juniper switch
    port_val = bmc_swp_list[0]
    bmc_ssh=None
    if "Ethernet" in port_val:
    #    print("\n MSW: Arista switch:")
       listing=[item.replace(':','') for item in bmc_mac_list]
       
       # MAC format for arista switch
       formatted_macs = []
       for macs in listing:
            modified_mac = '.'.join(macs[i:i+4] for i in range(0, len(macs), 4))
            formatted_macs.append(modified_mac)
       bmc_macs = '|'.join(formatted_macs).lower()
       bmc_ssh = f'ssh -q {bmc_sw} "show ip arp | i {bmc_macs}"'
       
    elif "ge" in port_val:
        print("\n MSW: Juniper switch")
        bmc_macs = '|'.join(bmc_mac_list).lower()
        bmc_ssh = f'ssh -q {bmc_sw} \'show arp no-resolve | match "{bmc_macs}"\''

    # Define filename convention
    msw_switch = str(bmc_sw.replace('.packet.net',''))
    tmp_file = f'tmp_{bmc_sw_header}.{msw_switch}'
    bmc_sw_file = f'{bmc_sw_header}.{msw_switch}'

    # Create file and redirect output to file.
    tmp = f'{tmp_file}.txt'
    output = os.popen(bmc_ssh)

    with open(tmp, 'w') as f:
        for o in output:
            f.write(o)

    # Reading from file and create another file
    with open(tmp, 'r') as f:
        response=None
        if "Ethernet" in port_val:
            response = os.popen(f'cat {tmp} | awk '"'{print $1, $3}'"'')
        elif "ge" in port_val:
            response = os.popen(f'cat {tmp} | awk '"'{print $1, $2}'"'')
        # merge to single dictionary in a list
        eth_list = dict()
        if "Ethernet" in port_val:
            for r in response:
                o = r.split()
                ori_dict = convert(o)
                formatted_dict = {i: j.replace('.', '') for i, j in ori_dict.items()}
                mac_keys = next(iter(formatted_dict.keys()))  
                mac_values = next(iter(formatted_dict.values()))       
                formatted_mac = ':'.join(mac_values[i:i+2] for i in range(0, len(mac_values), 2))

                new_values = {formatted_mac:mac_keys}
                eth_list.update(new_values)
        else:
            for r in response:
                o = r.split()
                ori_dict = convert(o)
                eth_list.update(ori_dict)
    with open(f'{bmc_sw_file}.txt', 'w') as bmc_new_info:
        bmc_new_info.write(str(eth_list))


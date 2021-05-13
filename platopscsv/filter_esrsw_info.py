#!/usr/bin/env python3

# Standard library imports
from colorama import Fore, Back, Style

# Local application imports
from .read_csv import get_columns as gc, get_header as gh
from .get_esrsw_info import get_sw_info as get_sw_info
from .get_swpstatus import get_swp_status as swp_status


def filter_ethsw_and_ethswp(csv_file):
    header = gh(csv_file)
    # Filtering eth*_switch
    get_sw = filter(lambda i: "eth" in i and "switch" in i and not "switchport" in i, header)
    list_eth_sw = list(get_sw)

    # Filtering eth*_switchport
    get_swp = filter(lambda i: "eth" in i and "switchport" in i, header)
    list_eth_swp = list(get_swp)

    filtered_sw = []
    for item in range(len(list_eth_sw)):
        eth_col = list_eth_sw[item]
        # Get the column values on the specific column
        columns = gc(csv_file, eth_col)
        set_filtered_sw = set(columns) #Get only 1 value in the column
        list_filtered_sw = list(set_filtered_sw)

        for f_sw in list_filtered_sw:
            filtered_sw.append(f_sw)  
    
    if len(list_eth_sw) == 2 and len(list_eth_swp) == 2:
        for esr_sw in filtered_sw:            
            for sw, swp in zip(list_eth_sw, list_eth_swp):
                if 'esr1a' in esr_sw and 'eth0_switch' in sw and 'eth0_switchport' in swp:
                    print("\n - Checking on ESR1A: eth0_switchport")
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)
                elif 'esr1b' in esr_sw and 'eth1_switch' in sw and 'eth1_switchport' in swp: 
                    print("\n - Checking on ESR1B: eth1_switchport")                  
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)

    if len(list_eth_sw) > 2 and len(list_eth_swp) > 2:
         for esr_sw in filtered_sw:            
            for sw, swp in zip(list_eth_sw, list_eth_swp):
                if 'esr1a' in esr_sw and 'eth0_switch' in sw and 'eth0_switchport' in swp:
                    print("\n - Checking on ESR1A: eth0_switchport")                 
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)
                elif 'esr1a' in esr_sw and 'eth1_switch' in sw and 'eth1_switchport' in swp:
                    print("\n - Checking on ESR1A: eth1_switchport")                   
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)
                elif 'esr1b' in esr_sw and 'eth2_switch' in sw and 'eth2_switchport' in swp:
                    print("\n - Checking on ESR1B: eth2_switchport")                
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)
                elif 'esr1b' in esr_sw and 'eth3_switch' in sw and 'eth3_switchport' in swp:
                    print("\n - Checking on ESR1B: eth3_switchport")               
                    get_sw_info(csv_file, esr_sw, sw, swp)
                    swp_status(csv_file, esr_sw, sw, swp)


# filter_ethsw_and_ethswp("AMS1-PLATOPS-1216-03112021-n2.xlarge.x86v1-r03b01-c312h.csv")
#filter_ethSw_and_ethSwp("rk09.p01.fr2.24-30_enrollment_data.csv")
# filter_ethSw_and_ethSwp("DA11-PLATOPS-978-01122021-n2.xlarge.x86v1 - RK30.csv")
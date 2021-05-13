#!/usr/bin/env python3

# Standard library imports
import subprocess
from collections import OrderedDict
from tabulate import tabulate
from colorama import Fore, Back, Style

# Local application imports
from .read_csv import get_columns as gc, get_csv_to_dict as gcsv_dict


def access_test(csv_file, bmc_sw, bmc_user):
    
    msw_switch = str(bmc_sw.replace('.packet.net',''))
    filepath = str(f'bmc_creds_{msw_switch}.txt') 

    # Getting the BMC user
    bmc_user = gc(csv_file, bmc_user)
    
    # Getting the rack postion definition
    file_csv_to_dict = gcsv_dict(csv_file) 

    ipmi_cmd = "ipmitool"
    ipmi_user = bmc_user[0]

    print("\n - IPMI access testing...")
    table_headers = ["Rack Position", "BMC MAC", "BMC IP", "BMC User", "BMC Password", "Remarks"]
    mapped_data = []

    with open(filepath) as bmc_creds:
        # Getting the rack position
        rack_dict = {}
        for rk in file_csv_to_dict:
            rk_position = "rack_position"
            bmc_mac = "bmc_mac"
            rack = { rk[rk_position]: rk[bmc_mac]}
            rack_dict.update(rack)

        
        for line in bmc_creds.readlines():
            lines = line.rstrip('\n')
            values = lines.split(" ")
            ipmi_server = values[1]
            ipmi_password = values[2]
            
            p = subprocess.run([ipmi_cmd, "-H", ipmi_server, "-U", ipmi_user, "-P", ipmi_password, "-I", "lanplus", "raw", "0x06","0x01"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output= p.returncode

            for rk_key, rk_val in rack_dict.items():
                if rk_val == values[0]:
                    if (output == 0):
                        mapped_data.append([rk_key, rk_val, ipmi_server, ipmi_user, ipmi_password, Fore.GREEN + '✔ [success]' + Style.RESET_ALL])
                    else:
                        mapped_data.append([rk_key, rk_val, ipmi_server, ipmi_user, ipmi_password, Fore.RED + '✘ [failed]' + Style.RESET_ALL])

    print(tabulate(mapped_data, table_headers, tablefmt="pretty"))
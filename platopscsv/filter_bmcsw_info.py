#!/usr/bin/env python3

# Local application imports
from .read_csv import get_columns as gc, get_header as gh
from .get_bmcsw_info import get_bmcsw_info as get_bmc_sw
from .get_bmcsw_creds import get_bmc_creds as gen_bmc_creds
from .ipmi_access import access_test as access
from .get_dell_mac_data import validate_mac as val_mac_data, get_mac_data as get_eth_mac
from .utils import is_vendor

def filter_bmcsw_and_bmcswp(csv_file, vendor):
    all_header_list = gh(csv_file)

    filtered_bmc_sw = []
    if "bmc_switch" in all_header_list:
        bmc_sw = "bmc_switch"
        
        # Get the column values on the specific column
        column = gc(csv_file, bmc_sw)
        set_filtered_sw = set(column) #Get only 1 value in the column
        list_filtered_bmc_sw = list(set_filtered_sw)
        
        # Append the filtered BMC switch for later use
        for f_bmc_sw in list_filtered_bmc_sw:
            filtered_bmc_sw.append(f_bmc_sw)     

    filtered_swp = []
    if "bmc_switchport" in all_header_list:
        bmc_swp = "bmc_switchport"

        # Get the column values on the specific column
        column = gc(csv_file, bmc_swp)
        set_filtered_swp = set(column) #Get only 1 value in the column
        list_filtered_swp = list(set_filtered_swp)

        # Append the filtered BMC switchport for later use
        for f_swp in list_filtered_swp:
            filtered_swp.append(f_swp) 


    # Header variables
    bmc_sw_hdr, bmc_swp_hdr, bmc_mac_hdr, bmc_user_hdr, bmc_pass_hdr = "bmc_switch", "bmc_switchport", "bmc_mac", "bmc_username", "bmc_password"

    for bmc_sw in filtered_bmc_sw:
        # Generate BMC information
        if "bmc_switch" and "bmc_switchport" and "bmc_mac" in all_header_list:
            get_bmc_sw(csv_file, bmc_sw, bmc_sw_hdr, bmc_swp_hdr, bmc_mac_hdr)

    for bmc_sw in filtered_bmc_sw:
        # Get the bmc credentialss
        if "bmc_mac" and "bmc_username" and "bmc_password" in all_header_list:
            print("Generating bmc credentials...")
            gen_bmc_creds(csv_file, bmc_sw, bmc_sw_hdr, bmc_mac_hdr, bmc_pass_hdr)
            
            # Test server access with IPMI
            access(csv_file, bmc_sw, bmc_user_hdr)

            # Get vendor and match mac address
            check_vendor = is_vendor(csv_file)
            if vendor == "dell":
                for bmc_user, bmc_pass in check_vendor.items():
                    if bmc_user == 'root' and bmc_pass == 'calvin':
                        get_eth_mac(csv_file, bmc_sw, bmc_user_hdr)
                        val_mac_data(csv_file, bmc_sw, bmc_user_hdr, bmc_mac_hdr)
                    else:
                        print("\n - FAILED: Your server vendor is not Dell!") 
            else:
                print("The vendor provided is not define")
        else:
            print("Required in the CSV file: bmc_username and bmc_password")
            exit()     


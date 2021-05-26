#!/usr/bin/env python3

# Standard library imports
import requests, warnings, re, json, csv
from ast import literal_eval
from colorama import Fore, Back, Style
from tabulate import tabulate

warnings.filterwarnings("ignore")

# Local application imports
from .read_csv import get_columns as gc, get_header as gh, get_csv_to_dict as gcsv_dict
from .utils import convert, sort_table

def get_mac_address(idrac_ip,idrac_username,idrac_password):
    mac_address = 'PermanentMACAddress'
    link_status = 'LinkStatus'
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    nic_fqdds = []
    for i in data['Members']:
        for ii in i.items():
            fqdd = (ii[1].split("/")[-1])
            nic_fqdds.append(fqdd)
    macs = []
    for i in sorted(nic_fqdds):
        response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/%s' % (idrac_ip, i),verify=False,auth=(idrac_username, idrac_password))
        data = response.json()
        if mac_address in data.keys() and link_status in data.keys():
            if data[mac_address] != "" and data[link_status] == "LinkUp":
                # print("%s: %s" % (i, data[mac_address]))
                macs.append((i, data[mac_address]))
            # else:
            #     print("- WARNING, unable to locate property \"%s\". Either spelling of property is incorrect or property not supported for %s" % (ii, i))
    mac_dict = dict()
    # mac_list = []
    for index, mac in enumerate(macs):
        orig_dict = convert(mac)
        corrected_mac = dict((f"eth{index}_mac", value.lower()) for (key, value) in orig_dict.items())
        mac_dict.update(corrected_mac)
    # mac_list.append(mac_dict)
    return mac_dict

def get_mac_data(csv_file, bmc_sw, bmc_user):

    msw_switch = str(bmc_sw.replace('.packet.net',''))
    bmc_sw_file = str(f'bmc_switch.{msw_switch}.txt')
    filepath = str(f'bmc_creds_{msw_switch}.txt') 

    # File naming for generating txt file for eth macs
    eth_name = re.sub(r'\bmsw\d*\b', '', msw_switch)
    eth_macs_list = str(f'eth_macs{eth_name}.txt')

    # Getting the rack postion definition
    file_csv_to_dict = gcsv_dict(csv_file)   

    idrac_user = gc(csv_file, bmc_user)
    idrac_username = idrac_user[0]

    
    with open(filepath, "r") as serverList:

        # Getting the rack position
        rack_dict = {}
        for rk in file_csv_to_dict:
            rk_position = "rack_position"
            bmc_mac = "bmc_mac"
            rack = { rk[rk_position]: rk[bmc_mac]}
            rack_dict.update(rack)

        eth_macs_value = {}
        for line in serverList.readlines():
            lines = line.rstrip('\n')
            values = lines.split(" ")
            idrac_ip = values[1]
            idrac_password = values[2]
            nic_macs = get_mac_address(idrac_ip,idrac_username,idrac_password)

            nic_mac_list = []
            
            with open(f'{bmc_sw_file}', 'r') as sw_name:
                contents = sw_name.read()
                bmc_dict = literal_eval(contents)  
                for rk, rv in rack_dict.items():
                    for key, value in bmc_dict.items():
                        if idrac_ip == value and key == rv :
                            # Adding rack position in the dictionary file                            
                            rk_position = {"rack_position": rk}                            
                            add_rack = {**rk_position, **nic_macs}
                            nic_mac_list.append(add_rack)

                            # Append new dictionary values with rack postions
                            new_values = {key: nic_mac_list}
                            eth_macs_value.update(new_values)           
   # Creating a file with json format
    with open(eth_macs_list, 'w') as eth_macs:
        eth_json = json.dumps(eth_macs_value)
        eth_macs.write(str(eth_json))
    
def validate_mac(csv_file, bmc_sw, bmc_user, bmc_mac):
    msw_switch = str(bmc_sw.replace('.packet.net',''))
    # File naming for getting txt file for eth macs
    eth_name = re.sub(r'\bmsw\d*\b', '', msw_switch)
    eth_macs_list = str(f'eth_macs{eth_name}.txt')

    # Getting the ethx_mac headers from csv
    headers = gh(csv_file)
    eth_mac_header = filter(lambda i: "eth" in i and "mac" in i, headers)
    eth_mac_hdr_list = []
    for eth_mac_row in eth_mac_header:
        eth_mac_hdr_list.append(eth_mac_row)
 
    # Generating csv to dictionary
    file_csv_to_dict = gcsv_dict(csv_file)
    keydict= {}
    for key in file_csv_to_dict:
        keydict[key['bmc_mac']] = []
        bmc_key = keydict[key['bmc_mac']]
        rk_position = 'rack_position'

        eth_dict = dict()
        for eth_hdr in eth_mac_hdr_list:
            eth_list = {rk_position: key[rk_position], eth_hdr: key[eth_hdr]}
            eth_dict.update(eth_list)
        bmc_key.append(eth_dict)

    with open(eth_macs_list, 'r') as json_file:
        data = json.load(json_file)

    print("\n - Matching MAC address from csv to the server...")
    table_headers = ["Rack Position", "BMC MAC", "Ethernet", "Ethernet MAC", "Remarks"]
    mapped_data = []
    table_sorted = []
    for k1 in data.keys():
        for p1 in data[k1]:
            for k2 in keydict.keys():
                if k1 in k2:
                    x = keydict[k2][0]
                    xx = dict(list(x.items())[1:])
                    y = data[k1][0]
                    yy = dict(list(y.items())[1:])
                    dicta_set = set(xx.items())
                    dictb_set = set(yy.items())
                    setinter = dictb_set.intersection(dicta_set)
                    setdiff = dictb_set.difference(dicta_set)
                    for k, v in setdiff:
                        mapped_data.append([
                            x['rack_position'],
                            Fore.LIGHTYELLOW_EX + x['rack_position'] + Style.RESET_ALL,
                            Fore.LIGHTYELLOW_EX + k1 + Style.RESET_ALL,
                            Fore.LIGHTYELLOW_EX + f'{k}', f'{v}' + Style.RESET_ALL,
                            Fore.RED + '✘ [not match]' + Style.RESET_ALL])
                    for k, v in setinter:
                        mapped_data.append([
                            x['rack_position'],
                            x['rack_position'], k1, f'{k}', f'{v}',
                            Fore.GREEN + '✔ [match]' + Style.RESET_ALL])    

    for row in sort_table(mapped_data, 0):
        table_sorted.append(row[1:])   
                                               
    print(tabulate(table_sorted, table_headers, tablefmt="pretty"))
            
       
        
    
        


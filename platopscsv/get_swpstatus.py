#!/usr/bin/env python3

# Standard library imports
import os
from ast import literal_eval
from colorama import Fore, Back, Style
from tabulate import tabulate

# Local application imports
from .read_csv import get_columns as gc
from .utils import sort_table


def get_swp_status(csv_file, sw, sw_header, swp_header):
    swp_list = gc(csv_file, swp_header)
    
    # Define filename convention
    sw = str(sw.replace('.packet.net',''))
    sw_file = f'{sw_header}.{sw}'

    table_headers = ["Rack Position", "Switch", "Switch Port", "Remarks"]
    mapped_data = []
    table_sorted = []
    with open(f'{sw_file}.txt', 'r') as sw_name:    
        contents = sw_name.read()
        rk_eth_dict = literal_eval(contents)
        search_stat = 'down'
    
        for rk, eth in rk_eth_dict.items():
            for port in eth:
                eth_port_stat = eth[port]
                if eth_port_stat != search_stat:
                    for i in range(len(swp_list)):
                        if f'{port}' in swp_list[i]:
                            mapped_data.append([rk, rk, sw, port, Fore.GREEN + '✔ [up]' + Style.RESET_ALL])
                else:
                    for i in range(len(swp_list)):
                        if f'{port}' in swp_list[i]:
                            mapped_data.append([
                                rk,
                                Fore.LIGHTYELLOW_EX + rk + Style.RESET_ALL,
                                Fore.LIGHTYELLOW_EX + sw + Style.RESET_ALL,
                                Fore.LIGHTYELLOW_EX + port + Style.RESET_ALL,                            
                                Fore.RED + '✘ [down]' + Style.RESET_ALL])
    for row in sort_table(mapped_data, 0):
        table_sorted.append(row[1:])

    print(tabulate(table_sorted, table_headers, tablefmt="pretty"))
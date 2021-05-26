#!/usr/bin/env python3

# Standard library imports
import requests, warnings

# Local application imports
from .read_csv import get_csv_to_dict as gcsv_dict

# convert list to dictionary
def convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def is_vendor(csv_file):

    # Getting the rack postion definition
    file_csv_to_dict = gcsv_dict(csv_file)

    user_pass_dict = {}
    for user_pass in file_csv_to_dict:
        bmc_user = "bmc_username"
        bmc_pass = "bmc_password"
        rack = { user_pass[bmc_user]: user_pass[bmc_pass]}
        user_pass_dict.update(rack)
    return user_pass_dict

def sort_table(table, col):
    return sorted(table, key=lambda k: int(k[col]))
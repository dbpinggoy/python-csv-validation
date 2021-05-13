#!/usr/bin/env python3

# Standard library imports
import os, argparse


# Local application imports
# from platopscsv.read_csv import get_columns as gc
from platopscsv.filter_esrsw_info import filter_ethsw_and_ethswp as filter_esrsw
from platopscsv.filter_bmcsw_info import filter_bmcsw_and_bmcswp as filter_bmcsw


parser = argparse.ArgumentParser(description='Python script to validate the CSV enrollment data')
parser.add_argument('-f', help='CSV filename', required=True)
parser.add_argument('-v', help='Server vendor like dell, smc', required=False)
# parser.add_argument('-s', help='Get specific FQDD property for all ethernet devices, pass in property name. To get the list of property names, first execute \"-e yy\" to get detailed information which will return the property values. Make sure to pass in the exact string as this value is case sensitive. Note: Multiple properties can be passed in by using a comma separator', required=False)

args = vars(parser.parse_args())

if args["f"]:
    csv_filename=args["f"]
if args["v"]:
    vendor = args["v"]
else:
    print("No vendor provided")


if __name__ == "__main__":
    print("[* Welcome to CSV Validation *]") 
    print("[*] Press CTRL-C to QUIT")
    # Change it to required value(in sec) 
    # stitle = get_arguments()
    try:
        # Delete any txt files if exists
        dir_name = os.getcwd()
        txt_files = os.listdir(dir_name)
        print(f'Removing txt files...')
        for txt in txt_files:
            if txt.endswith(".txt"):
                os.remove(os.path.join(dir_name, txt))
        filter_esrsw(csv_filename)
        filter_bmcsw(csv_filename, vendor)
        
    except KeyboardInterrupt: 
        print("\n[+] Quitting Program...")
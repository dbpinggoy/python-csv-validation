#!/usr/bin/env python3

# Standard library imports
import requests, warnings

# convert list to dictionary
def convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


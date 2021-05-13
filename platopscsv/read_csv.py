#!/usr/bin/env python3
import csv

def get_header(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        header_row = next(reader)
    return header_row

def get_columns(csv_file, column):
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        column_values=[]
        for lines in csv_reader:
            column_value = lines[column]
            column_values.append(column_value)
        return column_values

def get_single_column(csv_file, column):
    with open(csv_file, "r") as file:
        read_values = csv.DictReader(file)
        for row in read_values:
            print(row[column])

def get_csv_to_dict(csv_file):
    with open(csv_file, 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)
        records = []
        for row in rows:
            record = dict(zip(headers, row))
            records.append(record)
    return records
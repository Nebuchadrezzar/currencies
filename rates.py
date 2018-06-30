#!/usr/bin/env python3
import os
import sys
import urllib.request
import json
import csv
import re

if "-h" in str(sys.argv):
    print(
        """
    Pull currency rates from fixer.io, print rates and create a csv file of them.\n\
    -h, --help, this help\n\
    -s suppresses writing a csv file\n\
    -b base currency code to look up, default is EUR\n
    """
    )
    sys.exit(0)

# FIxer.io REST API as source
# define url parts
with open('APIkey.ini', 'r') as f:
    key = f.read().strip()

root = "http://data.fixer.io/api/latest"
APIKey = f"?access_key={key}&base="

# read base from argv or default
if "-b" in str(sys.argv):
    m = re.search(r'[A-Z]{3}', str(sys.argv))
    base = m.group(0)
else:
    base = "EUR"

# get the rates
url = root + APIKey + base

with urllib.request.urlopen(url) as document:
    feed = json.loads(document.read().decode("utf-8"))

# double dictionary with the base and date in top dict
date = feed['date']
from_curr = feed['base']
daily_rates = feed['rates']

# unpack the rates into a dict starting with date and base
rates = dict((cur, rate) for cur, rate in daily_rates.items())

# print a csv
for tocur, rate in rates.items():
    print(f'"{from_curr}","{tocur}",{rate}')

# check if the file exists, and if it does append to it
if os.path.exists('rates.csv'):
    entry = []
    with open('rates.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            entry.append(row[0])
    if base in entry and "-s" not in str(sys.argv):
        print(f'{base} rates already exist in this csv file')
        sys.exit(0)
    else:
        append_write = 'a'
else:
    append_write = 'w'

if "-s" not in str(sys.argv):
    with open('rates.csv', append_write) as csvfile:
        fieldnames = ['fromCurrency', 'toCurrency', 'rate', 'create timestamp',
                      'modified timestamp', 'createById', 'modifiedById',
                      ]
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for toCurr, rate in rates.items():
            writer.writerow({
                'fromCurrency': from_curr,
                'toCurrency': toCurr,
                'rate': rate,
                'create timestamp': (date + '00:00:00:000000'),
                'modified timestamp': (date + '00:00:00:000000'),
                'createById': 'fixer.io',
                'modifiedById': 'fix.io'
            })

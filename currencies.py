#!/usr/bin/env python3
import sys
import urllib.request
import json
import csv
import re
from datetime import datetime
import signal
import argparse


def signal_handler(signal, frame):
    print('\n')
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(
        description="""Create a csv of currencies from www.coinbase.com
                        Use .import "| tail - n + 2 currencies.csv"
                        onboardingclient_currencytypes to import in sqllite."""
    )
    parser.add_argument("-o", "--output",
                        action='store', nargs='?',
                        type=argparse.FileType('w'),
                        default='currencies.csv',
                        help='Path and Name of a file to direct output.'
                        )
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Print to stdout."
                        )
    args = parser.parse_args()

    currencies = get_currencies()
    currencies = scrub_currencies(currencies)

    if args.verbose:
        for row in currencies.items():
            for element in row:
                print(''.join(str(element)), end=' ')
            print('')

    # print("Creating file: ", args.output)
    with args.output as csvfile:
        fieldnames = ['id', 'currency code', 'currency name',
                      'create timestamp', 'modified timestamp',
                      'createById', 'modifiedById'
                      ]
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        # writer = csv.writer(csvfile, quotechar='|')
        writer.writeheader()
        id = 0
        for code, name in currencies.items():
            id += 1
            writer.writerow({
                'id': id,
                'currency code': code,
                'currency name': name,
                'modified timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                'create timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                'createById': 'coinbase',
                'modifiedById': 'coinbase'
            })


def get_currencies():
    query_currencies = "http://www.coinbase.com/api/v1/currencies/"
    with urllib.request.urlopen(query_currencies) as document:
        # print(document.info().items())
        currencies = json.loads(document.read().decode("utf-8"))
        return currencies


def scrub_currencies(currencies):
    currencies = dict((key, re.sub(' \(.*\)', '', value))
                      for value, key in currencies)
    # print(currencies)
    return currencies


if __name__ == '__main__':
    main()

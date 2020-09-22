"""
TaxHub Report Generator
Create a report for orders and refunds from a specified period,
the data of which is drawn from Plentymarkets.

Copyright (C) 2020  Sebastian Fricke, Panasiam

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import configparser
import os
import sys

import plenty_api

import plenty_taxhub_generator.packages.taxhub as taxhub
import plenty_taxhub_generator.packages.utils as utils

PROG_NAME = 'plenty_taxhub_generator'
USER = os.getlogin()
if sys.platform == 'linux':
    CONFIG_PATH = os.path.join(
        '/', 'home', str(f'{USER}'), '.' + PROG_NAME + '_config.ini'
    )
elif sys.platform == 'win32':
    CONFIG_PATH = os.path.join(
        'C:\\', 'Users', str(f'{USER}'), '.' + PROG_NAME + '_config.ini'
    )


def setup_argparser():
    p = argparse.ArgumentParser(prog=PROG_NAME)
    p.add_argument(
        '--from',
        '-f',
        '--start',
        required=True,
        help='Start date for the date range',
        dest='start_date',
    )
    p.add_argument(
        '--to',
        '-t',
        '--end',
        required=True,
        help='End date for the date range',
        dest='end_date',
    )
    p.add_argument(
        '--out',
        '-o',
        '--dest',
        required=False,
        help='Destination path for the output file',
        dest='output_path',
    )
    p.add_argument(
        '--mappings',
        '-m',
        '--map',
        required=False,
        help='Show the current mappings within the config file',
        dest='mappings',
        action='store_true',
    )
    p.add_argument(
        '--change_url',
        '-c',
        '--url',
        required=False,
        help='Change the base URL for the API request endpoint',
        dest='url',
    )
    args = p.parse_args()
    if args.url:
        if not utils.check_url(url=args.url):
            print(
                'ERROR: invalid URL [{0}] used for the change URL request.'.format(
                    args.url
                )
            )
            sys.exit(1)

    if args.output_path:
        if not os.path.exists(args.output_path):
            print(
                'ERROR: invalid directory path [{0}] used as output path'.format(
                    args.output_path
                )
            )
            sys.exit(1)
    return args


def gather_data_from_config(config):
    """
    Check the config for required fields and gather the URL, VAT ids,
    country ids and optional fixed values.

    Parameter:
        [configparser Object]

    Return:
        [Dict]
    """

    if 'General' not in config.sections():
        print('ERROR: config requires a General section with the base_url.')
        return None
    if not config.has_option(section='General', option='base_url'):
        print('ERROR: base_url required for the PlentyMarkets API request.')
        return None
    if 'Mappings' not in config.sections():
        print('ERROR: config requires a Mappings section')
        return None
    if not config.has_option(section='Mappings', option='country_id'):
        print('ERROR: Country ids required to map the required abbreviation')
        return None

    data = {
        'url': config['General']['base_url'],
        'countries': {},
        'referrer': {},
        'fixed_values': {},
    }
    data['countries'] = utils.country_id_mapping(config=config)
    data['referrer'] = utils.get_referrer_id_list(config=config)

    if 'fixed_values' in config.sections():
        for key in config['fixed_values']:
            data['fixed_values'][key] = config['fixed_values'][key]

    return data


def add_vat_data_to_mappings(mapping: dict, vat_data: dict) -> dict:
    """
    Add the Tax ID and the VAT configuration IDs to the existing
    country mappings.
    """
    for key in mapping['countries'].keys():
        country_id = mapping['countries'][key]['country_id']
        if country_id in vat_data.keys():
            mapping['countries'][key]['vat_conf'] = vat_data[country_id]['config']
            mapping['countries'][key]['tax_id'] = vat_data[country_id]['TaxId']
        else:
            print(f'ERROR: no VAT data found, for {key}: {country_id}')

    return mapping


def show_mappings(data: dict) -> None:
    print(f"PlentyMarkets API base URL: {data['url']}\n-------")

    for country in data['countries'].keys():
        print(
            'Country: {0}\tID: {1}'.format(
                country, data['countries'][country]['country_id']
            )
        )
    print('-------')
    for referrer in data['referrer']:
        print(f'Referrer: {referrer}')
    print('-------')
    for key, value in data['fixed_values'].items():
        print(f'optional fixed value: {key} = {value}')
    sys.exit(0)


def cli():
    out_path = os.path.join(os.getcwd(), 'tax_hub_report.csv')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    mapping = gather_data_from_config(config=config)
    args = setup_argparser()
    all_orders = []

    if args.url:
        config['General']['base_url'] = args.url
        config.write(CONFIG_PATH)
    if args.mappings:
        show_mappings(data=mapping)
    if args.output_path:
        out_path = args.output_path

    plenty = plenty_api.PlentyApi(
        base_url=mapping['url'], data_format='json', use_keyring=True
    )
    vat_data = plenty.plenty_api_get_vat_id_mappings()
    mapping = add_vat_data_to_mappings(mapping=mapping, vat_data=vat_data)

    for country in mapping['countries']:
        for referrer in mapping['referrer']:
            print(f'Load... country [{country}] referrer [{referrer}]')
            orders = plenty.plenty_api_get_orders_by_date(
                start=args.start_date,
                end=args.end_date,
                date_type='Payment',
                additional=['documents', 'location'],
                refine={
                    'countryId': mapping['countries'][country]['country_id'],
                    'referrerId': referrer,
                    'orderType': '1,4',
                },
            )
            all_orders += orders

    filtered_data = taxhub.filter_data(data=all_orders, mapping=mapping)

    filtered_data.to_csv(out_path, index=False, header=True)
    print(f'Report written to [{out_path}]')

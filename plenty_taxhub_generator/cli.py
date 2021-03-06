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
from pkg_resources import get_distribution, DistributionNotFound
from loguru import logger

import plenty_api

import plenty_taxhub_generator.packages.taxhub as taxhub
import plenty_taxhub_generator.packages.utils as utils


PROG_NAME = 'plenty_taxhub_generator'
USER = os.getlogin()
if sys.platform == 'linux':
    BASE_PATH = os.path.join(
        '/', 'home', str(f'{USER}'), '.config', PROG_NAME
    )
elif sys.platform == 'win32':
    BASE_PATH = os.path.join(
        'C:\\', 'Users', str(f'{USER}'), '.config', PROG_NAME
    )
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

CONFIG_PATH = os.path.join(BASE_PATH, 'config.ini')


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
    p.add_argument(
        '--version',
        '-v',
        required=False,
        help='show the version of this app and some dependencies',
        dest='version',
        action='store_true'
    )
    args = p.parse_args()
    if args.url:
        if not utils.check_url(url=args.url):
            logger.error(f"Invalid URL [{args.url}] used for the change "
                         "URL request.")
            sys.exit(1)

    if args.output_path:
        if not os.path.exists(args.output_path):
            logger.error(f"Invalid directory path [{args.output_path}] used "
                         "as output path")
            sys.exit(1)
    if args.version:
        try:
            __version__ = get_distribution(PROG_NAME).version
        except DistributionNotFound:
            __version__ = '(local)'
        print(f"{PROG_NAME} [{__version__}]\n"
              f"plenty_api [{plenty_api.__version__}]")
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
        logger.error("The config requires a 'General' section with the "
                     "base_url.")
        return None
    if not config.has_option(section='General', option='base_url'):
        logger.error("'Base_url' required for the PlentyMarkets API request.")
        return None
    if 'Mappings' not in config.sections():
        logger.error("The config requires a 'Mappings' section")
        return None
    if not config.has_option(section='Mappings', option='country_id'):
        logger.error('Country ids required to map the required abbreviation')
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
            logger.error(f"No VAT data found, for {key}: {country_id}")

    return mapping


def show_mappings(data: dict) -> None:
    logger.info(f"PlentyMarkets API base URL: {data['url']}\n-------")

    for country in data['countries'].keys():
        logger.info(f"Country: {country}\tID: "
                    f"{data['countries'][country]['country_id']}")
    for referrer in data['referrer']:
        logger.info(f'Referrer: {referrer}')
    for key, value in data['fixed_values'].items():
        logger.info(f'optional fixed value: {key} = {value}')
    sys.exit(0)


def cli():
    out_path = os.path.join(os.getcwd(), 'tax_hub_report.csv')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    mapping = gather_data_from_config(config=config)
    if not mapping:
        logger.error(f"Configuration does not exist or not valid.")
        sys.exit(1)
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
        base_url=mapping['url'], data_format='json', use_keyring=True,
        debug=False
    )
    vat_data = plenty.plenty_api_get_vat_id_mappings()
    mapping = add_vat_data_to_mappings(mapping=mapping, vat_data=vat_data)

    for country in mapping['countries']:
        for referrer in mapping['referrer']:
            logger.info(f"Load... country [{country}] referrer [{referrer}]")
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
    logger.info(f"Report written to [{out_path}]")

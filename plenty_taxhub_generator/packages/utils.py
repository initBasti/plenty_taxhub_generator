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

import re

import dateutil.parser

VALID_COUNTRY_ABBREVIATIONS = [
    'AF', 'AL', 'DZ', 'AD', 'AO', 'AG', 'AR', 'AM', 'AU', 'AT', 'AZ',
    'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BT', 'BO', 'BA',
    'BW', 'BR', 'BN', 'BG', 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'CF',
    'TD', 'CL', 'CN', 'CO', 'KM', 'CG', 'CD', 'CR', 'CI', 'HR', 'CU',
    'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER',
    'EE', 'SZ', 'ET', 'FJ', 'FI', 'FR', 'GA', 'GM', 'GE', 'DE', 'GH',
    'GR', 'GD', 'GT', 'GN', 'GW', 'GY', 'HT', 'HN', 'HU', 'IS', 'IN',
    'ID', 'IR', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE',
    'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY',
    'LI', 'LT', 'LU', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MR',
    'MU', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MA', 'MZ', 'MM', 'NA',
    'NR', 'NP', 'NL', 'NZ', 'NI', 'NE', 'NG', 'MK', 'NO', 'OM', 'PK',
    'PW', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'QA', 'RO', 'RU',
    'RW', 'KN', 'LC', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC',
    'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'SS', 'ES', 'LK', 'SD',
    'SR', 'SE', 'CH', 'SY', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TO', 'TT',
    'TN', 'TR', 'TM', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UY', 'UZ',
    'VU', 'VE', 'VN', 'YE', 'ZM', 'ZW',
]


def transform_date(date: str) -> str:
    """
    Transform a date from:
        {YYYY}-{MM}-{DD}T{HH}:{MM}:{SS}+{UTC-OFFSET}
                       to:
        {DD}/{MM}/{YYYY}
    The PlentyMarkets API uses the W3C date format.
    The TaxHub Report uses the {DD}/{MM}/{YYYY} format.

    Parameter:
        date [String]
    """
    try:
        parsed_date = dateutil.parser.parse(date)
    except dateutil.parser._parser.ParserError:
        print(f'ERROR: Invalid date: {date}, cannot transform date format.')
        return ''
    if not parsed_date:
        return ''
    return parsed_date.strftime('%d/%m/%Y')


def check_url(url) -> bool:
    """
    Check if the provided URL is in exactly the correct format.

    Parameter:
        url [String]
    """
    if not re.match(r'https://.*.plentymarkets-cloud\d{2}.com', url):
        return False
    return True


def country_id_mapping(config) -> dict:
    """
    Parse the list of country code to PlentyMarkets country ID mappings,
    while checking for common errors.

    Parameter:
        config [ConfigParser object]
    """
    mapping = {}
    conf_value = config['Mappings']['country_id']
    if conf_value.find(',') <= 0 and len(conf_value) > 6:
        print("ERROR: invalid country IDs, incorrect separator use: ','.")
        return {}

    country_ids = conf_value.split(',')

    for country in country_ids:
        if country.find('=') <= 0:
            print("ERROR: invalid country ID separate key and value with '='.")
            return {}
        country = country.strip(' ')
        pair = country.split('=')
        if pair[0].upper() not in VALID_COUNTRY_ABBREVIATIONS:
            print(f'ERROR: invalid country code: {pair[0]}')
            return {}
        try:
            int(pair[1])  # test if it is a valid number
        except ValueError:
            print(f'ERROR: invalid country ID value: {pair[1]}')
            return {}
        mapping[pair[0].upper()] = {
            'country_id': str(pair[1]),
            'tax_id': '',
            'vat_conf': [],
        }

    return mapping


def get_referrer_id_list(config: object) -> list:
    """
    Parse a list of referrer IDs from PlentyMarkets to use as order source
    for the report.
    If the option ALL is supplied, no restriction is applied.

    Parameter:
        config [ConfigParser object]
    """
    referrer_list = []
    conf_value: str = config['Mappings']['referrer_id']

    if conf_value == 'ALL':
        return ['ALL']

    if conf_value.find(',') <= 0 and len(conf_value) > 6:
        print('ERROR: invalid referrer IDs, incorrect separator use: ','.')
        return []
    elif conf_value.find(',') <= 0 and len(conf_value) <= 6:
        try:
            float(conf_value)  # test if it is a valid number
        except ValueError:
            print(f'ERROR: invalid referrer ID: {conf_value} must be a number.')
            return []
        return [conf_value]

    referrer_ids = conf_value.split(',')

    for referrer in referrer_ids:
        try:
            float(referrer)
        except ValueError:
            print(f'ERROR: invalid referrer ID: {conf_value} must be a number.')

        referrer_list.append(referrer)

    return referrer_list

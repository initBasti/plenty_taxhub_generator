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

import pandas

import plenty_taxhub_generator.packages.utils as utils

ORDER_TYPE_MAP = {'1': 'SALE', '4': 'REFUND'}
tax_columns = [
    'Position-Nr.', 'KindOfBusiness', 'TransactionId', 'DocumentId',
    'ReportingPeriod', 'DepatureDate', 'ArrivalDate', 'DocumentDate',
    'VatZone', 'VatRate', 'VatAmount (in VatZoneCurrency)', 'SourceZone',
    'SourceZoneZip', 'SourceZoneVatId', 'SourceZoneVatRate',
    'SourceZoneCurrencyCode', 'SourceZoneGross', 'SourceZoneNet',
    'TargetZone', 'TargetZoneZip', 'TargetZoneVatId', 'TargetZoneVatRate',
    'TargetZoneCurrencyCode', 'TargetZoneGross', 'TargetZoneNet', 'MarketZone',
    'MarketZoneCurrencyCode', 'MarketZoneGross', 'MarketZoneNet', 'Item ID',
    'ItemName', 'ItemDescription', 'CommodityCode', 'ItemQuantity',
    'StockkeepingUnit', 'ItemSalesPrice', 'ItemPurchasePrice',
    'ItemCurrencyCode', 'ItemWeight', 'TransportCode', 'ItemManufacturer',
    'ItemManufacturerZone', 'MPN', 'Brand', 'GTIN12 GTIN13 GTIN 14 GTIN 8',
    'ASIN', 'ISBN', 'UPC', 'JAN', 'PostingDateInvoice',
    'TransactionPartner Company Name', 'TransactionPartner Form of Address',
    'TransactionPartner First Name', 'TransactionPartner Platzhalter 2',
    'TransactionPartner Family Name', 'TransactionPartner Placeholder 2',
    'TransactionPartner Private Tax-ID', 'TransactionPartner Street',
    'TransactionPartner House Number', 'TransactionPartner Additional Address',
    'TransactionPartner ZIP', 'TransactionPartner City',
    'TransactionPartner Region', 'TransactionPartner Country IsoCode',
    'BillingAddress Company Name', 'BillingAddress Form of Address',
    'BillingAddress First Name', 'BillingAddress Platzhalter 2',
    'BillingAddress Family Name', 'BillingAddress Placeholder 2',
    'BillingAddress Private Tax-ID', 'BillingAddress Street',
    'BillingAddress House Number', 'BillingAddress Additional Address',
    'BillingAddress ZIP', 'BillingAddress Region', 'BillingAddress City',
    'BillingAddress Country IsoCode', 'Incoterms', 'Placeholder2',
    'Placeholder3', 'Placeholder4', 'Placeholder5', 'Placeholder6',
    'Placeholder7', 'Placeholder8', 'Placeholder9', 'Placeholder10',
    'Placeholder11', 'Placeholder12', 'Placeholder13', 'Placeholder14',
    'Placeholder15', 'Placeholder16', 'Placeholder17', 'Placeholder18',
    'Placeholder19', 'Placeholder20',
]


def insert_empty_entries(target: list, num: int) -> None:
    for _ in range(num):
        target.append('')


def get_order_type(value: int) -> str:
    if str(value) in ORDER_TYPE_MAP:
        return ORDER_TYPE_MAP.get(str(value))
    return ''


def get_document_data(row: dict) -> dict:
    """
    Check if the order contains the expected document for it's type.
    (sales order = invoice, refund = credit-note)
    And pull the full number together with it's creation date.

    Parameter:
        row [dict]      -   full row from the API JSON response

    Return:
        [dict]          -   containing the number and creation date
    """
    document_data = {'id': '', 'date': ''}
    if not row['documents']:
        return document_data

    for document in row['documents']:
        if row['typeId'] == 1 and document['type'] == 'invoice':
            document_data['id'] = document['numberWithPrefix']
            new_date = utils.transform_date(date=document['createdAt'])
            document_data['date'] = new_date
        if row['typeId'] == 4 and document['type'] == 'credit_note':
            document_data['id'] = document['numberWithPrefix']
            new_date = utils.transform_date(date=document['createdAt'])
            document_data['date'] = new_date

    return document_data


def get_delivery_date(row: dict) -> str:
    """
    Only sales-orders can be delivered, therefore check the type and
    then search for ID of a delivery date [5].

    Parameter:
        row [dict]      -   full row from the API JSON response

    Return:
        [str]           -   Date in {DD}/{MM}/{YYYY} format.
    """
    if row['typeId'] != 1:
        return ''

    for date in row['dates']:
        if date['typeId'] == 5:
            return utils.transform_date(date=date['date'])
    return ''


def get_vat_zone(row: dict, mapping: dict) -> str:
    """
    Find the country for which the VAT is charged,
    this is the same as the recipient country.

    Parameter:
        row [dict]      -   full row from the API JSON response
        mapping [dict]  -   data from the configuration and plenty VAT data

    Return:
        [str]           -   Abbreviation of the country in upper case
                            letters
    """
    if not row or not mapping:
        return ''

    vat_config_id = str(row['amounts'][0]['vats'][0]['countryVatId'])

    for country in mapping['countries']:
        if vat_config_id in mapping['countries'][country]['vat_conf']:
            return country
    return ''


def get_total_item_quantity(row: dict) -> str:
    """
    Get the total sum of the quantities of each item within the order.

    Parameter:
        row [dict]      -   full row from the API JSON response

    Returns:
        [str]           -   Total sum
    """
    total = 0
    for item in row['orderItems']:
        total += item['quantity']

    return str(total)


def filter_data(data: list, mapping: dict) -> pandas.DataFrame:
    """
    Reduce the data structure from the PlentyMarkets API request
    to the elements required for the TaxHub report.

    Parameter:
        data [List]         -   API data in JSON format
        mapping [Dict]      -   Configuration data and VAT data

    Return:
        [DataFrame]         -   with the required columns from the
                                tax_columns list
    """
    id_set = set()
    frame_data = []
    no_delivery = []
    no_document = []
    position = 1
    for entry in data:
        frame_row = []
        # skip duplicate Order IDs
        if entry['id'] in id_set:
            continue
        id_set.add(entry['id'])
        document = {'id': '', 'date': ''}
        frame_row.append(str(position))
        order_type = get_order_type(value=entry['typeId'])
        if not order_type:
            continue  # skip any order besides sales orders and refunds
        frame_row.append(order_type)
        frame_row.append(str(entry['id']))
        document = get_document_data(row=entry)
        if not document['id']:
            no_document.append(entry['id'])
        frame_row.append(document['id'])
        insert_empty_entries(target=frame_row, num=1)
        d_date = get_delivery_date(row=entry)
        if not d_date and entry['typeId'] == 1:
            no_delivery.append(entry['id'])
        frame_row.append(d_date)

        insert_empty_entries(target=frame_row, num=1)
        frame_row.append(document['date'])
        country = get_vat_zone(row=entry, mapping=mapping)
        if not country:
            continue
        frame_row.append(country)

        frame_row.append(str(f"{entry['amounts'][0]['vats'][0]['vatRate']} %"))
        frame_row.append(str(entry['amounts'][0]['vatTotal']))
        frame_row.append(mapping['fixed_values']['source_zone'])
        insert_empty_entries(target=frame_row, num=6)
        frame_row.append(country)
        insert_empty_entries(target=frame_row, num=1)
        frame_row.append(mapping['countries'][country]['tax_id'])
        frame_row.append(str(f"{entry['amounts'][0]['vats'][0]['vatRate']} %"))
        insert_empty_entries(target=frame_row, num=4)
        frame_row.append(mapping['fixed_values']['market_zone_currency'])
        frame_row.append(str(entry['amounts'][0]['grossTotal']))
        frame_row.append(str(entry['amounts'][0]['netTotal']))
        insert_empty_entries(target=frame_row, num=4)
        qty = get_total_item_quantity(row=entry)
        if not qty:
            print(f"WARNING: no item quantity for {entry['id']}.")
        frame_row.append(qty)

        insert_empty_entries(target=frame_row, num=64)
        position += 1
        frame_data.append(frame_row)

    frame = pandas.DataFrame(frame_data, columns=tax_columns)
    if no_document:
        print(f'INFO: Missing documents for Order ID: {no_document}')
    if no_delivery:
        print(f'INFO: Missing delivery date for Order ID: {no_delivery}')

    return frame

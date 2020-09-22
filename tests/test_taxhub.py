import pandas
import pytest
from pandas.testing import assert_frame_equal

from plenty_taxhub_generator.packages.taxhub import (filter_data,
                                                     get_delivery_date,
                                                     get_document_data,
                                                     get_order_type,
                                                     get_vat_zone, tax_columns
                                                     )
from tests.test_api_data import (sample_date_data, sample_document_data,
                                 sample_orders_api, sample_vat_data
                                 )


@pytest.fixture
def sample_mapping_data() -> dict:
    mapping = {
        'url': 'https://test.plentymarkets-cloud01.com',
        'vat_id': {'DE': 'DE12345678910', 'AT': 'AT12345678910'},
        'countries': {
            'DE': {
                'country_id': '1',
                'vat_conf': ['54', '55'],
                'tax_id': 'DE12345678910',
            },
            'AT': {
                'country_id': '2',
                'vat_conf': ['34', '35'],
                'tax_id': 'AT12345678910',
            },
        },
        'fixed_values': {'source_zone': 'DE', 'market_zone_currency': 'EUR'},
    }
    return mapping


@pytest.fixture
def expected_filter_result() -> object:
    result = [
        [
            '1', 'SALE', '12345', 'R20200600', '', '13/08/2020', '',
            '13/08/2020', 'DE', '16 %', '2.92', 'DE', '', '', '', '',
            '', '', 'DE', '', 'DE12345678910', '16 %', '', '', '', '',
            'EUR', '21.15', '18.23', '', '', '', '', '2', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
        ],
        [
            '2', 'REFUND', '12346', 'G20200600', '', '', '', '14/08/2020',
            'AT', '20 %', '7.29', 'DE', '', '', '', '', '', '', 'AT', '',
            'AT12345678910', '20 %', '', '', '', '', 'EUR', '43.76',
            '36.47', '', '', '', '', '5', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', ''
        ],
    ]
    df = pandas.DataFrame(result, columns=tax_columns)
    return df


def test_filter_data(
    sample_orders_api: list,
    sample_mapping_data: dict,
    expected_filter_result: pandas.DataFrame,
) -> None:
    result = filter_data(data=sample_orders_api, mapping=sample_mapping_data)

    assert_frame_equal(expected_filter_result, result)


def test_get_order_type() -> None:
    value = [1, 4, 99]
    expected = ['SALE', 'REFUND', '']
    result = []

    for val in value:
        result.append(get_order_type(value=val))

    assert expected == result


def test_get_document_data(sample_document_data: list) -> None:
    expected = [
        {'id': 'SALE_INVOICE_ID1', 'date': '03/02/2020'},
        {'id': 'REFUND_CREDIT_NOTE_ID1', 'date': '05/02/2020'},
        {'id': '', 'date': ''},
    ]
    result = []

    for sample in sample_document_data:
        result.append(get_document_data(row=sample))

    assert expected == result


def test_get_delivery_date(sample_date_data: list) -> None:
    expected = ['13/08/2020', '', '']
    result = []

    for sample in sample_date_data:
        result.append(get_delivery_date(row=sample))

    assert expected == result


def test_get_vat_zone(sample_vat_data: list, sample_mapping_data: dict) -> None:
    expected = ['DE', 'DE', 'AT', '', '']
    result = []

    for sample in sample_vat_data:
        result.append(get_vat_zone(row=sample, mapping=sample_mapping_data))

    assert expected == result

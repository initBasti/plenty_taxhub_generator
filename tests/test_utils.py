import configparser

import pytest

from plenty_taxhub_generator.packages.utils import (check_url,
                                                    country_id_mapping,
                                                    get_referrer_id_list,
                                                    transform_date
                                                    )


def config_obj(country='', referrer='') -> object:
    config = configparser.ConfigParser()
    config.read_dict({
        'General': {'url': 'https://...'},
        'Mappings': {
            'country_id': country,
            'referrer_id': referrer,
        },
        'fixed_values': {'source_zone': 'DE'}
    })

    return config


@pytest.fixture
def sample_referrer() -> list:
    samples = [
        config_obj(referrer='ALL'),
        config_obj(referrer=''),
        config_obj(referrer='3'),
        config_obj(referrer='3,4'),
        config_obj(referrer='3,4,5.01'),
        config_obj(referrer='104,4,5.01,2'),
        config_obj(referrer='abc')
    ]
    return samples


@pytest.fixture
def sample_country_mappings() -> list:
    samples = [
        config_obj(country='DE=1'),
        config_obj(country='DE=1,FR=2,GB=3,IT=4,ES=5'),
        config_obj(country='XX=5'),
        config_obj(country='PL=6,CZ=7,YY=99'),
        config_obj(country='DE:1'),
        config_obj(country='DE=1,FR=2GB=3,IT=4'),
        config_obj(country='abc'),
        config_obj(country='')
    ]
    return samples


def test_check_url() -> None:
    sample = [
        'https://google.com',
        'https://company.plentymarkets-cloud01.com',
        'https://othercompany.plentymarkets-cloud05.com',
        'abc',
        ''
    ]
    expected = [False, True, True, False, False]
    result = []

    for url in sample:
        result.append(check_url(url=url))

    assert expected == result


def test_get_referrer_id_list(sample_referrer) -> None:
    expected = [
        ['ALL'],
        [],
        ['3'],
        ['3', '4'],
        ['3', '4', '5.01'],
        ['104', '4', '5.01', '2'],
        []
    ]
    result = []

    for sample in sample_referrer:
        result.append(get_referrer_id_list(config=sample))

    assert expected == result


def test_country_id_mapping(sample_country_mappings) -> None:
    expected = [
        {'DE': {'country_id': '1', 'tax_id': '', 'vat_conf': []}},
        {
            'DE': {'country_id': '1', 'tax_id': '', 'vat_conf': []},
            'FR': {'country_id': '2', 'tax_id': '', 'vat_conf': []},
            'GB': {'country_id': '3', 'tax_id': '', 'vat_conf': []},
            'IT': {'country_id': '4', 'tax_id': '', 'vat_conf': []},
            'ES': {'country_id': '5', 'tax_id': '', 'vat_conf': []}
        },
        {},
        {},
        {},
        {},
        {},
        {}
    ]
    result = []

    for sample in sample_country_mappings:
        result.append(country_id_mapping(config=sample))

    assert expected == result


def test_transform_date() -> None:
    sample = ['2020-02-01T15:30:00+02:00', '1999-12-09T12:00:00+03:00',
              '2020-05-05T23:00:30+02:00', 'abc', '']
    expected = ['01/02/2020', '09/12/1999', '05/05/2020', '', '']
    result = []

    for test_date in sample:
        result.append(transform_date(date=test_date))

    assert expected == result

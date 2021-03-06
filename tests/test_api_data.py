import pytest


@pytest.fixture
def sample_orders_api():
    sample_orders = [
        {
            'id': 12345,
            'referrerId': 1,
            'roundTotalsOnly': True,
            'numberOfDecimals': 4,
            'statusName': 'shipped',
            'plentyId': 54321,
            'typeId': 1,
            'lockStatus': 'reversibleLocked',
            'locationId': '3',
            'createdAt': '2020-08-12T17:24:07+02:00',
            'updatedAt': '2020-08-13T08:48:33+02:00',
            'statusId': 7,
            'ownerId': '11',
            'relations': [
                {
                    'orderId': 12345,
                    'referenceType': 'warehouse',
                    'referenceId': 104,
                    'relation': 'sender',
                },
                {
                    'orderId': 12345,
                    'referenceType': 'contact',
                    'referenceId': 20955,
                    'relation': 'receiver',
                },
            ],
            'properties': [],
            'dates': [
                {'orderId': 12345, 'typeId': 2, 'date': '2020-08-12T17:23:52+02:00'},
                {'orderId': 12345, 'typeId': 5, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12345, 'typeId': 7, 'date': '2020-08-14T00:00:00+02:00'},
                {'orderId': 12345, 'typeId': 4, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12345, 'typeId': 3, 'date': '2020-08-12T17:23:51+02:00'},
            ],
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12345,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 18.23,
                    'grossTotal': 21.15,
                    'vatTotal': 2.92,
                    'invoiceTotal': 21.15,
                    'paidAmount': 21.15,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 54,
                            'vatField': 0,
                            'vatRate': 16,
                            'value': 2.92,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 18.23,
                            'grossTotal': 21.15,
                        }
                    ],
                }
            ],
            'orderReferences': [],
            'orderItems': [
                {
                    'id': 50523,
                    'orderId': 12345,
                    'typeId': 1,
                    'referrerId': 1,
                    'itemVariationId': 2255,
                    'quantity': 1,
                    'orderItemName': '',
                    'attributeValues': '',
                    'shippingProfileId': 12,
                    'countryVatId': 54,
                    'vatField': 0,
                    'vatRate': 16,
                    'position': '0',
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:07+02:00',
                    'warehouseId': 104,
                    'orderProperties': [],
                    'properties': [],
                    'dates': [],
                    'amounts': [
                        {
                            'id': 51866,
                            'orderItemId': 50523,
                            'isSystemCurrency': True,
                            'currency': 'EUR',
                            'exchangeRate': 1,
                            'purchasePrice': 23.7,
                            'priceOriginalGross': 21.15,
                            'priceOriginalNet': 18.2328,
                            'priceGross': 21.15,
                            'priceNet': 18.2328,
                            'surcharge': 0,
                            'discount': 0,
                            'isPercentage': True,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                        }
                    ],
                    'references': [],
                },
                {
                    'id': 50524,
                    'orderId': 12345,
                    'typeId': 6,
                    'referrerId': 1,
                    'itemVariationId': 0,
                    'quantity': 1,
                    'orderItemName': 'ShippingCosts',
                    'attributeValues': None,
                    'shippingProfileId': 0,
                    'countryVatId': 54,
                    'vatField': 0,
                    'vatRate': 16,
                    'position': '0',
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:07+02:00',
                    'warehouseId': None,
                    'orderProperties': [],
                    'properties': [],
                    'dates': [],
                    'amounts': [
                        {
                            'id': 51867,
                            'orderItemId': 50524,
                            'isSystemCurrency': True,
                            'currency': 'EUR',
                            'exchangeRate': 1,
                            'purchasePrice': 0,
                            'priceOriginalGross': 0,
                            'priceOriginalNet': 0,
                            'priceGross': 0,
                            'priceNet': 0,
                            'surcharge': 0,
                            'discount': 0,
                            'isPercentage': True,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                        }
                    ],
                    'references': [],
                },
            ],
            'addressRelations': [],
            'documents': [
                {
                    'id': 8507,
                    'type': 'invoice',
                    'number': '600',
                    'numberWithPrefix': 'R20200600',
                    'directoryId': None,
                    'path': '',
                    'userId': '11',
                    'source': 'admin',
                    'createdAt': '2020-08-13T08:30:08+02:00',
                    'updatedAt': '2020-08-13T08:30:09+02:00',
                    'displayDate': '2020-08-13T08:30:08+02:00',
                    'pivot': {
                        'plenty_document_reference_value': '12345',
                        'plenty_document_reference_document_id': '8507',
                    },
                }
            ],
            'comments': [],
        },
        {
            'id': 12346,
            'referrerId': 2,
            'roundTotalsOnly': True,
            'numberOfDecimals': 4,
            'statusName': 'shipped',
            'plentyId': 54321,
            'typeId': 4,
            'lockStatus': 'reversibleLocked',
            'locationId': '3',
            'createdAt': '2020-08-11T17:24:07+02:00',
            'updatedAt': '2020-08-15T08:48:33+02:00',
            'statusId': 11,
            'ownerId': '11',
            'relations': [
                {
                    'orderId': 12346,
                    'referenceType': 'warehouse',
                    'referenceId': 104,
                    'relation': 'sender',
                },
                {
                    'orderId': 12346,
                    'referenceType': 'contact',
                    'referenceId': 20955,
                    'relation': 'receiver',
                },
            ],
            'properties': [],
            'dates': [
                {'orderId': 12346, 'typeId': 2, 'date': '2020-08-12T17:23:52+02:00'},
                {'orderId': 12346, 'typeId': 5, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12346, 'typeId': 7, 'date': '2020-08-14T00:00:00+02:00'},
                {'orderId': 12346, 'typeId': 4, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12346, 'typeId': 3, 'date': '2020-08-12T17:23:51+02:00'},
            ],
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12346,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 36.47,
                    'grossTotal': 43.76,
                    'vatTotal': 7.29,
                    'invoiceTotal': 43.76,
                    'paidAmount': 43.76,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 34,
                            'vatField': 0,
                            'vatRate': 20,
                            'value': 7.29,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 36.47,
                            'grossTotal': 43.76,
                        }
                    ],
                }
            ],
            'orderReferences': [],
            'orderItems': [
                {
                    'id': 50523,
                    'orderId': 12346,
                    'typeId': 1,
                    'referrerId': 1,
                    'itemVariationId': 2255,
                    'quantity': 1,
                    'orderItemName': '',
                    'attributeValues': '',
                    'shippingProfileId': 12,
                    'countryVatId': 34,
                    'vatField': 0,
                    'vatRate': 16,
                    'position': '0',
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:07+02:00',
                    'warehouseId': 104,
                    'orderProperties': [],
                    'properties': [],
                    'dates': [],
                    'amounts': [
                        {
                            'id': 51866,
                            'orderItemId': 50523,
                            'isSystemCurrency': True,
                            'currency': 'EUR',
                            'exchangeRate': 1,
                            'purchasePrice': 23.7,
                            'priceOriginalGross': 21.15,
                            'priceOriginalNet': 18.2328,
                            'priceGross': 21.15,
                            'priceNet': 18.2328,
                            'surcharge': 0,
                            'discount': 0,
                            'isPercentage': True,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                        }
                    ],
                    'references': [],
                },
                {
                    'id': 50524,
                    'orderId': 12346,
                    'typeId': 4,
                    'referrerId': 1,
                    'itemVariationId': 2255,
                    'quantity': 1,
                    'orderItemName': '',
                    'attributeValues': '',
                    'shippingProfileId': 12,
                    'countryVatId': 54,
                    'vatField': 0,
                    'vatRate': 16,
                    'position': '0',
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:07+02:00',
                    'warehouseId': 104,
                    'orderProperties': [],
                    'properties': [],
                    'dates': [],
                    'amounts': [
                        {
                            'id': 51866,
                            'orderItemId': 50523,
                            'isSystemCurrency': True,
                            'currency': 'EUR',
                            'exchangeRate': 1,
                            'purchasePrice': 23.7,
                            'priceOriginalGross': 21.15,
                            'priceOriginalNet': 18.2328,
                            'priceGross': 21.15,
                            'priceNet': 18.2328,
                            'surcharge': 0,
                            'discount': 0,
                            'isPercentage': True,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                        }
                    ],
                    'references': [],
                },
                {
                    'id': 50525,
                    'orderId': 12346,
                    'typeId': 4,
                    'referrerId': 1,
                    'itemVariationId': 0,
                    'quantity': 3,
                    'orderItemName': 'ShippingCosts',
                    'attributeValues': None,
                    'shippingProfileId': 0,
                    'countryVatId': 54,
                    'vatField': 0,
                    'vatRate': 16,
                    'position': '0',
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:07+02:00',
                    'warehouseId': None,
                    'orderProperties': [],
                    'properties': [],
                    'dates': [],
                    'amounts': [
                        {
                            'id': 51867,
                            'orderItemId': 50524,
                            'isSystemCurrency': True,
                            'currency': 'EUR',
                            'exchangeRate': 1,
                            'purchasePrice': 0,
                            'priceOriginalGross': 0,
                            'priceOriginalNet': 0,
                            'priceGross': 0,
                            'priceNet': 0,
                            'surcharge': 0,
                            'discount': 0,
                            'isPercentage': True,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                        }
                    ],
                    'references': [],
                },
            ],
            'addressRelations': [],
            'documents': [
                {
                    'id': 8507,
                    'type': 'credit_note',
                    'number': '600',
                    'numberWithPrefix': 'G20200600',
                    'directoryId': None,
                    'path': '',
                    'userId': '11',
                    'source': 'admin',
                    'createdAt': '2020-08-14T08:30:08+02:00',
                    'updatedAt': '2020-08-14T08:30:09+02:00',
                    'displayDate': '2020-08-14T08:30:08+02:00',
                    'pivot': {
                        'plenty_document_reference_value': '12346',
                        'plenty_document_reference_document_id': '8507',
                    },
                }
            ],
            'comments': [],
        },
    ]
    return sample_orders


@pytest.fixture
def sample_document_data():
    sample = [
        {  # normal sales order with invoice
            'id': 12346,
            'typeId': 1,
            'documents': [
                {
                    'type': 'invoice',
                    'number': '600',
                    'numberWithPrefix': 'SALE_INVOICE_ID1',
                    'createdAt': '2020-02-03T04:05:06+02:00',
                    'updatedAt': '2020-02-03T04:05:06+02:00',
                    'displayDate': '2020-02-03T04:05:06+02:00',
                }
            ],
        },
        {  # normal refund with credit note
            'id': 12347,
            'typeId': 4,
            'documents': [
                {
                    'id': 8507,
                    'type': 'credit_note',
                    'number': '600',
                    'numberWithPrefix': 'REFUND_CREDIT_NOTE_ID1',
                    'createdAt': '2020-02-05T04:05:06+02:00',
                    'updatedAt': '2020-02-05T04:05:06+02:00',
                    'displayDate': '2020-02-05T04:05:06+02:00',
                }
            ],
        },
        {'id': 12348, 'typeId': 1, 'documents': []},  # sales order without invoice
    ]
    return sample


@pytest.fixture
def sample_date_data():
    sample = [
        {  # normale sales order
            'id': 12346,
            'typeId': 1,
            'dates': [
                {'orderId': 12346, 'typeId': 2, 'date': '2020-08-12T17:23:52+02:00'},
                {'orderId': 12346, 'typeId': 5, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12346, 'typeId': 7, 'date': '2020-08-14T00:00:00+02:00'},
                {'orderId': 12346, 'typeId': 4, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12346, 'typeId': 3, 'date': '2020-08-12T17:23:51+02:00'},
            ],
        },
        {'id': 12347, 'typeId': 6, 'dates': []},  # refund
        {  # Missing delivery date
            'id': 12348,
            'typeId': 1,
            'dates': [
                {'orderId': 12346, 'typeId': 2, 'date': '2020-08-12T17:23:52+02:00'},
                {'orderId': 12346, 'typeId': 7, 'date': '2020-08-14T00:00:00+02:00'},
                {'orderId': 12346, 'typeId': 4, 'date': '2020-08-13T08:48:33+02:00'},
                {'orderId': 12346, 'typeId': 3, 'date': '2020-08-12T17:23:51+02:00'},
            ],
        },
    ]
    return sample


@pytest.fixture
def sample_vat_data():
    sample = [
        {
            'id': 12345,
            'typeId': 1,
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12345,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 18.23,
                    'grossTotal': 21.15,
                    'vatTotal': 2.92,
                    'invoiceTotal': 21.15,
                    'paidAmount': 21.15,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 54,
                            'vatField': 0,
                            'vatRate': 16,
                            'value': 2.92,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 18.23,
                            'grossTotal': 21.15,
                        }
                    ],
                }
            ],
        },
        {
            'id': 12346,
            'typeId': 1,
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12346,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 18.23,
                    'grossTotal': 21.15,
                    'vatTotal': 2.92,
                    'invoiceTotal': 21.15,
                    'paidAmount': 21.15,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 55,
                            'vatField': 0,
                            'vatRate': 16,
                            'value': 2.92,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 18.23,
                            'grossTotal': 21.15,
                        }
                    ],
                }
            ],
        },
        {
            'id': 12347,
            'typeId': 1,
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12347,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 18.23,
                    'grossTotal': 21.15,
                    'vatTotal': 2.92,
                    'invoiceTotal': 21.15,
                    'paidAmount': 21.15,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 34,
                            'vatField': 0,
                            'vatRate': 20,
                            'value': 2.92,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 18.23,
                            'grossTotal': 21.15,
                        }
                    ],
                }
            ],
        },
        {
            'id': 12348,
            'typeId': 1,
            'amounts': [
                {
                    'id': 28498,
                    'orderId': 12348,
                    'isSystemCurrency': True,
                    'isNet': False,
                    'currency': 'EUR',
                    'exchangeRate': 1,
                    'netTotal': 18.23,
                    'grossTotal': 21.15,
                    'vatTotal': 2.92,
                    'invoiceTotal': 21.15,
                    'paidAmount': 21.15,
                    'giftCardAmount': 0,
                    'createdAt': '2020-08-12T17:24:07+02:00',
                    'updatedAt': '2020-08-12T17:24:23+02:00',
                    'shippingCostsGross': 0,
                    'shippingCostsNet': 0,
                    'prepaidAmount': 0,
                    'vats': [
                        {
                            'id': 28936,
                            'orderAmountId': 28498,
                            'countryVatId': 99,
                            'vatField': 0,
                            'vatRate': 24,
                            'value': 2.92,
                            'createdAt': '2020-08-12T17:24:07+02:00',
                            'updatedAt': '2020-08-12T17:24:07+02:00',
                            'netTotal': 18.23,
                            'grossTotal': 21.15,
                        }
                    ],
                }
            ],
        },
        {},
    ]
    return sample

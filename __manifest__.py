# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payment Account',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
Allows to create account payment from payment transaction.
    """,
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'base',
        'account',
        'payment',
    ],
    'data': [
        'views/account_payment.xml',
        'views/payment_acquirer.xml',
        'views/payment_transaction.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}


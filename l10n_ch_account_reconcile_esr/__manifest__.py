# -*- coding: utf-8 -*-
# copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Switzerland - ESR account reconcile',
    'version': '10.0.1.0.0',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'website': 'http://www.camptocamp.com',
    'license': 'AGPL-3',
    'summary': 'Adds a second automatic reconciliation button,'
    ' which is based on the esr',
    'depends': [
        'account',
        'base_transaction_id',
    ],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/account_reconciliation.xml',
    ],
    'installable': True,
    'auto_install': False,
}

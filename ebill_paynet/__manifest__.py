# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Ebill Paynet',
    'summary': """
        Paynet platform bridge implementation""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp SA,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-switzerland',
    'depends': [
        'ebill_base',
    ],
    'external_dependencies': {
        'python': [
            'zeep',
        ],
    },
    'data': [
        'data/transmit.method.xml',
        'security/ir.model.access.csv',
        'views/ebill_payment_contract.xml',
        'views/paynet_service.xml',
    ],
    'demo': [
    ],
}

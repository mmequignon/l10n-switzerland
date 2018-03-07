# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Specific hr for Enfinfidu',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Hr',
    'depends': [
        'hr_contract',
        'resource',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Views
        'views/hr_contract.xml',
        'views/hr_employee.xml',
    ],
    'installable': True,
}

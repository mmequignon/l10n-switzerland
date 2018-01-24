# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Security for Enfinfidu',
    'summary': "Security management",
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'maintainer': 'Camptocamp',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'calendar',
        'hr',
        'hr_holidays',
        'hr_attendance',
    ],
    'website': 'www.camptocamp.com',
    'data': [
        'security/category.xml',
        'security/groups.xml',
        'security/rules.xml',
        'views/menu.xml',
    ],
    'installable': True,
}

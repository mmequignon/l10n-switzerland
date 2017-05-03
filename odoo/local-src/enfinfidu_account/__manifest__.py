# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Specific account for Enfinfidu',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Report',
    'depends': [
        'account',
        'l10n_multilang',
        'l10n_ch',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Data
        'data_1/account.account.template.csv',  # 1- Add transfer account
        'data_2/account.chart.template.csv',    # 2- Add chart template
        'data_3/account.account.template.csv',  # 3- Complete transfer account
        'data_4/account.account.template.csv',  # 4- Add template accounts
        'data_4/account.account.tag.csv',       # 4- Add account tags
        'data_4/account.tax.template-override.csv',# 4- Override l10n_ch tax template names
        'data_4/account.tax.template.csv',      # 4- Add account tax template
        'data_5/account.chart.template.csv',    # 5- Complete chart template
    ],
    'installable': True,
}

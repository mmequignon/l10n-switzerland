# -*- coding: utf-8 -*-
# Copyright 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Enfinfidu Report Customization',
    'version': '10.0.1.0.2',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Specific',
    'website': 'http://www.camptocamp.com',
    'images': [],
    'depends': [
        'report',
        'account',
        'l10n_ch_hr_payroll_report',
    ],
    'data': [
        # Reports
        'report/layout.xml',
        'report/invoice.xml',
        'report/payslip.xml',
        'views/company_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

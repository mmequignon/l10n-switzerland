# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Specific payroll for Enfinfidu',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Hr',
    'depends': [
        'hr_payroll',
        'l10n_ch_hr_payroll',
        'l10n_ch_hr_payroll_report',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Data
        'data/hr_contribution_register.xml',
        'data/hr_salary_rule_category.xml',
        'data/hr_salary_rule.xml',
        'data/hr_rule_input.xml',
        'data/hr_payroll_structure.xml',
    ],
    'installable': True,
}

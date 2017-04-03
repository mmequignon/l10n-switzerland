# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Specific project for Enfinfidu',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Project',
    'depends': [
        'account',
        'hr_expense',
        'project',
        'project_task_default_stage',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Views
        'views/account_invoice.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/res_company.xml',
    ],
    'installable': True,
}

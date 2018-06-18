# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from ..common import (generate_contribution_registers,
                      generate_salary_rule_categories,
                      generate_salary_rules,
                      generate_payroll_structures)


@anthem.log
def post(ctx):
    """ Post 10.14.0 """
    # Apply config for:
    # Nicole Kate 28
    # John - David Burdet 30
    # Amplify 31
    # SmartCo 32
    # Bati - bloc Sàrl. 33
    # Assymba Sarl . 29
    # We check that no salary rules are applied on a wrong company
    companies = ctx.env['res.company'].search([
        ('id', 'in', [28, 29, 30, 31, 32, 33])])
    generate_contribution_registers(ctx, companies)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

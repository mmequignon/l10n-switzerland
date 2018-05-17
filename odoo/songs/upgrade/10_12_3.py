# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from ..common import (clean_structure_new_version,
                      generate_contribution_registers,
                      generate_salary_rule_categories,
                      generate_salary_rules,
                      generate_payroll_structures)


@anthem.log
def main(ctx):
    """ Applying update 10.12.3 """
    clean_structure_new_version(ctx)

    # Apply config for this company only
    # Uni-Constructions Sarl   16
    # We verify that no salary rules are apply on a wrong company
    companies = ctx.env['res.company'].search([
        ('id', 'in', [16])])
    generate_contribution_registers(ctx, companies)
    # Remove category generator for animed (already done)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

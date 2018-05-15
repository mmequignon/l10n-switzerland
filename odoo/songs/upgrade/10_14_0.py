# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from ..common import (clean_structure_new_version,
                      generate_contribution_registers,
                      generate_salary_rule_categories,
                      generate_salary_rules,
                      generate_payroll_structures)


@anthem.log
def trick_with_res_id(ctx):
    old_tax_templates = ctx.env['account.tax.template'].search(
        [('name', 'like', 'DEPRECATED')]
    )
    new_tax_templates = ctx.env['account.tax.template'].search(
        [('name', 'not like', 'DEPRECATED')]
    )
    for new_tax_template in new_tax_templates:
        for old_tax_template in old_tax_templates:
            if new_tax_template.name in old_tax_template.name:
                model_data = ctx.env['ir.model.data'].search(
                    [('res_id', '=', old_tax_template.id),
                     ('model', '=', 'account.tax.template')]
                )
                if model_data:
                    model_data.res_id = new_tax_template.id


@anthem.log
def pre(ctx):
    """ Pre 10.14.0 """
    trick_with_res_id(ctx)


@anthem.log
def post(ctx):
    """ Post 10.14.0 """
    clean_structure_new_version(ctx)

    # Apply config for:
    # R-éal                    24
    # Aria snaps               23
    # The Social Partner Sàrl  21
    # We check that no salary rules are applied on a wrong company
    companies = ctx.env['res.company'].search([
        ('id', 'in', [24, 23, 21])])
    generate_contribution_registers(ctx, companies)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

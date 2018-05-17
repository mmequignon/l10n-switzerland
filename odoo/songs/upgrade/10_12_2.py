# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem
from ..common import (generate_contribution_registers,
                      generate_salary_rule_categories,
                      generate_salary_rules,
                      generate_payroll_structures)


@anthem.log
def pre_clean(ctx, companies):
    for comp in companies:
        ctx.env.cr.execute("""
        DELETE FROM hr_structure_salary_rule_rel where
        (rule_id in (select id from hr_salary_rule  where company_id = %s )
        and struct_id not in
         (select id from hr_payroll_structure where company_id = %s ))
         OR  (rule_id not in
         (select id from hr_salary_rule  where company_id = %s )
          and struct_id in
          (select id from hr_payroll_structure where company_id = %s ))
         """ % (comp, comp, comp, comp))


@anthem.log
def main(ctx):
    """ Applying update 10.12.2 """
    # Apply config for this company only
    # Animed, Valérie et Olivier  Grin 14
    # Association Gamer Event 18
    # Enfin! Consulting Sarl 1
    # Melioris SA 19
    # Melioris Einkaufsberatung AG  17
    # Uni-Architectes Sarl   15
    # We verify that no salary rules are apply on a wrong company
    pre_clean(ctx, [1, 18, 19, 17, 15])
    companies = ctx.env['res.company'].search([
        ('id', 'in', [1, 14, 18, 19, 17, 15])])
    print str(companies)
    res_companies = ctx.env['res.company'].search([
        ('id', 'in', [18, 19, 17, 15])])
    generate_contribution_registers(ctx, res_companies)
    # Remove category generator for animed (already done)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

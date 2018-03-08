# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
import re


@anthem.log
def set_default_salary_rule_computed_rate(ctx):
    """ Extract the percentage used to compute the amount of the salary rules.
        The variable containing the percentage can be anywhere in the provided
        python code for the computation and its name is among the following:
            * per
            * per_in_limit
            * per_off_limit
        If it cannot be found, the default value is 100"""
    rules = ctx.env['hr.salary.rule'].search([('amount_select', '=', 'code')])
    re_rate = re.compile(
        r'^(?:.*?;)?per(?:_(?:in|off)_limit)? = (.*?)(?: / 100)?;.*'
    )

    for rule in rules:
        rate = '100.0'
        rate_match = re_rate.match(rule.amount_python_compute)
        if rate_match:
            rate = rate_match.group(1)
        rule.write({'rate_python_compute': 'rate = %s' % rate})


@anthem.log
def update_salary_rule_i18n(ctx):
    """ Remove all translations for the salary rules records
        and recreate them with the ones loaded from *.po files """
    i18n_obj = ctx.env['ir.translation']
    i18n_rules = i18n_obj.search(
        [('name', '=', 'hr.salary.rule,name'),
         '|', ('module', '=', 'enfinfidu_payroll'),
         ('module', '=', 'l10n_ch_hr_payroll')]
    )
    i18n_obj.search([('name', '=', 'hr.salary.rule,name'),
                     ('module', '=', None)]).unlink()
    rules = ctx.env['hr.salary.rule'].search([])

    for rule in rules:
        for i18n_rule in i18n_rules.filtered(lambda r: r.src == rule.name):
            i18n_rule.copy({'res_id': rule.id, 'module': None})


@anthem.log
def main(ctx):
    """ Applying update 10.13.0 """
    set_default_salary_rule_computed_rate(ctx)
    update_salary_rule_i18n(ctx)

# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem


@anthem.log
def generate_contribution_registers(ctx, companies):
    registers = ctx.env['hr.contribution.register'].search([])
    for comp in companies:
        with ctx.log(u'Generate contribution registers for %s' % comp.name):
            for register in registers:
                register.copy({
                    'company_id': comp.id
                })


@anthem.log
def generate_salary_rule_categories(ctx, companies):
    categories = ctx.env['hr.salary.rule.category'].search([])
    cat_with_parent = categories.filtered(lambda c: c.parent_id)
    cat_without_parent = categories - cat_with_parent
    for comp in companies:
        with ctx.log(u'Generate salary rule categories for %s' % comp.name):
            category_dict = {}
            for cwop in cat_without_parent:
                category_dict[cwop.id] = cwop.copy({
                    'company_id': comp.id
                })

            for cwp in cat_with_parent:
                new_parent = category_dict.get(cwp.parent_id.id)
                cwp.copy({
                    'company_id': comp.id,
                    'parent_id': new_parent.id
                })


@anthem.log
def generate_salary_rules(ctx, companies):

    def create_salary_rule(rule, comp, parent=False):

        new_category = ctx.env['hr.salary.rule.category'].search([
            ('code', '=', rule.category_id.code),
            ('company_id', '=', comp.id)
        ])

        new_debit_account = False
        new_credit_account = False

        if rule.account_debit:
            new_debit_account = ctx.env['account.account'].search([
                ('code', '=', rule.account_debit.code),
                ('company_id', '=', comp.id)
            ])
        if rule.account_credit:
            new_credit_account = ctx.env['account.account'].search([
                ('code', '=', rule.account_credit.code),
                ('company_id', '=', comp.id)
            ])
        return rule.copy({
            'company_id': comp.id,
            'category_id': new_category.id,
            'account_debit': new_debit_account and new_debit_account.id,
            'account_credit': new_credit_account and new_credit_account.id,
            'parent_rule_id': parent and parent.id,
            'child_ids': False,
        })

    rules = ctx.env['hr.salary.rule'].search([])
    rules_with_parent = rules.filtered(lambda r: r.parent_rule_id)
    rules_without_parent = rules - rules_with_parent
    company_rules_dict = {}
    for comp in companies:
        with ctx.log(u'Generate salary rules for %s' % comp.name):
            rules_dict = {}
            for rule in rules_without_parent:
                rules_dict[rule.id] = create_salary_rule(rule, comp)

            for rule in rules_with_parent:
                new_parent = rules_dict.get(rule.parent_rule_id.id)
                rules_dict[rule.id] = create_salary_rule(rule, comp,
                                                         parent=new_parent)

            company_rules_dict[comp.id] = rules_dict

    return company_rules_dict


@anthem.log
def generate_payroll_structures(ctx, companies, company_rules_dict):

    def create_structure(structure, company, parent=False):

        new_structure = structure.copy({
            'company_id': company.id,
            'parent_id': parent and parent.id,
            'children_ids': False,
            'rule_ids': False,
        })
        # Overwrite of code as (copy) is automatically appended
        new_structure.code = structure.code
        return new_structure

    structures = ctx.env['hr.payroll.structure'].search([])
    struct_with_parent = structures.filtered(lambda s: s.parent_id)
    struct_without_parent = structures - struct_with_parent
    for comp in companies:
        with ctx.log(u'Generate payroll structures for %s' % comp.name):

            rules_dict = company_rules_dict.get(comp.id)
            structure_dict = {}

            for swop in struct_without_parent:
                structure_dict[swop.id] = create_structure(swop, comp)

            for swp in struct_with_parent:
                new_parent = structure_dict.get(swp.parent_id.id)
                structure_dict[swp.id] = create_structure(swp, comp,
                                                          parent=new_parent)

            # Add rule_ids m2m relation
            for struct in structures:
                new_struct = structure_dict.get(struct.id)
                old_rules = struct.rule_ids
                new_rules = ctx.env['hr.salary.rule']
                for old_rule in old_rules:
                    new_rules |= rules_dict.get(old_rule.id)

                new_struct.write({
                    'rule_ids': [(6, False, new_rules.ids)]
                })


@anthem.log
def main(ctx):
    """ Applying update 10.9.0 """
    companies = ctx.env['res.company'].search([])
    companies -= ctx.env.ref('base.main_company')

    generate_contribution_registers(ctx, companies)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

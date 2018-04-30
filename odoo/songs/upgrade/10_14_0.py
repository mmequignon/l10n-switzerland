# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


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
def generate_contribution_registers(ctx, companies):
    # We use id Strategypod Sàrl (ID:4), it seems to be well configured
    registers = ctx.env['hr.contribution.register'].search([
        ('company_id', '=', 4)])
    for comp in companies:
        with ctx.log(u'Generate contribution registers for %s' % comp.name):
            for register in registers:
                register.copy({
                    'company_id': comp.id
                })


@anthem.log
def generate_salary_rule_categories(ctx, companies):
    # We use id Strategypod Sàrl (ID:4), it seems to be well configured
    categories = ctx.env['hr.salary.rule.category'].search([
        ('company_id', '=', 4)])
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

    # Check if current_company has already taxes
    # We use id Strategypod Sàrl (ID:4), it seems to be well configured
    rules = ctx.env['hr.salary.rule'].search([('company_id', '=', 4)])
    rules_with_parent = rules.filtered(lambda r: r.parent_rule_id)
    rules_without_parent = rules - rules_with_parent
    company_rules_dict = {}
    for comp in companies:
        allready_rules = ctx.env['hr.salary.rule'].search([
            ('company_id', '=', comp.id)])

        if allready_rules:
            dat_dict = {}
            for rule in allready_rules:
                dat_dict[rule.id] = rule
            company_rules_dict[comp.id] = dat_dict
            continue
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

    # We use id Strategypod Sàrl (ID:4), it seems to be well configured
    structures = ctx.env['hr.payroll.structure'].search(
        [('company_id', '=', 4)])
    struct_with_parent = structures.filtered(lambda s: s.parent_id)
    struct_without_parent = structures - struct_with_parent
    for comp in companies:
        with ctx.log(u'Generate payroll structures for %s' % comp.name):

            structure_dict = {}

            for swop in struct_without_parent:
                structure_dict[swop.id] = create_structure(swop, comp)

            for swp in struct_with_parent:
                new_parent = structure_dict.get(swp.parent_id.id)
                structure_dict[swp.id] = create_structure(swp, comp,
                                                          parent=new_parent)

            # Add rule_ids m2m relation
            for struct in structure_dict.keys():
                new_struct = structure_dict.get(struct)
                current_template = ctx.env['hr.payroll.structure'].search(
                    [('company_id', '=', 4), ('code', '=', new_struct.code)])
                ids_list = []
                for template_rule in current_template.rule_ids:
                    current_rule = ctx.env['hr.salary.rule'].search(
                        [('company_id', '=', comp.id),
                         ('name', '=', template_rule.name),
                         ('sequence', '=', template_rule.sequence)],
                        limit=1)
                    if current_rule:
                        ids_list.append(current_rule.id)

                new_struct.write({
                    'rule_ids': [(6, False, ids_list)]
                })


@anthem.log
def clean_structure_new_version(ctx):

    contracts = ctx.env['hr.contract'].search([])
    for contract in contracts:
        if (
            contract.struct_id and
            contract.struct_id.company_id != contract.employee_id.company_id
        ):
            new_structure = ctx.env['hr.payroll.structure'].search([
                ('name', '=', contract.struct_id.name),
                ('company_id', '=', contract.employee_id.company_id.id),
            ], limit=1)
            if new_structure:
                contract.struct_id = new_structure.id
            else:
                ctx.log('ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    structures = ctx.env['hr.payroll.structure'].search(
        [('rule_ids', '!=', False)],
        order='id desc'
    )
    for structure in structures:
        # Search for duplicate with no rules
        # search if the record is already deleted or not
        present = ctx.env['hr.payroll.structure'].search([
            ('id', '=', structure.id),
        ])
        if not present:
            continue
        other_structures = ctx.env['hr.payroll.structure'].search([
            ('name', '=', structure.name),
            ('company_id', '=', structure.company_id.id),
            ('id', '!=', structure.id),
        ])
        contracts = ctx.env['hr.contract'].search([
            ('struct_id', 'in', other_structures.ids),
        ])
        if contracts:
            contracts.write({
                'struct_id': structure.id,
            })
        other_structures.unlink()


@anthem.log
def pre(ctx):
    """ Pre 10.14.0 """
    trick_with_res_id(ctx)


@anthem.log
def post(ctx):
    """ Post 10.14.0 """
    clean_structure_new_version(ctx)

    # Apply config for:
    # R-éal        24
    # Aria snaps   10
    # We check that no salary rules are applied on a wrong company
    companies = ctx.env['res.company'].search([
        ('id', 'in', [24, 23])])
    generate_contribution_registers(ctx, companies)
    generate_salary_rule_categories(ctx, companies)
    rules_dict = generate_salary_rules(ctx, companies)
    generate_payroll_structures(ctx, companies, rules_dict)

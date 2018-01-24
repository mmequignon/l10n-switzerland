# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import add_xmlid


@anthem.log
def fix_paper_format(ctx):
    """ Fix paper format in account_invoices report """

    paper = ctx.env.ref('report.paperformat_euro', False)

    # set paper format for account_invoices report
    report = ctx.env.ref('account.account_invoices')
    report.paperformat_id = paper

    # set paper format for companies
    companies = ctx.env['res.company'].search([('paperformat_id', '=', False)])
    if paper:
        companies.write({'paperformat_id': paper.id})


@anthem.log
def update_account_tags(ctx):
    """ Update account tags """
    tag_dict = {
        'Switzerland VAT Form: grid 302a': '__setup__.vat_tag_302_a',
        'Switzerland VAT Form: grid 302b': '__setup__.vat_tag_302_b',
        'Switzerland VAT Form: grid 342a': '__setup__.vat_tag_342_a',
        'Switzerland VAT Form: grid 342b': '__setup__.vat_tag_342_b',
    }

    tags = ctx.env['account.account.tag'].search([
        ('name', 'in', tag_dict.keys())
    ])
    for tag in tags:
        add_xmlid(ctx, tag, tag_dict[tag.name])


@anthem.log
def update_company_taxes(ctx):
    """ Update taxes for some companies """

    companies = ctx.env['res.company'].search([])

    for company in companies:

        chart_template = company.chart_template_id

        tax_templates = ctx.env['account.tax.template'].search([
            ('amount', 'in', [3.7, 7.7]),
            ('chart_template_id', '=', chart_template.id),
            ('name', 'not ilike', 'invest'),
        ])

        tax_templates_invest = ctx.env['account.tax.template'].search([
            ('amount', 'in', [3.7, 7.7]),
            ('chart_template_id', '=', chart_template.id),
            ('name', 'ilike', 'invest'),
        ])

        _create_tax(ctx, company, tax_templates)
        _create_tax(ctx, company, tax_templates_invest, is_invest=True)


@anthem.log
def _create_tax(ctx, company, tax_templates, is_invest=False):
        for tax_template in tax_templates:
            domain = [
                ('amount', '=', tax_template.amount),
                ('type_tax_use', '=', tax_template.type_tax_use),
                ('price_include', '=', tax_template.price_include),
                ('company_id', '=', company.id),
            ]

            if not is_invest:
                domain.append(('name', 'not ilike', 'invest'))
            else:
                domain.append(('name', 'ilike', 'invest'))

            tax = ctx.env['account.tax'].search(domain)

            if not tax:

                account = ctx.env['account.account'].search([
                    ('code', '=', tax_template.account_id.code),
                    ('company_id', '=', company.id),
                ])

                refund_account = ctx.env['account.account'].search([
                    ('code', '=', tax_template.refund_account_id.code),
                    ('company_id', '=', company.id),
                ])

                val = {
                    'name': tax_template.name,
                    'type_tax_use': tax_template.type_tax_use,
                    'amount_type': tax_template.amount_type,
                    'active': tax_template.active,
                    'company_id': company.id,
                    'sequence': tax_template.sequence,
                    'amount': tax_template.amount,
                    'description': tax_template.description,
                    'price_include': tax_template.price_include,
                    'include_base_amount': tax_template.include_base_amount,
                    'analytic': tax_template.analytic,
                    'tag_ids': [(6, 0, [t.id for t in tax_template.tag_ids])],
                    'tax_adjustment': tax_template.tax_adjustment,
                    'account_id': account.id,
                    'refund_account_id': refund_account.id,
                }
                ctx.env['account.tax'].create(val)


@anthem.log
def main_pre(ctx):
    """ Pre 10.12.0 """
    fix_paper_format(ctx)


@anthem.log
def main_post(ctx):
    """ Post 10.12.0 """
    update_account_tags(ctx)
    update_company_taxes(ctx)

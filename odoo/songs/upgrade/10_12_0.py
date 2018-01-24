# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


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
def main(ctx):
    """ Run setup """
    fix_paper_format(ctx)

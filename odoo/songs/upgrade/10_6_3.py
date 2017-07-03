# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def update_paper_format_company(ctx):
    companies = ctx.env['res.company'].search([])
    paper_format = ctx.env.ref('report.paperformat_euro')
    companies.write({'paperformat_id': paper_format.id})


@anthem.log
def add_payment_user_rights(ctx):
    users = ctx.env['res.users'].search([])
    group = ctx.env.ref('account_payment_order.group_account_payment')
    users.write({'groups_id': [(4, group.id)]})


@anthem.log
def main(ctx):
    """ Run setup """
    update_paper_format_company(ctx)
    add_payment_user_rights(ctx)

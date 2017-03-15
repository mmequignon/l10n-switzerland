# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.records import create_or_update, add_xmlid
from anthem.lyrics.loaders import load_csv_stream

from ..common import req


# BASE
@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/cust_000/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


# ACCOUNTING
@anthem.log
def load_account_journal(ctx):
    """ Load account journal """
    for journal in ctx.env['account.journal'].search([]):
        if not journal.get_metadata()[0]['xmlid']:
            add_xmlid(ctx, journal,
                      '__setup__.account_journal_%s' % journal.code)

    filepath = 'data/install/cust_000/account.journal.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'account.journal', csv_content)


@anthem.log
def activate_analytic(ctx):
    """ Activating analytic """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write({
        'implied_ids': [
            (4, ctx.env.ref('analytic.group_analytic_accounting').id)
        ]
    })


@anthem.log
def load_partner_banks(ctx):
    """ Load Banks """
    filepath = 'data/install/res.partner.bank.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'res.partner.bank', csv_content)


@anthem.log
def main(ctx):
    """ Run setup """
    import_users(ctx)

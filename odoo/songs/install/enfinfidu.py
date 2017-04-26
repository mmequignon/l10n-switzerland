# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.records import add_xmlid
from anthem.lyrics.loaders import load_csv_stream

from ..common import req


# BASE
@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/enfinfidu/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


# HR
@anthem.log
def import_salary_rule(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/enfinfidu/hr.salary.rule.csv')
    load_csv_stream(ctx, 'hr.salary.rule', content, delimiter=',')


# ACCOUNTING
@anthem.log
def load_account_journal(ctx):
    """ Load account journal """
    for journal in ctx.env['account.journal'].search([]):
        if not journal.get_metadata()[0]['xmlid']:
            add_xmlid(ctx, journal,
                      '__setup__.account_journal_%s' % journal.code)

    filepath = 'data/install/enfinfidu/account.journal.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'account.journal', csv_content)


@anthem.log
def load_partner_banks(ctx):
    """ Load Banks """
    filepath = 'data/install/enfinfidu/res.partner.bank.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'res.partner.bank', csv_content)


@anthem.log
def load_account_journal_fromcsv(ctx):
    """ Load account journal without add_xmlid """
    filepath = 'data/install/enfinfidu/account.journal.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'account.journal', csv_content)


@anthem.log
def load_account_payment_mode(ctx):
    """ Load account payment mode """
    filepath = 'data/install/enfinfidu/account.payment.mode.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'account.payment.mode', csv_content)


@anthem.log
def main(ctx):
    """ Run setup """
    import_users(ctx)
    import_salary_rule(ctx)
    load_account_journal_fromcsv(ctx)
    load_account_payment_mode(ctx)
    # TODO later
    # load_account_journal(ctx)
    # load_partner_banks(ctx)

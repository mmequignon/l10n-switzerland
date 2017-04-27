# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from base64 import b64encode
from pkg_resources import resource_string
from pkg_resources import resource_stream
from anthem.lyrics.records import create_or_update
from anthem.lyrics.loaders import load_csv_stream

import anthem
from ..common import req
from .accounting import configure_missing_chart_of_account


# BASE
@anthem.log
def setup_company(ctx):
    """ Setup company """

    create_or_update(
        ctx, 'res.company', '__setup__.rlbatiment',
        {
            'name': u'RL Batiment',
            'street': "Rue des Marronniers 16",
            'zip': "1800",
            'city': "Vevey",
            'country_id': ctx.env.ref('base.ch').id,
            'phone': "+41 79 742 77 60",
            'email': "info@rlbatiment.ch",
            'vat': "CHE-319.996.611",
            'currency_id': ctx.env.ref('base.CHF').id,
        })

    company = ctx.env.ref('__setup__.rlbatiment')

    # load logo on company
    logo_content = resource_string(
        req, 'data/images/customer_001.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo


# PROJECT
@anthem.log
def setup_project(ctx):
    """ Setup project """

    create_or_update(
        ctx, 'project.project', '__setup__.project_rlbatiment',
        {
            'name': u'RL Batiment',
        })
    create_or_update(
        ctx, 'res.company', '__setup__.rlbatiment',
        {
            'project_id': ctx.env.ref('__setup__.project_rlbatiment').id,
        })


# USERS
@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/customer_001/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


@anthem.log
def import_account_journals(ctx):
    """ Import account journals """
    fp = 'data/install/customer_001/account.journal.csv'
    content = resource_stream(req, fp)
    load_csv_stream(ctx, 'account.journal', content, delimiter=',')


@anthem.log
def import_payment_modes(ctx):
    """ Import payment modes """
    fp = 'data/install/customer_001/account.payment.mode.csv'
    content = resource_stream(req,)
    load_csv_stream(ctx, 'account.payment.mode', content, delimiter=',')


@anthem.log
def add_customer_company_to_main_company_users(ctx):
    """ add_customer_company_to_main_company_users """
    for user in ctx.env['res.users'].search([
        ('company_id', '=', ctx.env.ref('base.main_company').id),
    ]):
        user.write({
            'company_ids': [(4, ctx.env.ref('__setup__.rlbatiment').id)],
        })


# ACCOUNTING
@anthem.log
def configure_rl_batiment_chart_of_account(ctx):
    """Configure Missing COA for RL Batiment"""
    configure_missing_chart_of_account(
        ctx,
        coa_dict={
            '__setup__.rlbatiment': {
                'chart_template_id':
                    'enfinfidu_account.enfinfidu_chart_template',
                'template_transfer_account_id':
                    'enfinfidu_account.transfer_account_id',
                # 'sale_tax_id': 'l10n_ch.1_vat_80',
                # 'purchase_tax_id': 'l10n_ch.1_vat_80_purchase',
            },
        }
    )


@anthem.log
def main(ctx):
    """ Run setup """
    setup_company(ctx)
    setup_project(ctx)
    import_users(ctx)
    add_customer_company_to_main_company_users(ctx)
    configure_rl_batiment_chart_of_account(ctx)
    import_account_journals(ctx)
    import_payment_modes(ctx)

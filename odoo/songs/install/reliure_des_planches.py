# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from base64 import b64encode
from pkg_resources import resource_string
from pkg_resources import resource_stream
from anthem.lyrics.records import add_xmlid, create_or_update
from anthem.lyrics.loaders import load_csv_stream

import anthem
from ..common import req
from .accounting import configure_missing_chart_of_account


@anthem.log
def setup_company(ctx):
    create_or_update(
        ctx, 'res.company', '__setup__.reliure_des_planches',
        {
            'name': u'Reliure des Planches',
            'street': "Rue Industrielle 30",
            'vat': 'CHE-287.357.586 TVA',
            'zip': "1820",
            'city': u'Montreux',
            'country_id': ctx.env.ref('base.ch').id,
            'phone': "+41 21 963 67 09",
            'fax': "+41 21 963 67 09",
            'email': "cpidoux@reliuredesplanches.ch",
            'website': "www.reliuredesplanches.ch",
            'currency_id': ctx.env.ref('base.CHF').id,
        })

    company = ctx.env.ref('__setup__.reliure_des_planches')

    # load logo on company
    logo_content = resource_string(
        req, 'data/images/reliuredesplanches.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo

    partner = company.partner_id
    partner.mobile = "+41 79 103 03 72"
    if not partner.get_metadata()[0]['xmlid']:
        add_xmlid(ctx, partner, '__setup__.reliure_des_planches_partner')


@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/reliure_des_planches/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')

    user = ctx.env.ref('__setup__.res_user_reliure_des_planches_manager')
    user.password_crypt = (
        '$pbkdf2-sha512$19000$pNT6X8uZM.Y8Z2zN2VtrrQ$x/5qTQeSb2jl7EK6HmaKc'
        'xyKkQKJ9g2XDOEchaWdw.HEF2ay88mL.hGSdHcf8LZ3KsGBBEfi5y9DbXq0NedACA'
    )


@anthem.log
def import_account_journals(ctx):
    """ Import account journals """
    fp = 'data/install/reliure_des_planches/account.journal.csv'
    content = resource_stream(req, fp)
    load_csv_stream(ctx, 'account.journal', content, delimiter=',')


@anthem.log
def import_payment_modes(ctx):
    """ Import payment modes """
    fp = 'data/install/reliure_des_planches/account.payment.mode.csv'
    content = resource_stream(req, fp)
    load_csv_stream(ctx, 'account.payment.mode', content, delimiter=',')


@anthem.log
def import_partner_banks(ctx):
    """ Import payment modes """
    fp = 'data/install/reliure_des_planches/res.partner.bank.csv'
    content = resource_stream(req, fp)
    load_csv_stream(ctx, 'res.partner.bank', content, delimiter=',')


@anthem.log
def add_customer_company_to_main_company_users(ctx):
    """ add_customer_company_to_main_company_users """
    for user in ctx.env['res.users'].search([
        ('company_id', '=', ctx.env.ref('base.main_company').id),
    ]):
        user.write({
            'company_ids': [(4, ctx.env.ref('__setup__.reliure_des_planches').id)],
        })


@anthem.log
def configure_reliure_des_planches_chart_of_account(ctx):
    """Configure Missing COA for Reliure_Des_Planches Conseil"""
    configure_missing_chart_of_account(
        ctx,
        coa_dict={
            '__setup__.reliure_des_planches': {
                'chart_template_id':
                    'enfinfidu_account.enfinfidu_chart_template',
                'template_transfer_account_id':
                    'enfinfidu_account.transfer_account_id',
                'sale_tax_id': 'enfinfidu_account.tax_tmp_vat_80',
                'purchase_tax_id': 'enfinfidu_account.tax_tmp_vat_80_purchase',
            },
        }
    )


@anthem.log
def main(ctx):
    """ Run setup """
    setup_company(ctx)
    import_users(ctx)
    add_customer_company_to_main_company_users(ctx)
    configure_reliure_des_planches_chart_of_account(ctx)
    import_account_journals(ctx)
    import_payment_modes(ctx)
    import_partner_banks(ctx)

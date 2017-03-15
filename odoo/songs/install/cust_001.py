# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from base64 import b64encode
from pkg_resources import resource_string
from pkg_resources import resource_stream
from anthem.lyrics.records import create_or_update
from anthem.lyrics.loaders import load_csv_stream

import anthem
from ..common import req

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
        req, 'data/images/cust_001.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo


@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/cust_001/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')

# SALES


@anthem.log
def set_sales_settings(ctx):
    sale_config = ctx.env['sale.config.settings']
    # Sections in Sale lines
    sale_config.create({'group_sale_layout': 1}).execute()
    # UOM in Sale Lines
    sale_config.create({'group_uom': 1}).execute()


# ACCOUNTING


@anthem.log
def main(ctx):
    """ Run setup """
    setup_company(ctx)
    import_users(ctx)
    set_sales_settings(ctx)

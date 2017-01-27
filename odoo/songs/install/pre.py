# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from base64 import b64encode
from pkg_resources import resource_string, resource_stream

import anthem

from anthem.lyrics.loaders import load_csv_stream

from ..common import req


@anthem.log
def setup_company(ctx):
    """ Setup company """
    company = ctx.env.ref('base.main_company')
    company.name = 'NeoMedical'

    # load logo on company
    logo_content = resource_string(req, 'data/images/company_main_logo.jpg')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo

    content = resource_stream(req, 'data/install/res.company.csv')
    load_csv_stream(ctx, 'res.company', content, delimiter=',')


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR',):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })


@anthem.log
def admin_user_password(ctx):
    """ Change admin password """
    # password for the test server,
    # the password must be changed in production
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$RwjBWKtVqtU6Z0wpBWDsvQ$58z4KqZPcwa2a9hlP0tdV'
        'wjbXhyyRINZ5zEWCECs2WdWDZTIZzCH/vuy4rIaD/VuHdL47oAevx.MUcySy6GCDg'
    )


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_company(ctx)
    setup_language(ctx)
    admin_user_password(ctx)

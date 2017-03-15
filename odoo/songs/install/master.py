# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from base64 import b64encode
from pkg_resources import resource_string
from anthem.lyrics.records import create_or_update

import anthem
from ..common import req


@anthem.log
def setup_company(ctx):
    """ Setup company """
    company = ctx.env.ref('base.main_company')

    # load logo on company
    logo_content = resource_string(
        req, 'data/images/company_main_logo.jpg')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo

    values = {
        'name': u'Enfin! Consulting Sarl',
        'street': "Ch. de Montéclard 2A",
        'zip': "1066",
        'city': "Epalinges",
        'country_id': ctx.env.ref('base.ch').id,
        'phone': "+41 21 652 46 86",
        'fax': "+41 00 000 00 00",
        'email': "finance@enfinconsulting.ch",
        'website': "http://www.enfinfidu.ch",
        'vat': "CHE-260.151.945",
        'currency_id': ctx.env.ref('base.CHF').id,
    }
    company.write(values)


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR',):
        ctx.env['base.language.install'].create(
            {'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d.%m.%Y',
    })


@anthem.log
def activate_chf_currency(ctx):
    """ Activating CHF currency """
    chf_currency = ctx.env.ref('base.CHF')
    chf_currency.active = True


@anthem.log
def admin_user_password(ctx):
    """ Changing admin password """
    # TODO default admin password for the test server, must be changed
    # To get an encrypted password:
    # $ docker-compose run --rm odoo python -c \
    # "from passlib.context import CryptContext; \
    #  print CryptContext(['pbkdf2_sha512']).encrypt('my_password')"
    if os.environ.get('RUNNING_ENV') == 'dev':
        ctx.log_line('Not changing password for dev RUNNING_ENV')
        return
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$tVYq5dwbI0Tofc85RwiBcA$a1tNyzZ0hxW9kXKIyEwN1'
        'j84z5gIIi1PQmvtFHuxQ4rNA2RaXSGLjXnEifl6ZQZ/wiBJK6fZkeaGgF3DW9A2Bg'
    )


@anthem.log
def set_admin_lang(ctx):
    """ change default language """
    values = {
        'lang': "fr_FR"
    }

    create_or_update(ctx, 'res.partner', 'base.partner_root', values)


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_company(ctx)
    setup_language(ctx)
    activate_chf_currency(ctx)
    admin_user_password(ctx)
    set_admin_lang(ctx)

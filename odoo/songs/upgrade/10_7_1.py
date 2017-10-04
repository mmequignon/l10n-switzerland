# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def change_address_format(ctx):
    """Remove spaces after line breaks"""
    ctx.env.cr.execute("""update res_country set address_format = '%(street)s
%(street2)s
%(country_code)s-%(zip)s %(city)s' where code like 'CH';""")


@anthem.log
def update_company_language(ctx):
    """Update lang for company partners (used in invoice report)"""
    ctx.env.cr.execute("""UPDATE res_partner
        SET lang = 'fr_FR'
        WHERE id IN (1, 10, 243);""")


@anthem.log
def main(ctx):
    """ Run setup """
    change_address_format(ctx)
    update_company_language(ctx)

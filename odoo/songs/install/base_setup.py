# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def multi_company(ctx):
    """ Configure multicompany """
    general_settings = ctx.env['base.config.settings']
    vals = {'group_multi_company': True,
            'module_inter_company_rules': True}
    general_settings.create(vals).execute()


@anthem.log
def change_address_format(ctx):
    ctx.env.cr.execute("""
    update res_country set address_format = '%(street)s
    %(street2)s
    %(country_code)s-%(zip)s %(city)s' where code like 'CH';
    """)


@anthem.log
def activate_multicurrency(ctx):
    """ Activating multi-currency """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write({
        'implied_ids': [(4, ctx.env.ref('base.group_multi_currency').id)]
    })


@anthem.log
def main(ctx):
    """ Run scenario """
    multi_company(ctx)
    change_address_format(ctx)
    activate_multicurrency(ctx)
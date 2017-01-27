# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update, add_xmlid
from anthem.lyrics.loaders import load_csv_stream

from pkg_resources import resource_stream

from ..common import req


@anthem.log
def activate_multicurrency(ctx):
    """ Activating multi-currency """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write({
        'implied_ids': [(4, ctx.env.ref('base.group_multi_currency').id)]
    })


@anthem.log
def import_chart_of_accounts(ctx):
    """ Import Chart of Accounts """
    if not ctx.env.ref('__setup__.l10n_ch_coa_original_1100',
                       raise_if_not_found=False):
        # First install: the default l10n_ch chart has been
        # automatically installed, we'll clean the accounts
        # but the mandatory ones (used by taxes, properties, ...)

        # We don't have xmlids on the accounts because they have
        # been generated from the templates. We create a XMLID
        # from the account's code as defined in the default template.
        # So we'll have a consistent way to link the usual accounts
        for account in ctx.env['account.account'].search([]):
            add_xmlid(ctx, account,
                      '__setup__.l10n_ch_coa_original_%s' % account.code)

        # We want to keep those accounts because they are required
        # by the system (taxes and so on).
        # As we have added XMLIDs on them, we can safely change their
        # code (and other fields) in 'account.account.csv'.
        # All the other accounts will be removed and imported
        # from 'account.account.csv'
        required_account_codes = ('1100', '1170', '1171', '2000', '2200',
                                  '3200', '4200', '3806', '4906', '1090',
                                  '1001', '1021', '999999')
        required_accounts = ctx.env['account.account'].browse()
        for code in required_account_codes:
            required_accounts |= ctx.env.ref(
                '__setup__.l10n_ch_coa_original_%s' % code
            )

        other_accounts = ctx.env['account.account'].search(
            [('id', 'not in', required_accounts.ids)]
        )
        other_accounts.unlink()

    # Import the custom chart of account.
    # To modify a required account (1100, 2000, ...), XMLID in the
    # following form should be used in the file:
    # __setup__.l10n_ch_coa_original_xxxx
    with ctx.log('Import Accounts'):
        filepath = 'data/install/account.account.csv'
        csv_content = resource_stream(req, filepath)
        load_csv_stream(ctx, 'account.account', csv_content)


@anthem.log
def set_fiscalyear(ctx):
    values = {'date_start': '2017-01-01',
              'name': '2017',
              'date_end': '2017-12-31',
              'type_id': 1,
              'company_id': False,
              'active': True,
              }
    create_or_update(ctx, 'date.range', '__setup__.date_range_2017', values)


@anthem.log
def main(ctx):
    """ Configuring accounting """
    activate_multicurrency(ctx)
    import_chart_of_accounts(ctx)
    set_fiscalyear(ctx)

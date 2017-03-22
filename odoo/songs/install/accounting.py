# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def no_coa_instance_lock(ctx):
    """Prepare no accounting in holding"""
    values = {
        'name': "Dummy account to delete",
        'code': "DUMMY",
        'user_type_id': ctx.env.ref('account.data_account_type_equity').id,
        }
    create_or_update(ctx, 'account.account',
                     '__setup__.dummy_holding_account', values)
    company = ctx.env.ref('base.main_company')
    company.expects_chart_of_accounts = False


@anthem.log
def no_coa_instance_unlock(ctx):
    """ Remove dummy account on main company """
    ctx.env.ref('__setup__.dummy_holding_account').unlink()


@anthem.log
def configure_missing_chart_of_account(ctx):
    """Configure Missing COA for companies"""

    coa_dict = {
        'base.main_company': {
            'chart_template_id': 'specific_account.enfinfidu_chart_template',
            'template_transfer_account_id':
                'specific_account.transfer_account_id',
            # 'sale_tax_id': 'l10n_ch.1_vat_80',
            # 'purchase_tax_id': 'l10n_ch.1_vat_80_purchase',
        },
        '__setup__.rlbatiment': {
            'chart_template_id': 'specific_account.enfinfidu_chart_template',
            'template_transfer_account_id':
                'specific_account.transfer_account_id',
            # 'sale_tax_id': 'l10n_ch.1_vat_80',
            # 'purchase_tax_id': 'l10n_ch.1_vat_80_purchase',
        },
    }
    for company_xml_id, values in coa_dict.iteritems():
        company = ctx.env.ref(company_xml_id)
        coa = ctx.env.ref(values['chart_template_id'])
        template_transfer_account = ctx.env.ref(
            values['template_transfer_account_id']
        )
        # sale_tax = ctx.env.ref(values['sale_tax_id'])
        # purchase_tax = ctx.env.ref(values['purchase_tax_id'])
        if not company.chart_template_id:
            wizard = ctx.env['wizard.multi.charts.accounts'].create({
                'company_id': company.id,
                'chart_template_id': coa.id,
                'transfer_account_id': template_transfer_account.id,
                'code_digits': coa.code_digits,
                # 'sale_tax_id': sale_tax.id,
                # 'purchase_tax_id': purchase_tax.id,
                'complete_tax_set': coa.complete_tax_set,
                'currency_id': ctx.env.ref('base.CHF').id,
                'bank_account_code_prefix': coa.bank_account_code_prefix,
                'cash_account_code_prefix': coa.cash_account_code_prefix,
            })
            wizard.execute()


@anthem.log
def main(ctx):
    """ Configuring accounting """
    configure_missing_chart_of_account(ctx)

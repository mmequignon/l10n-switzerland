# Copyright 2012-2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class BaseInitInvoice(SavepointCase):

    def setUp(self):
        super().setUp()
        self.company = self.env.ref('base.main_company')
        self.partner = self.env.ref('base.res_partner_12')
        bank = self.env['res.bank'].create({
            'name': 'BCV',
            'bic': 'BIC23423',
            'clearing': '234234',
        })
        # define company bank account
        self.bank_journal = self.env['account.journal'].create({
            'company_id': self.company.id,
            'type': 'bank',
            'code': 'BNK42',
            'bank_id': bank.id,
            'bank_acc_number': '01-1234-1',
        })
        self.bank_acc = self.bank_journal.bank_account_id
        self.payment_mode = self.env['account.payment.mode'].create({
            'name': 'Inbound Credit transfer CH',
            'company_id': self.company.id,
            'bank_account_link': 'fixed',
            'fixed_journal_id': self.bank_journal.id,
            'payment_method_id':
            self.env.ref('account.account_payment_method_manual_in').id,
        })
        self.partner.customer_payment_mode_id = self.payment_mode.id
        fields_list = [
            'company_id',
            'user_id',
            'currency_id',
            'journal_id',
        ]
        self.inv_values = self.env['account.invoice'].default_get(fields_list)
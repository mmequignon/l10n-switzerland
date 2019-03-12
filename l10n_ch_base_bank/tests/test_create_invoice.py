# Copyright 2012-2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from .base_mixin import BaseInitInvoice
from odoo import exceptions


class TestCreateInvoice(BaseInitInvoice):

    def setUp(self):
        super().setUp()

    def test_emit_invoice_with_isr_reference(self):
        self.inv_values.update({
            'partner_id': self.partner.id,
            'type': 'out_invoice'
        })
        invoice = self.env['account.invoice'].new(self.inv_values)
        invoice._onchange_partner_id()
        self.assertEqual(invoice.partner_bank_id, self.bank_acc)
        self.assertNotEqual(invoice.reference_type, 'isr')

        invoice.reference = '132000000000000000000000014'

        invoice.onchange_reference()

        self.assertEqual(invoice.reference_type, 'isr')

    def test_emit_invoice_with_isr_reference_15_pos(self):
        self.inv_values.update({
            'partner_id': self.partner.id,
            'type': 'out_invoice'
        })
        invoice = self.env['account.invoice'].new(self.inv_values)
        invoice._onchange_partner_id()
        self.assertEqual(invoice.partner_bank_id, self.bank_acc)
        self.assertNotEqual(invoice.reference_type, 'isr')

        invoice.reference = '132000000000004'
        invoice.reference_type = 'isr'  # set manually ISR reference type

        # and save
        self.env['account.invoice'].create(
            invoice._convert_to_write(invoice._cache)
        )

    def test_emit_invoice_with_non_isr_reference(self):
        self.inv_values.update({
            'partner_id': self.partner.id,
            'type': 'out_invoice'
        })
        invoice = self.env['account.invoice'].new(self.inv_values)
        invoice._onchange_partner_id()
        self.assertEqual(invoice.partner_bank_id, self.bank_acc)
        self.assertNotEqual(invoice.reference_type, 'isr')

        invoice.reference = 'Not a ISR ref with 27 chars'

        invoice.onchange_reference()

        self.assertNotEqual(invoice.reference_type, 'isr')

    def test_emit_invoice_with_missing_isr_reference(self):
        self.inv_values.update({
            'partner_id': self.partner.id,
            'type': 'out_invoice',
            'account_id': 1,  # set dummy account to be replaced by onchange
        })
        invoice = self.env['account.invoice'].new(self.inv_values)

        with self.assertRaises(exceptions.ValidationError):
            invoice._onchange_partner_id()

            invoice.reference = False
            invoice.reference_type = 'isr'  # set manually ISR reference type

            # and save
            self.env['account.invoice'].create(
                invoice._convert_to_write(invoice._cache)
            )

    def test_emit_invoice_with_isr_reference_missing_ccp(self):
        self.inv_values.update({
            'partner_id': self.partner.id,
            'type': 'out_invoice',
            'account_id': 1,  # set dummy account to be replaced by onchange
        })
        invoice = self.env['account.invoice'].new(self.inv_values)
        self.bank_acc.acc_number = 'not a CCP'

        with self.assertRaises(exceptions.ValidationError):
            invoice._onchange_partner_id()

            invoice.reference = '132000000000000000000000014'

            invoice.onchange_reference()
            invoice.reference_type = 'isr'
            self.env['account.invoice'].create(
                invoice._convert_to_write(invoice._cache)
            )

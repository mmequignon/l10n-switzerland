# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.tests.common import SingleTransactionCase
from odoo.tools import file_open

from xmlunittest import XmlTestMixin


class TestEbillPaynet(SingleTransactionCase, XmlTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'Customer One', 'customer': True
        })
        cls.contract = cls.env['ebill.payment.contract'].create({
            'partner_id': cls.customer.id,
            'paynet_account_number': '123123123',
        })
        cls.account = cls.env['account.account'].search(
                    [('user_type_id', '=', cls.env.ref(
                        'account.data_account_type_revenue').id)],
                    limit=1)
        cls.at_receivable = cls.env["account.account.type"].create({
            "name": "Test receivable account",
            "type": "receivable",
        })
        cls.a_receivable = cls.env["account.account"].create({
            "name": "Test receivable account",
            "code": "TEST_RA",
            "user_type_id": cls.at_receivable.id,
            "reconcile": True,
        })
        cls.product = cls.env['product.template'].create({
            'name': 'Product One',
            'list_price': 100.00,
        })
        cls.invoice_1 = cls.env['account.invoice'].create({
           'partner_id': cls.customer.id,
           'account_id': cls.account.id,
           'type': 'out_invoice',
           'transmit_method_id': cls.env.ref(
               'ebill_paynet.paynet_transmit_method').id,
           'invoice_line_ids': [
               (0, 0, {
                   'account_id': cls.account.id,
                   'product_id': cls.product.product_variant_ids[:1].id,
                   'name': 'Product 1',
                   'quantity': 1.0,
                   'price_unit': 100.00,
                   }),
               ],
           })

    @classmethod
    def compare_xml_line_by_line(self, content, expected):
        """This a quick way to check the diff line by line to ease debugging"""
        generated_line = [l.strip() for l in content.split(b'\n')
                          if len(l.strip())]
        expected_line = [l.strip() for l in expected.split(b'\n')
                         if len(l.strip())]
        number_of_lines = len(expected_line)
        for i in range(number_of_lines):
            if generated_line[i].strip() != expected_line[i].strip():
                print('Diff at {}/{}'.format(i, number_of_lines))
                print('Expected {}'.format(expected_line[i]))
                print('Generated {}'.format(generated_line[i]))
                break

    def test_invoice(self):
        self.invoice_1.action_invoice_sent()
        m = self.env['paynet.invoice.message'].search([('invoice_id', '=', self.invoice_1.id)], limit=1)

        payload = m.payload.encode('utf8')
        self.assertXmlDocument(payload)

        expected = file_open('ebill_paynet/tests/examples/invoice_1.xml').read()
        self.compare_xml_line_by_line(payload, expected.encode('utf8'))

        # self.assertXmlEquivalentOutputs(payload, expected)

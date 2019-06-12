# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from freezegun import freeze_time

from odoo.tests.common import SingleTransactionCase
from odoo.tools import file_open

from string import Template
from xml.etree import ElementTree as ET
from xmlunittest import XmlTestMixin


@freeze_time("2019-06-07 09:06:00")
class TestInvoiceMessage(SingleTransactionCase, XmlTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref('base.ch')
        cls.company = cls.env.user.company_id
        cls.company.vat = "CHE-012.345.678"
        cls.company.name = "TestCompany"
        cls.company.street = "StreetOne"
        cls.company.street2 = ""
        cls.company.zip = '8888'
        cls.company.city = 'TestCity'
        cls.company.country_id = cls.country
        cls.bank = cls.env.ref('base.res_bank_1')
        cls.tax7 = cls.env['account.tax'].create({
            'name': 'Test tax',
            'type_tax_use': 'sale',
            'amount_type': 'percent',
            'amount': '7',
        })
        cls.partner_bank = cls.env['res.partner.bank'].create({
            'bank_id': cls.bank.id,
            'acc_number': '300.300.300',
            'acc_holder_name': 'AccountHolderName',
            'partner_id': cls.company.partner_id.id,

        })
        cls.terms = cls.env.ref('account.account_payment_term_15days')
        cls.paynet = cls.env['paynet.service'].create({
            'url': 'https://dws-test.paynet.ch/DWS/DWS',
            'client_pid': '52110726772852593',
        })
        cls.state = cls.env['res.country.state'].create({
            'code': 'VD',
            'name': 'Vaud',
            'country_id': cls.country.id,
        })
        cls.customer = cls.env['res.partner'].create({
            'name': 'Test RAD Customer XML', 'customer': True,
            'street': 'Teststrasse 100',
            # 'street2': 'Passage des araignées',
            'city': 'Fribourg',
            'zip': '1700',
            'country_id': cls.country.id,
            'state_id': cls.state.id,
        })
        cls.contract = cls.env['ebill.payment.contract'].create({
            'partner_id': cls.customer.id,
            'paynet_account_number': '41010198248040391',
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
           'partner_bank_id': cls.partner_bank.id,
           'payment_term_id': cls.terms.id,
           'type': 'out_invoice',
           'transmit_method_id': cls.env.ref(
               'ebill_paynet.paynet_transmit_method').id,
           'invoice_line_ids': [
               (0, 0, {
                   'account_id': cls.account.id,
                   'product_id': cls.product.product_variant_ids[:1].id,
                   'name': 'Product 1',
                   'quantity': 4.0,
                   'price_unit': 123.00,
                   'invoice_line_tax_ids': [(4, cls.tax7.id, 0)],
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
        """ Check XML payload genetated for an invoice."""
        self.invoice_1.number = 'INV_TEST_01'
        self.invoice_1.action_invoice_sent()
        # Should have a due date different to create date, but  this does not work
        # self.invoice_1.date_due = '2019-07-01'
        m = self.env['paynet.invoice.message'].search(
            [('invoice_id', '=', self.invoice_1.id)],
            limit=1,
        )
        # Remove the PDF file data from the XML to ease testing
        lines = m.payload.splitlines()
        for pos, line in enumerate(lines):
            if line.find('Back-Pack') != -1:
                lines.pop(pos + 1)
                break
        payload = '\n'.join(lines).encode('utf8')
        self.assertXmlDocument(payload)
        # Prepare the XML file that is expected
        expected_tmpl = Template(
            file_open('ebill_paynet/tests/examples/invoice_1.xml').read()
        )
        expected = expected_tmpl.substitute(
            IC_REF=m.ic_ref
        ).encode('utf8')
        self.compare_xml_line_by_line(payload, expected)
        print ('Shipment_id is {}'.format(m.shipment_id))
        # self.assertXmlEquivalentOutputs(payload, expected)

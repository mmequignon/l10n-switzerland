# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SingleTransactionCase

from odoo.addons.ebill_paynet.components.api import PayNetDWS

from .common import recorder


class TestEbillPaynet(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.paynet = cls.env['paynet.service'].create({
            'url': 'https://dws-test.paynet.ch/DWS/DWS',
        })
        cls.dws = PayNetDWS()
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

    @recorder.use_cassette
    def test_ping_service(self):
        """Check the ping service testing purpose only."""
        self.dws.service.ping()

    @recorder.use_cassette
    def test_takeShipment(self):
        ch = self.env.ref('base.ch')
        attachment = self.env['ir.attachment'].search(
            [['res_model', '=', 'res.country'], ['res_id', '=', ch.id]]
        )
        attachment = self.env.ref('mail.msg_discus4_attach1')
        shipment_id = self.paynet.take_shipment(attachment[0].datas)
        self.assertTrue(shipment_id.startswith('SC'))
        # The shipment is not found on the server ?
        # self.paynet.get_shipment_content(shipment_id)

    @recorder.use_cassette
    def test_getShipmentList(self):
        res = self.paynet.get_shipment_list()

    def test_invoice(self):
        self.invoice_1.action_invoice_sent()
    # def test_generate_xml(self):
    #     self.paynet_invoice_1.generate_payload()



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
        })
        cls.invoice_1 = cls.env['account.invoice'].create({
            'partner_id': cls.customer.id,
        })
        cls.paynet_invoice_1 = cls.env['paynet.invoice.message'].create({
            'invoice_id': cls.invoice_1.id
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

    # def test_generate_xml(self):
    #     self.paynet_invoice_1.generate_payload()

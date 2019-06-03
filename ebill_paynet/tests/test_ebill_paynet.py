# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SingleTransactionCase

from odoo.addons.ebill_paynet.components.api import PayNetDWS

from .common import recorder


class TestEbillPaynet(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # This is the api should probably be used from paynet.service only
        cls.paynet = cls.env['paynet.service'].create({
            'url': 'https://dws-test.paynet.ch/DWS/DWS',
        })
        cls.dws = PayNetDWS()
        cls.customer = cls.env['res.partner'].create({
            'name': 'Customer One', 'customer': True
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
        self.dws.client.service.ping()

    @recorder.use_cassette
    def test_getShipmentList_service(self):
        """Check get empty list of shipments."""
        self.dws.client.service.getShipmentList(
            Authorization=self.dws.authorization()
        )

    # def test_generate_xml(self):
    #     self.paynet_invoice_1.generate_payload()

    # @recorder.use_cassette
    def test_takeShipment(self):
        ch = self.env.ref('base.ch')
        attachment = self.env['ir.attachment'].search(
            [['res_model', '=', 'res.country'], ['res_id', '=', ch.id]]
        )
        attachment = self.env.ref('mail.msg_discus4_attach1')
        shipment_id = self.paynet.take_shipment(attachment[0].datas)
        print('Take Shipment {}'.format(shipment_id))
        self.paynet.get_shipment_content(shipment_id)

    def test_getShipmentList(self):
        res = self.paynet.get_shipment_list()

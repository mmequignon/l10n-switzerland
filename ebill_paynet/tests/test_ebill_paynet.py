# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SingleTransactionCase

from odoo.addons.ebill_paynet.components.api import PayNetDWS


class TestEbillPaynet(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def test_ping_service(self):
        self.dws.client.service.ping()

    def test_getShipmentList_service(self):
        self.dws.client.service.getShipmentList(Authorization=self.dws.authorization())

    # def test_generate_xml(self):
    #     self.paynet_invoice_1.generate_payload()

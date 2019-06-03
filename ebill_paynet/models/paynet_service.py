# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ebill_paynet.components.api import PayNetDWS


class PaynetService(models.Model):

    _name = "paynet.service"

    url = fields.Char()
    username = fields.Char()
    password = fields.Char()
    client_pid = fields.Char(string="Paynet ID", size=20)

    def take_shipment(self):
        """Send a shipment via DWS to the Paynet System
        """
        dws = PayNetDWS()
        dws.client.service.takeShipment()

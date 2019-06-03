# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ebill_paynet.components.api import PayNetDWS

from zeep.exceptions import Error, Fault


class PaynetService(models.Model):

    _name = "paynet.service"

    url = fields.Char()
    username = fields.Char()
    password = fields.Char()
    client_pid = fields.Char(string="Paynet ID", size=20)

    @api.multi
    def take_shipment(self, content):
        """Send a shipment via DWS to the Paynet System
        """
        self.ensure_one()
        dws = PayNetDWS()
        res = dws.client.service.takeShipment(
            Authorization=dws.authorization(),
            # ProcessingDate  : Preferred processing date,
            #                   if not provided, processed asap
            # ShipmentPriority: Value between 1 and 9 (default is 5)
            Content=content
        )
        # First test shows that res is a string with the shipment id
        return res

    @api.multi
    def get_shipment_list(self):
        self.ensure_one()
        dws = PayNetDWS()
        res = dws.client.service.getShipmentList(
            Authorization=dws.authorization(),
            # fromEntry     : Position number as of which shipments should be
            #                 retrieved (default is 1)
            # maxEntries    : Max number of shimpment listed (default is 100)
            # FromDate      :
            # ToDate        :
            # ShipmentStates
            # FromShipmentPriority:
            # ToShipmentPriority:
        )
        print('GET SHIPMENT LIST : {}'.format(res))
        return res

    @api.multi
    def get_shipment_content(self, shipment_id):
        self.ensure_one()
        dws = PayNetDWS()

        try:
            res = dws.client.service.getShipmentContent(
                Authorization=dws.authorization(),
                ShipmentID=shipment_id,
            )
        except Fault as e:
            dws.handle_fault(e)
            # raise
            return
        print('GET SHIPMENT CONTENT : {}'.format(res))
        self.confirm_shipment(shipment_id)
        return res

    @api.multi
    def confirm_shipment(self, shipment_id):
        self.ensure_one()
        dws = PayNetDWS()
        res = dws.client.service.confirmShipment(
            Authorization=dws.authorization(),
            ShipmentId=shipment_id,
        )
        return res

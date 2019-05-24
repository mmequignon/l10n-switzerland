# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaynetService(models.Model):

    _name = "paynet.service"

    url = fields.Char()
    username = fields.Char()
    password = fields.Char()
    client_pid = fields.Char(string="Paynet ID", size=20)

# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EbillPaymentContract(models.Model):

    _inherit = "ebill.payment.contract"

    paynet_account_number = fields.Char(string="Paynet account number", size=20)

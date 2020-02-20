# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    credit_control_line_ids = fields.One2many(
        comodel_name='credit.control.line',
        inverse_name='account_id',
        string='Credit Lines',
        readonly=True)

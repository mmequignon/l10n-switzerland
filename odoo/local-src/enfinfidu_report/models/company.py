# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    report_logo = fields.Binary(
        string='Report logo',
        help='Image to be used only in reports.',
    )
    report_partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Report Bank',
    )

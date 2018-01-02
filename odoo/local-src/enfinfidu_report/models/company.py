# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


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

    @api.model
    def create(self, values):
        # We need to have beautiful reports when we create a new company,
        # so, if the paperformat is undefined, we define it.
        if 'paperformat_id' not in values:
            paperformat = self.env.ref(
                'report.paperformat_euro',
                raise_if_not_found=False
            )
            if paperformat:
                values['paperformat_id'] = paperformat.id
        return super(ResCompany, self).create(values)

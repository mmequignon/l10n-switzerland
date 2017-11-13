# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def _get_default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one('res.company', 'Company',
                                 default=_get_default_company_id)

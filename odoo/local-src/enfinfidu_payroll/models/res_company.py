# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.addons.decimal_precision as dp
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    # AI(LAA)
    laanp_per = fields.Float(
        string="Percentage LAANP (%)",
        digits=dp.get_precision('Payroll Rate'),
        required=False)

    # AMAT(GE)
    amat_ge_per = fields.Float(
        string="Maternity insurance (AMAT GE)",
        digits=dp.get_precision('Payroll Rate'),
        required=False)

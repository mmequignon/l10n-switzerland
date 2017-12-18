# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.addons.decimal_precision as dp
from odoo import models, fields


class HrPayrollConfig(models.TransientModel):
    _inherit = 'hr.payroll.config'

    # AI(LAA)
    laanp_per = fields.Float(
        string="Percentage LAANP (%)",
        default=lambda self: self._get_default_configs('laanp_per'),
        digits=dp.get_precision('Payroll Rate'),
        required=False)

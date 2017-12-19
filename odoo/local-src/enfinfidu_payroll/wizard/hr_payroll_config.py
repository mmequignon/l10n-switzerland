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

    amat_ge_per = fields.Float(
        string="Maternity insurance (AMAT GE)",
        default=lambda self: self._get_default_configs('amat_ge_per'),
        digits=dp.get_precision('Payroll Rate'),
        required=False)

    def values_to_company(self):
        super(HrPayrollConfig, self).values_to_company()
        company_id = self.company_id
        company_id.write({'laanp_per': self.laanp_per,
                          'amat_ge_per': self.amat_ge_per})

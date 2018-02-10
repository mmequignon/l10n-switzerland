# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import UserError


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    @api.multi
    def unlink(self):
        # also added constrain to field `struct_id` in hr.contract
        contracts = self.env['hr.contract'].search(
            [('struct_id', 'in', self.ids)]
        )
        if contracts:
            raise UserError(
                _("One of the selected items used in Contract: \n%s\n"
                  "Please remove from Contract before deletion.") %
                '\n'.join(contracts.mapped('name')))
        else:
            return super(HrPayrollStructure, self).unlink()

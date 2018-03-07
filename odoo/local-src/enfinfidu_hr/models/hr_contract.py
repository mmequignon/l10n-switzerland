# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    employee_company_id = fields.Many2one(
        related='employee_id.company_id',
        string='Employee company',
        readonly=True,
        store=True,
    )

    working_hours_company_id = fields.Many2one(
        related='working_hours.company_id',
        string='Working hours company',
        readonly=True,
        store=True,
    )

    @api.multi
    @api.constrains('working_hours_company_id', 'employee_company_id')
    def _check_working_hours(self):
        for contract in self:
            working_hours = contract.working_hours
            if working_hours:
                employee_company = contract.employee_company_id
                working_hours_company = contract.working_hours_company_id
                if employee_company != working_hours_company:
                    raise ValidationError(
                        _(
                            'You cannot choose working schedule %s '
                            'for this contract, '
                            'because employee company is %s '
                            'and working schedule company is %s'
                        )
                        % (
                            working_hours.name,
                            employee_company.name,
                            working_hours_company.name,
                        )
                    )

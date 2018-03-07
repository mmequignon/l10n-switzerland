# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    calendar_company_id = fields.Many2one(
        related='calendar_id.company_id',
        string='Calendar company',
        readonly=True,
        store=True,
    )

    @api.multi
    @api.constrains('calendar_company_id', 'company_id')
    def _check_calendar(self):
        for employee in self:
            calendar_id = employee.calendar_id
            if calendar_id:
                employee_company = employee.company_id
                calendar_company = employee.calendar_company_id
                if employee_company != calendar_company:
                    raise ValidationError(
                        _(
                            'You cannot choose calendar %s '
                            'for this employee, '
                            'because employee company is %s '
                            'and calendar company is %s'
                        )
                        % (
                            calendar_id.name,
                            employee_company.name,
                            calendar_company.name,
                        )
                    )

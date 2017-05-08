# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


# bsfin-17
class Employee(models.Model):

    _inherit = "hr.employee"

    @api.multi
    def get_leaves_to_date(self, desired_date):

        #   if employee is absent on desired_date
        #   function calculates days from start to desired_date
        # how many days were allocated
        allocations = self.env['hr.holidays'].sudo().search([
            ('employee_id', 'in', self.ids),
            ('type', '=', 'add'),
            ('state', '=', 'validate')
        ])
        leaves_allocated = sum(allocations.mapped('number_of_days'))

        # how many days used before
        consumes = self.env['hr.holidays'].sudo().search([
            ('employee_id', 'in', self.ids),
            ('type', '=', 'remove'),
            ('date_to', '<=', desired_date),
            ('state', '=', 'validate')
        ])
        leaves_consumed_before = sum(consumes.mapped('number_of_days'))

        # days of current leave (if present)
        during_leave = self.env['hr.holidays'].sudo().search([
            ('employee_id', 'in', self.ids),
            ('type', '=', 'remove'),
            ('date_from', '<=', desired_date),
            ('date_to', '>=', desired_date),
            ('state', '=', 'validate')
        ])
        if during_leave:
            # during_leave must be single record or vacations overlaps
            date_tstamp = fields.Date.from_string(desired_date)
            df_tstamp = fields.Date.from_string(during_leave.date_from)
            leaves_consumed_before += (df_tstamp - date_tstamp).days
        # leaves with type remove stored with negative value
        return leaves_allocated+leaves_consumed_before

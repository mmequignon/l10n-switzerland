# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


# bsfin-17
class Employee(models.Model):

    _inherit = "hr.employee"

    @api.multi
    def get_leaves_to_date(self, datestring):

        # [BSFIN-72] desired date to 23:23:59
        des_date = fields.Date.from_string(datestring)
        desired_date = fields.Date.to_string(des_date) + ' 23:59:59'

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
            # during_leave must be single record or vacations overlapse
            df_tstamp = fields.Date.from_string(during_leave.date_from)
            while df_tstamp <= des_date:
                if self.work_scheduled_on_day(
                    df_tstamp,
                    during_leave.holiday_status_id.exclude_public_holidays,
                    during_leave.holiday_status_id.exclude_rest_days,
                ):
                    leaves_consumed_before -= 1
                df_tstamp += relativedelta(days=1)
        # leaves with type remove stored with negative value
        return leaves_allocated+leaves_consumed_before

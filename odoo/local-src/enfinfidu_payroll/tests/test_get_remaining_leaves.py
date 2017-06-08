# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools import mute_logger
from odoo.addons.hr_holidays.tests.common import TestHrHolidaysBase
from odoo import fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestGetRemainingLeaves(TestHrHolidaysBase):
    @mute_logger('odoo.addons.base.ir.ir_model', 'odoo.models')
    def test_00_get_remaining_leaves(self):
        """ Testing leave request flow """
        Holidays = self.env['hr.holidays']
        HolidaysStatus = self.env['hr.holidays.status']

        # HrManager creates some holiday statuses
        HolidayStatusManagerGroup = HolidaysStatus.sudo(self.user_hrmanager_id)
        HolidayStatusManagerGroup.create({
            'name': 'WithMeetingType',
            'limit': True,
            'categ_id': self.env['calendar.event.type'].sudo(
                self.user_hrmanager_id).create(
                {'name': 'NotLimitedMeetingType'}).id
        })
        self.holidays_status_2 = HolidayStatusManagerGroup.create({
            'name': 'Limited',
            'limit': False,
            'double_validation': True,
            'exclude_rest_days': False,
            'exclude_public_holidays': False
        })

        # Create leave allocation approve and validate
        test_alloc = Holidays.sudo(self.user_hrmanager_id).create({
            'name': 'Days for limited category',
            'employee_id': self.employee_emp_id,
            'holiday_status_id': self.holidays_status_2.id,
            'type': 'add',
            'number_of_days_temp': 20,
        })
        test_alloc.action_approve()
        test_alloc.action_validate()

        # Create leave request approve and validate
        leave_request = Holidays.sudo(self.user_hrmanager_id).create({
            'name': '6 day vacation',
            'employee_id': self.employee_emp_id,
            'holiday_status_id': self.holidays_status_2.id,
            'date_from': (datetime.today() + relativedelta(days=10)).strftime(
                '%Y-%m-%d %H:%M'),
            'date_to': (datetime.today() + relativedelta(days=16)),
            'number_of_days_temp': 6,
        })
        leave_request.action_approve()
        leave_request.action_validate()

        employee = self.env['hr.employee'].browse(self.employee_emp_id)

        # test before vacation allocated days 20
        remaining_leaves_before = employee.get_leaves_to_date(
            fields.Datetime.to_string(
                datetime.today() + relativedelta(days=5)))
        self.assertEqual(remaining_leaves_before, 20)

        # test during vacation allocated 20 - 3 days
        remaining_leaves_during = employee.get_leaves_to_date(
            fields.Datetime.to_string(
                datetime.today() + relativedelta(days=13)))
        self.assertEqual(remaining_leaves_during, 16)

        # test after vacation 20 - 6 = 14
        remaining_leaves_after = employee.get_leaves_to_date(
            fields.Datetime.to_string(
                datetime.today() + relativedelta(days=20)))
        self.assertEqual(remaining_leaves_after, 14)

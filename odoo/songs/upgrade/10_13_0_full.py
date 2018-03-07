# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def fix_calendar_on_employee(ctx):
    calendar_model = ctx.env['resource.calendar']
    employees = ctx.env['hr.employee'].search([
        ('calendar_id', '!=', False),
    ])
    for employee in employees:
        ctx.log_line('Process employee: %s' % employee.name)
        good_company = employee.company_id
        current_calendar = employee.calendar_id
        if current_calendar.company_id != good_company:
            ctx.log_line(
                '==> Need to change good_company %s by %s'
                % (
                    employee.calendar_id.company_id.name,
                    good_company.name,
                )
            )
            new_calendar = calendar_model.search([
                ('name', '=', current_calendar.name),
                ('company_id', '=', good_company.id),
            ])
            if not new_calendar:
                new_calendar = current_calendar.copy({
                    'company_id': good_company.id,
                })
            employee.calendar_id = new_calendar


@anthem.log
def fix_resource_calendar_on_contract(ctx):
    calendar_model = ctx.env['resource.calendar']
    contracts = ctx.env['hr.contract'].search([
        ('working_hours', '!=', False),
    ])
    for contract in contracts:
        ctx.log_line('Process contract: %s' % contract.name)
        good_company = contract.employee_id.company_id
        current_calendar = contract.working_hours
        if current_calendar.company_id != good_company:
            ctx.log_line(
                '==> Need to change good_company %s by %s'
                % (
                    contract.working_hours.company_id.name,
                    good_company.name,
                )
            )
            new_calendar = calendar_model.search([
                ('name', '=', current_calendar.name),
                ('company_id', '=', good_company.id),
            ])
            if not new_calendar:
                new_calendar = current_calendar.copy({
                    'company_id': good_company.id,
                })
            contract.working_hours = new_calendar


@anthem.log
def pre(ctx):
    """ PRE update 10.13.0 full """
    fix_calendar_on_employee(ctx)
    fix_resource_calendar_on_contract(ctx)

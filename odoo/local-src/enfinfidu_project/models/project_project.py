# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    company_ids = fields.One2many(
        comodel_name='res.company',
        inverse_name='project_id',
        string='Company',
        copy=False,
        readonly=True,
    )

    supplier_invoice_ids = fields.One2many(
        comodel_name='account.invoice',
        compute='_compute_opened_tasks',
        string='Supplier invoices',
        readonly=True,
        store=False,
    )
    supplier_invoice_count = fields.Integer(
        compute='_compute_opened_tasks',
        string='Number of supplier invoices',
    )

    expense_ids = fields.One2many(
        comodel_name='hr.expense',
        compute='_compute_opened_tasks',
        string='Expenses',
        readonly=True,
        store=False,
    )
    expense_count = fields.Integer(
        compute='_compute_opened_tasks',
        string='Number of expenses',
    )

    bank_statement_ids = fields.One2many(
        comodel_name='account.bank.statement',
        compute='_compute_opened_tasks',
        string='Bank statements',
        readonly=True,
        store=False,
    )
    bank_statement_count = fields.Integer(
        compute='_compute_opened_tasks',
        string='Number of bank statements',
    )

    other_tasks_ids = fields.One2many(
        comodel_name='project.task',
        compute='_compute_opened_tasks',
        string='Other tasks',
        readonly=True,
        store=False,
    )
    other_tasks_count = fields.Integer(
        compute='_compute_opened_tasks',
        string='Number of other tasks',
    )

    @api.multi
    @api.depends(
        'task_ids',
        'task_ids.supplier_invoice_id',
        'task_ids.expense_id',
        'task_ids.bank_statement_id',
        'task_ids.type'
    )
    def _compute_opened_tasks(self):
        for project in self:
            tasks = project.task_ids

            invoices = tasks.mapped('supplier_invoice_id')
            project.supplier_invoice_ids = [(6, 0, invoices.ids)]
            project.supplier_invoice_count = len(invoices)

            expenses = tasks.mapped('expense_id')
            project.expense_ids = [(6, 0, expenses.ids)]
            project.expense_count = len(expenses)

            bank_statements = tasks.mapped('bank_statement_id')
            project.bank_statement_ids = [(6, 0, bank_statements.ids)]
            project.bank_statement_count = len(bank_statements)

            other_tasks = tasks.filtered(lambda t: t.type == 'other')
            project.other_tasks_ids = [(6, 0, other_tasks.ids)]
            project.other_tasks_count = len(other_tasks)

    @api.multi
    def related_supplier_invoices(self):
        self.ensure_one()
        action_ref = 'account.action_invoice_tree2'
        action_data = self.env.ref(action_ref).read()[0]
        action_data['domain'] = [
            ('id', 'in', self.supplier_invoice_ids.ids)
        ]
        return action_data

    @api.multi
    def related_expenses(self):
        self.ensure_one()
        action_ref = 'hr_expense.hr_expense_actions_all'
        action_data = self.env.ref(action_ref).read()[0]
        action_data['view_mode'] = 'tree,form'
        action_data['views'] = [(False, u'tree'), (False, u'form')]
        action_data['domain'] = [
            ('id', 'in', self.expense_ids.ids)
        ]
        return action_data

    @api.multi
    def related_bank_statements(self):
        self.ensure_one()
        action_ref = 'account.action_bank_statement_tree'
        action_data = self.env.ref(action_ref).read()[0]
        action_data['domain'] = [
            ('id', 'in', self.bank_statement_ids.ids)
        ]
        return action_data

    @api.multi
    def related_other_tasks(self):
        self.ensure_one()
        action_ref = 'project.action_view_task'
        action_data = self.env.ref(action_ref).read()[0]
        action_data['domain'] = [
            ('id', 'in', self.other_tasks_ids.ids)
        ]
        return action_data

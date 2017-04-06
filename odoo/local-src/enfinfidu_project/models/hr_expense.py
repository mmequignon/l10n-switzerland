# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    project_id = fields.Many2one(
        related='company_id.project_id',
        string='Project',
        readonly=True,
    )

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='expense_id',
        string='Tasks',
        copy=False,
    )

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        domain=[
            ('type', 'in', ['expense', 'other']),
            ('expense_id', '=', False)
        ],
        compute='_compute_task_id',
        inverse='_inverse_task_id',
    )

    task_attachment_ids = fields.One2many(
        related='task_id.attachment_ids',
        readonly=True,
        string='Task attachments'
    )

    @api.depends('task_ids')
    def _compute_task_id(self):
        for expense in self:
            expense.task_id = (
                expense.task_ids[0]
                if expense.task_ids
                else False
            )

    def _inverse_task_id(self):
        for expense in self:
            expense.task_ids = (
                [(6, 0, [expense.task_id.id])]
                if expense.task_id
                else [(5, 0)]
            )

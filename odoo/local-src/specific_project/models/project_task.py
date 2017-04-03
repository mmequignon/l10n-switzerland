# -*- coding: utf-8 -*-
# © 2017 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_id = fields.Many2one(
        required=True,
    )

    stage_id = fields.Many2one(
        domain=None,
    )

    type = fields.Selection(
        selection=[
            ('supplier_invoice', 'Supplier invoice'),
            ('expense', 'Expense'),
            ('bank_statement', 'Bank statement'),
            ('other', 'Other')
        ],
        default='other',
        required=True,
    )

    @api.onchange('type')
    def _onchange_type(self):
        if self.type != 'supplier_invoice':
            self.supplier_invoice_id = False
        if self.type != 'expense':
            self.expense_id = False
        if self.type != 'bank_statement':
            self.bank_statement_id = False

    supplier_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Supplier invoice',
    )

    expense_id = fields.Many2one(
        comodel_name='hr.expense',
        string='Expense',
    )

    bank_statement_id = fields.Many2one(
        comodel_name='account.bank.statement',
        string='Bank statement',
    )

    company_id = fields.Many2one(
        compute='_compute_company_id',
        store=True,
        readonly=True,
    )

    @api.depends('project_id', 'project_id.company_ids')
    def _compute_company_id(self):
        for task in self:
            if task.project_id and task.project_id.company_ids:
                task.company_id = task.project_id.company_ids[0].id
            else:
                task.company_id = False

# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    project_id = fields.Many2one(
        related='company_id.project_id',
        string='Project',
        readonly=True,
    )

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='supplier_invoice_id',
        string='Tasks',
        copy=False,
    )

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        domain=[
            ('type', 'in', ['supplier_invoice', 'other']),
            ('supplier_invoice_id', '=', False)
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
        for invoice in self:
            invoice.task_id = (
                invoice.task_ids[0]
                if invoice.task_ids
                else False
            )

    def _inverse_task_id(self):
        for invoice in self:
            invoice.task_ids = (
                [(6, 0, [invoice.task_id.id])]
                if invoice.task_id
                else [(5, 0)]
            )

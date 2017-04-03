# -*- coding: utf-8 -*-
# © 2017 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='supplier_invoice_id',
        string='Tasks',
        copy=False,
    )

    project_id = fields.Many2one(
        related='company_id.project_id',
        string='Project',
        readonly=True,
    )

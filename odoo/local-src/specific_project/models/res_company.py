# -*- coding: utf-8 -*-
# © 2017 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
    )

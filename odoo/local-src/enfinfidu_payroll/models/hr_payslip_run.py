# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def _getAccountJournalId(self):
        """Search the journal.id for Salaire"""

        journalCode = 'SAL'
        # Current company of the user
        companyId = self.env.user.company_id.id
        journal = self.env['account.journal'].search([
            ('company_id', '=', companyId),
            ('code', '=', journalCode)
        ])
        return journal.id

    # Set the default value for the journal_id
    journal_id = fields.Many2one(default=_getAccountJournalId)

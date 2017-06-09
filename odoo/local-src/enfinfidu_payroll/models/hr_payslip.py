# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        ok = super(HrPayslip, self).action_payslip_done()
        if not ok:
            return False
        for slip in self:
            if slip.move_id:
                for ml in slip.move_id.line_ids:
                    if ml.partner_id:
                        baid = slip.contract_id.employee_id.bank_account_id
                        ml_dict = {'partner_bank_id': baid.id}
                        ml.write(ml_dict)
        return True

# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from odoo.tools.safe_eval import safe_eval


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    rate_python_compute = fields.Text(
        'Rate', help=""" Rate displayed in the payslip lines
         Available variables:
        ----------------------
         payslip: object containing the payslips
         employee: hr.employee object
         contract: hr.contract object
         rules: object containing the rules code (previously computed)
         categories: object containing the computed salary rule categories
         worked_days: object containing the computed worked days.
         inputs: object containing the computed inputs.

        Note: returned value have to be set in the variable 'rate'

        Example:
        rate = employee.company_id.custom_rate
        """
    )

    @api.multi
    def compute_rule(self, localdict):
        res = super(HrSalaryRule, self).compute_rule(localdict)

        for rule in self:
            if rule.amount_select == 'code' and rule.rate_python_compute:
                safe_eval(rule.rate_python_compute, localdict,
                          mode='exec', nocopy=True)
                rule.percentage = float(localdict.get('rate', '100'))

        return res

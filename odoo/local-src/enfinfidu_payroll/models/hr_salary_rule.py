# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from odoo.tools.safe_eval import safe_eval


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    rate_python_compute = fields.Text(
        'Rate'
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

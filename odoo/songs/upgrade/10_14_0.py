# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def trick_with_res_id(ctx):
    old_tax_templates = ctx.env['account.tax.template'].search(
        [('name', 'like', 'DEPRECATED')]
    )
    new_tax_templates = ctx.env['account.tax.template'].search(
        [('name', 'not like', 'DEPRECATED')]
    )
    for new_tax_template in new_tax_templates:
        for old_tax_template in old_tax_templates:
            if new_tax_template.name in old_tax_template.name:
                model_data = ctx.env['ir.model.data'].search(
                    [('res_id', '=', old_tax_template.id),
                     ('model', '=', 'account.tax.template')]
                )
                if model_data:
                    model_data.res_id = new_tax_template.id


@anthem.log
def pre(ctx):
    """ Pre 10.14.0 """
    trick_with_res_id(ctx)

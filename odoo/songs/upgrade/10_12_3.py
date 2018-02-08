# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem


@anthem.log
def reassign_correct_structure_contract(ctx):
    # Some contract have the correct structure but on a wrong company
    contracts = ctx.env['hr.contract'].search([])
    for contract in contracts:
        if contract.struct_id:
            # This contact has a salary structure we control company_id
            new_structure = get_structure_for_company(
                ctx,
                contract.employee_id.company_id.id,
                contract.struct_id.name)
            if new_structure and contract.struct_id.id != new_structure.id:
                with ctx.log(
                        u'Reassign structure for %s' %
                        contract.employee_id.name):
                    contract.write({'struct_id': new_structure.id})


@anthem.log
def get_structure_for_company(ctx, company_id, structure_name):
    new_structures = ctx.env['hr.payroll.structure'].search(
        [('name', '=', structure_name),
         ('company_id', '=', company_id)], order='id desc')
    if len(new_structures) >= 1:
        for structure in new_structures:
            if structure.rule_ids:
                return structure
    return False


@anthem.log
def clean_structure(ctx):
    new_structures = ctx.env['hr.payroll.structure'].search([])
    for new_stucture in new_structures:
        # Search for dupplicate with no rules
        # search if the record is already deleted or not
        present = ctx.env['hr.payroll.structure'].search([('id', '=',
                                                           new_stucture.id)])
        if not present:
            continue
        rec_del = False
        dup_structures = ctx.env['hr.payroll.structure'].search(
            [('name', '=', new_stucture.name),
             ('company_id', '=', new_stucture.company_id.id),
             ], order='id asc')
        if len(dup_structures) > 1:
            for dup in dup_structures:
                if not dup.rule_ids:
                    with ctx.log(
                            u'Remove dup for struct for %s %s' % (
                                    dup.name, dup.company_id.id)):
                        dup.unlink()
                        rec_del = True
            # Not record delete we assume that both of them have rules we
            # shoot the first one (we have sort differently
            # in get_structure_for_company)
            if not rec_del:
                dup[0].unlink()


@anthem.log
def main(ctx):
    reassign_correct_structure_contract(ctx)
    clean_structure(ctx)

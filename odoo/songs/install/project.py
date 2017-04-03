# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from anthem.lyrics.records import create_or_update

import anthem


@anthem.log
def setup_project(ctx):
    """ Setup project """

    types = ctx.env['project.task.type'].search([])
    types.unlink()

    create_or_update(
        ctx, 'project.task.type', '__setup__.project_task_type_new',
        {
            'name': u'New',
            'sequence': 10,
            'case_default': True,
        })
    create_or_update(
        ctx, 'project.task.type', '__setup__.project_task_type_in_progress',
        {
            'name': u'In progress',
            'sequence': 20,
        })
    create_or_update(
        ctx, 'project.task.type', '__setup__.project_task_type_done',
        {
            'name': u'Done',
            'sequence': 30,
            'fold': True,
        })


@anthem.log
def main(ctx):
    """ Run setup """
    setup_project(ctx)

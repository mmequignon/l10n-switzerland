# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream

from ..common import req


@anthem.log
def import_salary_rule(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/cust_000/hr.salary.rule.csv')
    load_csv_stream(ctx, 'hr.salary.rule', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Run setup """
    import_salary_rule(ctx)

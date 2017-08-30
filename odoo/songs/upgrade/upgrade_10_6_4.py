# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from base64 import b64encode
from pkg_resources import resource_string

import anthem
from ..common import req


@anthem.log
def remove_tagline(ctx):
    """Remove tagline"""
    company = ctx.env.ref('base.main_company')
    company.write({'rml_header1': ''})


@anthem.log
def set_reports_logo(ctx):
    """Set report_logo for all companies"""
    main_company = ctx.env.ref('base.main_company')
    logo_content = resource_string(
        req, 'data/images/company_main_report_logo.png')
    b64_logo = b64encode(logo_content)
    main_company.report_logo = b64_logo

    for company in ctx.env['res.company'].search(
            [('id', '!=', main_company.id)]):
        company.report_logo = company.logo


@anthem.log
def post(ctx):
    """ Run setup """
    remove_tagline(ctx)
    set_reports_logo(ctx)

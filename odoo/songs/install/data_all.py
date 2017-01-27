# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

""" Data loaded in all modes

The data loaded here will be loaded in the 'demo' and
'full' modes.

"""


from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream

from ..common import req


@anthem.log
def load_analytic_accounts(ctx):
    """ Load Analytic Accounts """
    filepath = 'data/install/account.analytic.account.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'account.analytic.account', csv_content)


@anthem.log
def load_users(ctx):
    """ Load Users """
    filepath = 'data/install/res.users.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'res.users', csv_content)


@anthem.log
def main(ctx):
    """ Loading data """
    load_analytic_accounts(ctx)
    load_users(ctx)

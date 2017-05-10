# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from pkg_resources import resource_stream
from anthem.lyrics.loaders import load_csv_stream
from ..common import req


""" Data loaded in all modes

The data loaded here will be loaded in the 'demo' and
'full' modes.

"""


@anthem.log
def load_product_template(ctx):
    """ Load account payment mode """
    filepath = 'data/install/shared_data/product.template.csv'
    csv_content = resource_stream(req, filepath)
    load_csv_stream(ctx, 'product.template', csv_content)


@anthem.log
def main(ctx):
    """ Loading data """
    load_product_template(ctx)

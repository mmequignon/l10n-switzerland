# Copyright 2011-2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import models


def post_init(cr, registry):
    """Import CSV data as it is faster than xml and because we can't use
    noupdate anymore with csv"""
    from odoo.tools import convert_file
    filenames = ['data/res.city.csv', 'data/res.city.zip.csv']
    for filename in filenames:
        convert_file(
            cr, 'l10n_ch_zip',
            filename, None, mode='init', noupdate=True,
            kind='init', report=None,
        )

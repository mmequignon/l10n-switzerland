# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def create_mail_server(ctx):
    """Create mail server"""
    values = {
        'name': "Mail Server",
        }
    create_or_update(ctx, 'fetchmail.server',
                     '__setup__.mail_server', values)


@anthem.log
def main(ctx):
    """ Run setup """
    create_mail_server(ctx)

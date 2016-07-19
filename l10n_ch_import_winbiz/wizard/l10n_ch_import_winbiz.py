# -*- coding: utf-8 -*-
# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import sys
import traceback
import logging
import base64
from lxml import etree
import tempfile
from itertools import izip_longest
from StringIO import StringIO
from openerp import models, fields, api, exceptions
from datetime import datetime


_logger = logging.getLogger(__name__)


class AccountWinbizImport(models.TransientModel):
    _name = 'account.winbiz.import'
    _description = 'Import Accounting Winbiz'
    _rec_name = 'state'

    company_id = fields.Many2one('res.company', 'Company',
                                 invisible=True)
    report = fields.Text(
        'Report',
        readonly=True
        )
    journal_id = fields.Many2one('account.journal', 'Journal',
                                 required=True)
    state = fields.Selection(selection=[('draft', "Draft"),
                                        ('done', "Done"),
                                        ('error', "Error")],
                             readonly=True,
                             default='draft')
    file = fields.Binary(
        'File',
        required=True
        )
    imported_move_ids = fields.Many2many(
        'account.move', 'import_cresus_move_rel',
        string='Imported moves')

    help_html = fields.Html('Import help', readonly=True,
                            default='''
                 In order to import your 'Winbiz Salaires' .xml \
                 file you must complete the following requirements : \
                <ul>
                <li> The accounts, analytical accounts used in the Cresus\
                 file must be previously created into Odoo  </li>
                </ul>''')

    ODOO_MOVE_ARGS = {'ref', 'date', 'journal_id'}

    @staticmethod
    def make_move(lines, **kwargs):
        # assert set(kwargs.keys()) == self.ODOO_MOVE_ARGS
        kwargs.update({'line_ids': [(0, 0, ln) for ln in lines]})
        return kwargs

    ODOO_LINE_ARGS = {'account_id', 'partner_id', 'name',
                      'tax_line_id', 'analytic_account_id'}

    @staticmethod
    def make_line(debit=0.0, credit=0.0, **kwargs):
        # assert set(kwargs.keys()) == self.ODOO_LINE_ARGS
        kwargs.update({'debit': debit, 'credit': credit})
        return kwargs

    @api.multi
    def open_account_moves(self):
        res = {
            'domain': str([('id', 'in', self.imported_move_ids.ids)]),
            'name': 'Account Move',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
        return res

    def _parse_xml(self):
        """Parse stored XML file.

        Manage base 64 decoding.

        :param imp_id: current importer id
        :returns: generator

        """
        # We use tempfile in order to avoid memory error with large files
        with tempfile.TemporaryFile() as src:
            content = self.file
            src.write(content)
            with tempfile.TemporaryFile() as decoded:
                src.seek(0)
                base64.decode(src, decoded)
                decoded.seek(0)
                for a, e in etree.iterparse(decoded, tag=u'c_tmpexport'):
                    yield {kid.tag: kid.text for kid in e.getchildren()}

    @staticmethod
    def _parse_date(date_string):
        """Parse a date coming from Winbiz and put it in the format used by Odoo.

           :param date_string: winbiz data
           :returns: a date string
        """
        format = '%Y-%m-%d'
        dt = datetime.strptime(date_string, format)
        return fields.Date.to_string(dt)

    def _find_account(self, code):
        account_obj = self.env['account.account']
        account = account_obj.search([('code', '=', code)], limit=1)
        if not account:
            raise exceptions.MissingError("No account with code %s" % code)
        return account

    @api.multi
    def _standardise_data(self, data):
        """ This function split one line of the XML into multiple lines.
        Winbiz just writes one line per move.
        """

        journal_id = self.journal_id.id
        cp = self.env.user.company_id
        company_partner = cp.partner_id.name
        previous_pce = None
        previous_date = None
        lines = []
        for self.index, winbiz_item in enumerate(data, 1):
            if previous_pce is not None and previous_pce != winbiz_item[u'pièce']:
                yield self.make_move(
                    lines,
                    date=previous_date,
                    ref=previous_pce,
                    journal_id=journal_id)
                lines = []
            previous_pce = winbiz_item[u'pièce']
            previous_date = self._parse_date(winbiz_item[u'date'])

            amount = float(winbiz_item[u'montant'])

            recto_line = self.make_line(
                debit=amount,
                account_id=self._find_account(winbiz_item[u'cpt_débit']).id,
                partner_id=False,
                name=winbiz_item[u'libellé'],
                tax_line_id=None,
                analytic_account_id=None)
            lines.append(recto_line)

            verso_line = self.make_line(
                credit=amount,
                account_id=self._find_account(winbiz_item[u'cpt_crédit']).id,
                partner_id=False,
                name=winbiz_item[u'libellé'],
                tax_line_id=None,
                analytic_account_id=None)
            lines.append(verso_line)

        yield self.make_move(
            lines,
            date=previous_date,
            ref=previous_pce,
            journal_id=journal_id)

    @api.multi
    def _import_file(self):
        move_obj = self.env['account.move']
        data = self._parse_xml()
        data = self._standardise_data(data)
        self.imported_move_ids = [move_obj.create(mv).id for mv in data]

    @api.multi
    def import_file(self):
        try:
            self._import_file()
        except Exception as exc:
            self.env.cr.rollback()
            self.write({
                'state': 'error',
                'report': 'Error (at row %s):\n%s' % (self.index, exc)})
            return {'name': 'Import Move lines',
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.winbiz.import',
                    'res_id': self.id,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new'}
        self.state = 'done'
        # show the resulting moves in main content area
        return {'domain': str([('id', 'in', self.imported_move_ids.ids)]),
                'name': 'Imported Journal Entries',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'view_id': False,
                'type': 'ir.actions.act_window'}

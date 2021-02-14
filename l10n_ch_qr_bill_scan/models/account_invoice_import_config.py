# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountInvoiceImportConfig(models.Model):
    _inherit = "account.invoice.import.config"

    tax_control = fields.Boolean(
        default=False,
    )
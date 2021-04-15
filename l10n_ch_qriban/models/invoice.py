# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re

from odoo import api, models
from odoo.tools.misc import mod10r

l10n_ch_ISR_NUMBER_LENGTH = 27
l10n_ch_ISR_ID_NUM_LENGTH = 6


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def _need_isr_ref(self):
        """Uses hook of l10n_ch_fix_isr_reference module"""
        has_qriban = (
            self.partner_bank_id and
            self.partner_bank_id._is_qr_iban() or False
        )
        return has_qriban or super()._need_isr_ref()

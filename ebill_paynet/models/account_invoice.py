# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_sent(self):
        """ """
        # Should it be done on open or sent ?
        res = super().action_invoice_sent()
        paynet_method = self.env.ref('ebill_paynet.paynet_transmit_method')
        for invoice in self:
            if invoice.transmit_method_id != paynet_method:
                continue
            print("LET GET THAT EBILL SENT")
            # Get the ebill.contract
            contract = self.env['ebill.payment.contract'].search(
                [
                    ('is_valid', '=', True),
                    ('partner_id', '=', invoice.partner_id.id),
                ],
                limit=1
            )
            if not contract:
                print('No valid contract what to do ?')
                continue
            # Create a paynet.invoice.message
            # pdf = self.env['report'].sudo().get_pdf([invoice.id], 'account.report_invoice')
            r = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
            pdf, _ = r.render(invoice.id)
            attachment = self.env['ir.attachment'].create({
                'name': 'paynet ebill',
                'type': 'binary',
                'datas': base64.b64encode(pdf),
                'res_model': 'account.invoice',
                'res_id': invoice.id,
                'mimetype': 'application/x-pdf',
            })
            message = self.env['paynet.invoice.message'].create({
                'invoice_id': invoice.id,
                'attachment_id': attachment.id,
                'ebill_account_number': contract.paynet_account_number,
            })
            # Send the ebill
            # message.send_to_paynet()

        return res

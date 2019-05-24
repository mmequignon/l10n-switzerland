# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Need Jinja 2.10 
# from jinja2 import Environment, select_autoescape
from odoo import api, fields, models

# jinja_env = Environment(autoescape=select_autoescape(['xml']))


class PaynetInvoiceMessage(models.Model):

    _name = "paynet.invoice.message"

    invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        ondelete="restrict"
    )
    attachment_id = fields.Many2one('ir.attachment', 'PDF')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('reject', 'Reject'),
        ('error', 'Error'),
        ],
        default='draft'
    )
    ic_ref = fields.Char('IC Ref', size=14, help="Document reference")
    # Set with invoice_id.number but also with returned data from server ?
    ref = fields.Char('Reference N°', size=35)
    ebill_account_number = fields.Char('Paynet Id', size=20)
    payload = fields.Text('Payload sent')
    response = fields.Text('Response recieved')


    @api.multi
    def generate_payload(self):
        for message in self:
            biller = message.invoice_id.commercial_partner_id
            customer = message.invoice_id.partner_id
            # pay_cont = self.env['ebill.payment.contract'].search(message.invoice_id.get_payment_contract()

            assert message.state == 'draft'
            assert biller.paynet_billerid
            # assert pay_cont.ebill_account_number

            with message.attachment_id._open() as fobj:
                data = PdfFile.removeSignature(fobj)
                b64data = base64.b64encode(data).rstrip()

            # ref: maximum 14 chars
            document_ref = 'SA%012d' % message.id

            bank = message.invoice_id.partner_bank_id
            bank_account = self.pool['res.partner.bank'].acc_number_digits(cr, uid, bank.id)

            if message.invoice_id.type != 'out_invoice' or message.invoice_id.abacus_residual == 0:
                # No payment
                payment_type = 'NPY'
            elif message.invoice_id.abacus_residual == message.invoice_id.amount_total:
                # ESR with fixed amount (no distinction fixed/variable in customer's e-banking)
                payment_type = 'ESR'
            else:
                # ESR with variable amount
                payment_type = 'ESP'

            with open(INVOICE_TEMPLATE) as tpl:
                templ = Template(tpl.read(), input_encoding='utf-8',
                                 default_filters=['unicode', 'x'],
                                 future_imports=['unicode_literals'])

            payload = templ.render_unicode(
                invoice=message.invoice_id,
                invoice_esr=self.pool['account.invoice']._get_ref(message.invoice_id),
                invoice_esr_bank=bank_account,
                biller=biller,
                customer=customer,
                document_ref=document_ref,
                document_type=DOCUMENT_TYPE[message.invoice_id.type],
                payment_type=payment_type,
                ebill_account_number=pay_cont.ebill_account_number,
                biller_address=biller.partner_id._get_address('invoice'),
                customer_address=customer._get_address('invoice'),
                pdf_data=b64data,
                format_date=format_date,
            )

            message.write({
                'ic_ref': document_ref,
                'reference_no': report.invoice_id.number,
                'ebill_account_number': pay_cont.ebill_account_number,
                'payload': payload,
            })
        return True

# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from datetime import datetime
# Need Jinja 2.10 
# from mako.template import Template
from jinja2 import Environment, select_autoescape, FileSystemLoader
from odoo import api, fields, models
from odoo.modules.module import get_module_root


MODULE_PATH = get_module_root(os.path.dirname(__file__))
INVOICE_TEMPLATE = 'invoice-2013A.xml'
TEMPLATE_DIR = MODULE_PATH + '/messages'

DOCUMENT_TYPE = {
    'out_invoice': 'EFD',
    'out_refund': 'EGS',
}

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['xml'])
)
template = jinja_env.get_template(INVOICE_TEMPLATE)


class PaynetInvoiceMessage(models.Model):

    _name = "paynet.invoice.message"

    service_id = fields.Many2one(
        comodel_name="paynet.service",
        string="Paynet Service",
        required=True,
        ondelete="restrict",
        readonly=True,
    )
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
    ic_ref = fields.Char(
        string="IC Ref",
        size=14,
        compute='_compute_ic_ref',
        help="Document interchange reference",
    )
    # Set with invoice_id.number but also with returned data from server ?
    ref = fields.Char('Reference N°', size=35)
    ebill_account_number = fields.Char('Paynet Id', size=20)
    payload = fields.Text('Payload sent')
    response = fields.Text('Response recieved')

    @api.depends()
    def _compute_ic_ref(self):
        for message in self:
            message.ic_ref = 'SA%012d' % message.id

    @api.multi
    def send_to_paynet(self):
        self.generate_payload()
        # send it

    @staticmethod
    def format_date(date_string=0, fmt='%Y%m%d'):
        """Reformat an ISO 8601 date and return 'dd.mm.yyyy'
            This date format is "little-endian, dot-separated'
            It is used in many countries, including Germany and Switzerland
        """
        # if isinstance(date_string, (int, long, float)):
            # return today(date_string, fmt=fmt)
        if not date_string:
            date_string = datetime.now()
        if date_string:
            if hasattr(date_string, 'strftime'):
                return date_string.strftime(fmt)
            date_part = date_string.split()[0]
            return datetime.strptime(date_part, '%Y-%m-%d').strftime(fmt)

    @api.multi
    def generate_payload(self):
        for message in self:
            # biller = message.invoice_id.commercial_partner_id
            biller = message.invoice_id.company_id
            customer = message.invoice_id.partner_id
            # pay_cont = self.env['ebill.payment.contract'].search(message.invoice_id.get_payment_contract()

            assert message.state == 'draft'
            # assert biller.paynet_billerid
            # assert pay_cont.ebill_account_number

            # with message.attachment_id.datas as fobj:
                # data = PdfFile.removeSignature(fobj)
                # b64data = base64.b64encode(data).rstrip()
            b64data = message.attachment_id.datas

            bank = message.invoice_id.partner_bank_id
            # bank_account = self.pool['res.partner.bank'].acc_number_digits(cr, uid, bank.id)
            bank_account = bank.sanitized_acc_number

            if message.invoice_id.type == 'out_invoice':
                # ESR with fixed amount (no distinction fixed/variable in customer's e-banking)
                payment_type = 'ESR'
                # ESP with variable amount
                # payment_type = 'ESP'
            else:
                # No payment
                payment_type = 'NPY'

            # with open(INVOICE_TEMPLATE) as tpl:
            #     templ = Template(tpl.read(), input_encoding='utf-8',
            #                      default_filters=['unicode', 'x'],
            #                      future_imports=['unicode_literals'])

            payload = template.render(
                client_pid=message.service_id.client_pid,
                invoice=message.invoice_id,
                # TODO fix this one
                invoice_esr='ref esr', #self.pool['account.invoice']._get_ref(message.invoice_id),
                # invoice_esr_bank=bank_account,
                bank=bank,
                biller=biller,
                customer=customer,
                ic_ref=message.ic_ref,
                document_type=DOCUMENT_TYPE[message.invoice_id.type],
                payment_type=payment_type,
                ebill_account_number=message.ebill_account_number, #pay_cont.ebill_account_number,
                biller_address=biller, #biller.address_get(['invoice'])['invoice'],
                customer_address=customer, #customer.address_get(['invoice'])['invoice'],
                pdf_data=b64data,
                format_date=self.format_date,
            )
            message.write({
                # 'reference_no': report.invoice_id.number,
                # 'ebill_account_number': pay_cont.ebill_account_number,
                'payload': payload,
            })
        return True

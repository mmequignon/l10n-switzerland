# -*- coding: utf-8 -*-
import base64
import os

from odoo import tools

from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Settings
from zeep.transports import Transport

# PENDING_STATES = {'ShipmentState': ['ReadyForSending', 'Submitted']}

TEST_URL = 'https://dws-test.paynet.ch/DWS/DWS/'
WSDL_DOC = os.path.join(os.path.dirname(__file__), 'wsdl', 'DWSPayNet.wsdl')
SSL_CERTIFICATE = os.path.join(os.path.dirname(__file__), 'certificats', 'pseudo__System-Services.chain.pem')


# def set_content_encoding(context):
#     content = context.envelope.childAtPath('Body/ShipmentDeliveryMsg/Content')
#     if content is not None:
#         content.set('encoding', 'UTF-8')

class PayNetDWS(object):
    """PayNet DWS web services."""
    # _hooks = {
    #     'marshalled': set_content_encoding,
    # }

    def __init__(self):
        self.settings = Settings(strict=False, xml_huge_tree=True)
        session = Session()
        session.verify = SSL_CERTIFICATE
        transport = Transport(session=session)
        self.client = Client(WSDL_DOC, transport=transport)

    @staticmethod
    def userid():
        return os.getenv('PAYNET_USERID')

    @staticmethod
    def password():
        return os.getenv('PAYNET_PASSWORD')

    def authorization(self):
        auth = {'UserName': self.userid(), 'Password': self.password()}
        return auth


    # def post(self, data):
    #     if isinstance(data, unicode):
    #         data = data.encode('utf-8')
    #     b64content = base64.b64encode(data)
    #     with self:
    #         docid = self.service.takeShipment(self._auth, Content=b64content)
    #     return str(docid)

    # def list_iter(self):
    #     with self:
    #         res = self.service.getShipmentList(self._auth)
    #     for item in res.Shipment:
    #         yield {
    #             'id': str(item.ShipmentID),
    #             'date': str(item.CreationDate),
    #             'state': str(item.ShipmentState),
    #             'sender': str(item.SenderID),
    #             'receiver': str(item.ReceiverID),
    #             'size': int(item.ContentSize),
    #             'priority': int(item.ShipmentPriority),
    #             # DocumentIdentifier
    #             'doc_name': str(item.DocumentIdentifier.Name),
    #             'doc_type': str(item.DocumentIdentifier.Type),
    #             'doc_format': str(item.DocumentIdentifier.Format),
    #             'doc_version': str(item.DocumentIdentifier.Version),
    #             'doc_extension': str(item.DocumentIdentifier.Extension),
    #             'doc_category': str(item.DocumentIdentifier.Category),
    #         }

    # def get(self, docid):
    #     with self:
    #         res = self.service.getShipmentContent(self._auth, docid)
    #     data = base64.b64decode(res.Content)
    #     return load_xml(data)

    # def confirm(self, docid):
    #     with self:
    #         self.service.confirmShipmentReceipt(self._auth, docid)
    #     return True

    # def iter_documents(self, ignore_state=False):
    #     states = None if ignore_state else PENDING_STATES
    #     with self:
    #         res = self.service.getShipmentList(self._auth, ShipmentStates=states)
    #     if not res:
    #         return
    #     for item in res.Shipment:
    #         assert (item.DocumentIdentifier.Category,
    #                 item.DocumentIdentifier.Extension) == ('Structured', 'xml'), item
    #         assert item.ShipmentState in ('ReadyForSending', 'Submitted', 'ArrivedAtDestination'), item

    #         resp = self.get(item.ShipmentID)

    #         # Remember the document ID
    #         resp._ID = str(item.ShipmentID)

    #         resp._meta = {
    #             'date': str(item.CreationDate),
    #             'state': str(item.ShipmentState),
    #             'sender': str(item.SenderID),
    #             'receiver': str(item.ReceiverID),
    #             'size': int(item.ContentSize),
    #             'priority': int(item.ShipmentPriority),
    #             # DocumentIdentifier
    #             'doc_name': str(item.DocumentIdentifier.Name),
    #             'doc_type': str(item.DocumentIdentifier.Type),
    #             'doc_format': str(item.DocumentIdentifier.Format),
    #             'doc_version': str(item.DocumentIdentifier.Version),
    #         }
    #         yield resp

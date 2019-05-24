# import base64
import os

from lxml import html
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport

WSDL_DOC = os.path.join(os.path.dirname(__file__), 'wsdl', 'DWSPayNet.wsdl')
SSL_PROD_CERTIFICATE = os.path.join(
    os.path.dirname(__file__), 'certificats', 'prod_services_chain.pem'
)
SSL_TEST_CERTIFICATE = os.path.join(
    os.path.dirname(__file__), 'certificats', 'test_services_chain.pem'
)


class PayNetDWS(object):
    """PayNet DWS web services."""

    def __init__(self, url, test_service):
        settings = Settings(xml_huge_tree=True)
        session = Session()
        if test_service:
            session.verify = SSL_TEST_CERTIFICATE
        else:
            session.verify = SSL_PROD_CERTIFICATE
        transport = Transport(session=session)
        self.client = Client(WSDL_DOC, transport=transport, settings=settings)
        if url:
            self.service = self.client.create_service(
                '{http://www.sap.com/DWS}DWSBinding', url
            )
        else:
            self.service = self.client.service

    @staticmethod
    def authorization(userid, password):
        """Generate Authorization node."""
        return {'UserName': userid, 'Password': password}

    @staticmethod
    def handle_fault(fault):
        msg = ('{}\n' 'code: {} -> {}\n' 'actor: {}\n' 'detail: {}\n').format(
            fault.message.upper(),
            fault.code,
            fault.subcodes,
            fault.actor,
            html.tostring(fault.detail),
        )
        return msg

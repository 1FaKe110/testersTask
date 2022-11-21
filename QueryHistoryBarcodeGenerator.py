import datetime

from lxml import etree as et

from XmlSaver import XmlSaver
from XmlSender import XmlSender


class QueryHistory(XmlSaver, XmlSender):

    def __init__(self, circuit='test', filename=None):
        super().__init__(circuit)
        self.filename = filename or 'QueryHistoryBarcode.xml'
        self.nsmap = {
            "ns": 'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01',
            'qp': 'http://fsrar.ru/WEGAIS/QueryParameters'
        }

    def generate_document(self, mark: str):
        documents = et.Element('{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Documents', nsmap=self.nsmap)
        owner = et.SubElement(documents, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Owner')
        fsrarid = et.SubElement(owner, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}FSRAR_ID')
        fsrarid.text = '010000006090'

        document = et.SubElement(documents, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Document')
        qhb = et.SubElement(document, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}QueryHistoryBCode')
        parameters = et.SubElement(qhb, '{http://fsrar.ru/WEGAIS/QueryParameters}Parameters')
        parameter = et.SubElement(parameters, '{http://fsrar.ru/WEGAIS/QueryParameters}Parameter')
        name = et.SubElement(parameter, '{http://fsrar.ru/WEGAIS/QueryParameters}Name')
        value = et.SubElement(parameter, '{http://fsrar.ru/WEGAIS/QueryParameters}Value')
        name.text = 'ШК'
        value.text = mark

        return documents


def main():
    qh = QueryHistory()
    print(qh.send(qh.generate_document('22N00000XOKBM71KO952N0S712050180034224R200JCI75CVKVWXZ0CGCA6OV8XHRIS')))


if __name__ == '__main__':
    main()

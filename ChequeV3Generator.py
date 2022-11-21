import datetime

from lxml import etree as et
from random import randrange as rr, randint as ri

from BarcodeGenerator import BarcodeGenerator
from XmlSaver import XmlSaver


class ChequeGenerator(BarcodeGenerator, XmlSaver):
    def __init__(self, filename=None):
        super().__init__()
        self.filename = filename or 'ChequeV3.xml'
        self.nsmap = {
            "xsi": 'http://www.w3.org/2001/XMLSchemainstance',
            "ns": 'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01',
            'ck': 'http://fsrar.ru/WEGAIS/ChequeV3',
            'oref': 'http://fsrar.ru/WEGAIS/ClientRef_v2',
            'pref': 'http://fsrar.ru/WEGAIS/ProductRef_v2'
        }

    def generate_bottle(self, mark):

        bottle = et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Bottle')

        data = {
            'barcode': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Barcode'),
            'ean': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}EAN'),
            'price': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Price')
        }
        data['barcode'].text = mark
        data['ean'].text = self.add_zeros(rr(0, 9_999_999_999_999), 13)
        data['price'].text = f'{rr(50, 10_000)}'

        for value in data.values():
            bottle.append(value)

        return bottle

    def generate_cheque(self):
        documents = et.Element('{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Documents', nsmap=self.nsmap)
        owner = et.SubElement(documents, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Owner')
        fsrarid = et.SubElement(owner, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}FSRAR_ID')
        fsrarid.text = '010000006090'

        document = et.SubElement(documents, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Document')
        cheque_v3 = et.SubElement(document, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}ChequeV3')
        identifier = et.SubElement(cheque_v3, '{http://fsrar.ru/WEGAIS/ChequeV3}Identity')
        identifier.text = f"{datetime.datetime.today().strftime('%Y-%M-%D')}/{datetime.datetime.today().timestamp()}"
        header = et.SubElement(cheque_v3, '{http://fsrar.ru/WEGAIS/ChequeV3}Header')

        cheque_v3_data = {
            'Date': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Date'),
            'Kassa': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Kassa'),
            'Shift': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Shift'),
            'Number': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Number'),
            'Type': et.Element('{http://fsrar.ru/WEGAIS/ChequeV3}Type')
        }
        cheque_v3_data['Date'].text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        cheque_v3_data['Kassa'].text = f'{int(datetime.datetime.now().timestamp())}'
        cheque_v3_data['Shift'].text = f'{rr(0, 999)}'
        cheque_v3_data['Number'].text = f'{rr(0, 9999)}'
        cheque_v3_data['Type'].text = 'Продажа' if bool(rr(0, 1)) else 'Возврат'

        for value in cheque_v3_data.values():
            header.append(value)

        content = et.SubElement(cheque_v3, '{http://fsrar.ru/WEGAIS/ChequeV3}Content')

        marks = self.get_new(rr(1, 10)) + self.get_old(rr(1, 10))
        for mark in marks:
            content.append(self.generate_bottle(mark))

        return documents


def main():
    cg = ChequeGenerator()
    cg.save_cheque(cg.generate_cheque(), cg.filename)


if __name__ == '__main__':
    main()

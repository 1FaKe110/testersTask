import datetime

from lxml import etree as et
from random import randrange as rr

from BarcodeGenerator import BarcodeGenerator
from XmlSaver import XmlSaver


class ChequeGenerator(BarcodeGenerator, XmlSaver):
    def __init__(self, filename=None):
        super().__init__()
        self.filename = filename or 'ChequeV0.xml'

    @staticmethod
    def generate_bottle(mark):
        bottle = et.Element('Bottle')
        bottle.attrib['price'] = f'{rr(100, 999_999) / 100}'
        bottle.attrib['barcode'] = mark
        bottle.attrib['volume'] = f'{rr(5, 9_999_999, 5) / 10_000}'
        bottle.attrib['ean'] = ''.join(str(rr(0, 9)) for _ in range(13))
        return bottle

    def generate_cheque(self):
        root = et.Element('Cheque')
        root.attrib['inn'] = ''.join(str(rr(0, 9)) for _ in range(10))
        root.attrib['kpp'] = ''.join(str(rr(0, 9)) for _ in range(9))
        root.attrib['address'] = 'address'
        root.attrib['name'] = 'name'
        root.attrib['kassa'] = ''.join(str(rr(0, 9)) for _ in range(16))
        root.attrib['shift'] = ''.join(str(rr(0, 9)) for _ in range(3))
        root.attrib['number'] = ''.join(str(rr(0, 9)) for _ in range(5))
        root.attrib['datetime'] = datetime.datetime.now().strftime('%d$m%y%H%M')

        marks = self.get_new(rr(1, 10)) + self.get_old(rr(1, 10))
        for mark in marks:
            root.append(self.generate_bottle(mark))

        return root


def main():
    cg = ChequeGenerator()
    cg.save_cheque(cg.generate_cheque(), cg.filename)


if __name__ == '__main__':
    main()

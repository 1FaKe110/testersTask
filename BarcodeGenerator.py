from pprint import pprint
from random import randrange as rr
from Base36Converter import Base36
from datetime import datetime


class BarcodeGenerator(Base36):

    def __init__(self):
        super().__init__()
        self.alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    @staticmethod
    def add_zeros(x, length: int) -> str:
        return f'{"0" * (length - len(str(x)))}{x}'

    def gen_old_mark(self):
        """
        Generate old barcode where length is 68 symbols.
        """

        version = self.add_zeros(rr(0, 99), 2) + 'N'
        alc = self.add_zeros(self.to_base36(rr(0, 99999999999999999)), 16)
        org_number = self.add_zeros(self.to_base36(rr(0, 999999)), 4)
        year = str(datetime.today().year)[-1]
        mount = self.add_zeros(datetime.today().month, 2)
        day = self.add_zeros(datetime.today().day, 2)
        rand_num = self.add_zeros(rr(0, 999), 3)
        rand_num2 = self.add_zeros(rr(0, 999999), 6)
        sign = ''.join(self.alf[rr(0, len(self.alf))] for _ in range(31))

        mark = f'{version}{alc}{org_number}{year}{mount}{day}{rand_num}{rand_num2}{sign}'.upper()
        if len(mark) != 68:
            raise RuntimeError(f"Invalid mark length: {len(mark)}")
        return mark

    def gen_new_mark(self):
        """
        Generate new barcode where length is 150 symbols
        """
        tpe = self.add_zeros(rr(0, 999), 3)
        ser = self.add_zeros(rr(0, 999), 3)
        num = self.add_zeros(rr(0, 999), 8)
        egs = self.add_zeros(rr(0, 999), 7)
        sign = ''.join(self.alf[rr(0, len(self.alf))] for _ in range(129))

        mark = f'{tpe}{ser}{num}{egs}{sign}'

        if len(mark) != 150:
            raise RuntimeError(f"Invalid mark length: {len(mark)}")
        return mark

    def get_old(self, amount):
        """Returns list of barcodes where length is 68"""
        return [self.gen_old_mark() for _ in range(amount)]

    def get_new(self, amount):
        """Returns list of barcodes where length is 150"""
        return [self.gen_new_mark() for _ in range(amount)]


def main():
    bg = BarcodeGenerator()
    print("Old barcodes: ")
    pprint(bg.get_old(20))
    print("New barcodes: ")
    pprint(bg.get_new(20))


if __name__ == '__main__':
    main()

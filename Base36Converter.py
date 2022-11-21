class Base36:

    def __init__(self):
        self.alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

    def to_base36(self, number: int) -> str:
        value = ''
        while number != 0:
            number, index = divmod(number, len(self.alphabet))
            value = self.alphabet[index] + value

        return value or '0'

    @staticmethod
    def from_base36(value: str) -> int:
        return int(value, 36)

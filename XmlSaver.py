from lxml import etree as et


class XmlSaver:

    @staticmethod
    def save_cheque(root, filename):
        chq = et.tostring(root, encoding='utf-8')
        with open(f'out_files/{filename}', 'w', encoding='utf-8') as f:
            f.write(chq.decode('utf-8'))

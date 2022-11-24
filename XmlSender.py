from pprint import pprint

import requests as rq
from lxml import etree as et
from dataclasses import dataclass
from os import getlogin
import logging


import paramiko
import sshtunnel


@dataclass
class XmlSender:
    __main_circuits = {
        'sand': {
            "srv": "gitlab-ci.ru:9092",
            "netty": "http://194.67.93.217:14206/wb",
            "topic": 'piter-in'
        },
        'test': {
            "srv": "10.10.4.28:9092",
            "netty": "http://10.10.4.247:8002/wb",
            "topic": 'cc'
        },
        'prod': {
            "srv": "prod-kafka-01.nd.fsrar.ru:9092",
            "netty": "http://10.10.5.226:8001/wb",
            "topic": 'cheqconfirm'
        }
    }

    def __init__(self, circuit):
        self.netty = self.__main_circuits[circuit]['netty']
        self.logger = logging.getLogger(__name__)

    def send(self, etree_file):
        xml = et.tostring(etree_file, encoding='utf-8')
        files = {'file': xml.decode("utf-8")}

        tunnel = sshtunnel.SSHTunnelForwarder(
            '208',
            remote_bind_address=('10.0.50.208', 20010),
            ssh_config_file=f'/home/{getlogin()}/.ssh/config',
            ssh_pkey=f'/home/{getlogin()}/.ssh/id_rsa',
            ssh_username='Gabko',
            logger=self.logger
        )
        # print(tunnel.read_private_key_file(f'/home/{getlogin()}/.ssh/id_rsa'))
        print(tunnel.start())
        print(tunnel.stop())

        # tunnel.start()
        # print(tunnel.local_bind_port)
        # resp = rq.post(self.netty, files=files, timeout=1)
        # tunnel.stop()

        return ''


def main():
    logging.getLogger('main').setLevel(logging.DEBUG)
    sender = XmlSender('test')
    resp = sender.send(et.parse('out_files/ChequeV0.xml'))
    pprint(resp)


if __name__ == '__main__':
    main()

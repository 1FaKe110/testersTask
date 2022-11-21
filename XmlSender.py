from pprint import pprint

import requests as rq
from lxml import etree as et
from dataclasses import dataclass
from os import getlogin

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

    def send(self, etree_file):
        xml = et.tostring(etree_file, encoding='utf-8')
        files = {'file': xml.decode("utf-8")}

        with sshtunnel.open_tunnel(
            ('10.0.50.208', 443),
            ssh_username='Gabko',
            ssh_pkey=f'/home/{getlogin()}/.ssh/id_rsa',



        ) as tunnel:
            resp = rq.post(self.netty, files=files)


        return resp


def main():
    sender = XmlSender('test')
    resp = sender.send(et.parse('out_files/ChequeV0.xml'))
    pprint(resp)


if __name__ == '__main__':
    main()
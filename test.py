from sshtunnel import open_tunnel
from time import sleep
from QueryHistoryBarcodeGenerator import QueryHistory


def main():
    with open_tunnel(
            ssh_address_or_host='10.0.50.208',
            ssh_username="Gabko",
            ssh_pkey="/home/ifake/.ssh/id_rsa.pub",
            remote_bind_address=('127.0.0.1', 3306)
    ) as server:
        print(server.local_bind_port)

    print('FINISH!')


if __name__ == '__main__':
    main()

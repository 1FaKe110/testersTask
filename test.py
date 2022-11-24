from sshtunnel import open_tunnel


def main():
    args = {'ssh_address': '208', 'ssh_port': 22, 'remote_bind_addresses': [('10.0.50.208', 20010)], 'threaded': False, 'ssh_config_file': '~/.ssh/config', 'compression': False, 'allow_agent': True,
            'debug_level': 40}

    with open_tunnel(**args) as server:
        print(server.local_bind_port)

    print('FINISH!')


if __name__ == '__main__':
    main()

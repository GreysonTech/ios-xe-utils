"""
 Netconf python example by yang-explorer (https://github.com/CiscoDevNet/yang-explorer)

 Installing python dependencies:
 > pip install lxml ncclient

 Running script: (save as example.py)
 > python example.py -a 192.168.1.1 -u netconf -p netconf --port 830
"""


import lxml.etree as ET

from argparse import ArgumentParser
from getpass import getpass
from json import decoder, dumps, encoder, load
from ncclient import manager
from ncclient.operations import RPCError
from xmltodict import parse



def file_handler(fnc, path, mode_='rt', newline_=None):
    """ Helper to read/ write file objects and delegate 'to do' to passed in function """
    with open(file=path, mode=mode_, newline=newline_) as f:
        return fnc(f)


def from_text(file, *args, **kwargs):
    """ Return file contents as string """
    try:
        return file.read()

    except MemoryError as e:
        return e


def get_config_handler(m, *args, **kwargs):
    """ Execute get-config netconf operation """
    try:
        response = m.get_config(source='running', filter=filter).xml
        data = dumps(parse(str(response), process_namespaces=False), indent=4)
    except RPCError as e:
        data = e._raw
    
    # used for testing only
    print(data)


def connection_handler(fnc,
                    host,
                    username,
                    password,
                    port,
                    *args,
                    **kwargs):
    """ Helper to iterate over objects (i.e. hosts) and delegate 'to do' to passed in function """

    with manager.connect(host=host,
                    port=port,
                    username=username,
                    password=password,
                    timeout=30,
                    hostkey_verify=False,
                    device_params={'name': 'csr'}) as m:
                    
        return fnc(m, *args, **kwargs)


if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    parser.add_argument('--filter', type=str,
                        help="Netconf get-config filter")

    args = parser.parse_args()
    
    host = args.host
    username = input('Username: ') if args.username is None else args.username
    password = getpass() if args.password is None else args.password
    port = args.port
    filter = file_handler(from_text, args.filter) if args.filter else args.filter

    connection_handler(get_config_handler,
                    host,
                    username,
                    password, 
                    port,
                    filter
                    )
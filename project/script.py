"""
 Simple NETCONF operations Python script to be used via command-line.

 Code adapted from example Python script generated by YangExplorer
 when building RPCs:
 Netconf python example by yang-explorer (https://github.com/CiscoDevNet/yang-explorer)
 Python template (https://github.com/CiscoDevNet/yang-explorer/blob/master/server/explorer/templates/pyscript.py)

 Install Python dependencies using requirements.txt on project/ directory:
    > pip install -r requirements.txt

 Running script: (save as example.py)
 
    # Edit running configuration
    > python example.py -a 192.168.1.1 -u netconf -p netconf --port 830 edit-config -config edit_static-ap-tag.xml
    OR
    > python example.py -a 192.168.1.1 edit-config -config edit_static-ap-tag.xml

    # Get full running configuration
    > python example.py -a 192.168.1.1 get-config
    OR
    # Get specific running configuration
    > python example.py -a 192.168.1.1 get-config -filter filter_hostname.xml

    Username and password will be prompted for if not passed directly to CLI

"""


from argparse import ArgumentParser, FileType
from getpass import getpass
from json import decoder, dumps, encoder, load

from ncclient import manager
from ncclient.operations import RPCError
from xmltodict import parse



def connection_handler(fields, *args, **kwargs):
    """
    Handler function to:
        - Connect to device using context manager
        - Provide callback to NETCONF operation handler based on subparser 

    """

    def edit_config_handler(m):
        """ Execute edit-config netconf operation """
        try:
            response = m.edit_config(target='running', error_option='rollback-on-error', config=config).xml
            data = dumps(parse(str(response), process_namespaces=False), indent=4)
        
        except RPCError as e:
            data = e._raw

        # used for testing only
        print(data)


    def get_config_handler(m):
        """ Execute get-config netconf operation """
        try:
            response = m.get_config(source='running', filter=filter).xml
            data = dumps(parse(str(response), process_namespaces=False), indent=4)
        except RPCError as e:
            data = e._raw

        # used for testing only
        print(data)


    # define function mappings
    fnc_mappings = {'edit-config': edit_config_handler,
                    'get-config': get_config_handler}

    # choose corresponding operation handler
    try:
        subparser_name = fields['subparser']
        fnc = fnc_mappings[subparser_name]
    except AttributeError as e:
        return e._raw

    # assign parser and subparser arguments
    host = fields['host']
    username = input('Username: ') if fields['username'] is None else None
    password = getpass() if fields['password'] is None else None
    port = fields['port']
    filter = fields['filter'].read() if fields.get('filter') is not None else None
    config = fields['config'].read() if fields.get('config') is not None else None

    with manager.connect(host=host, port=port, username=username, password=password, timeout=30,
                         hostkey_verify=False, device_params={'name': 'csr'}) as m:

        return fnc(m, *args)


if __name__ == '__main__':

    # parent parser with common arguments
    parser = ArgumentParser(prog='IOS-XE Utils', description='Usage: ')

    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")

    # provide different options via subparsers
    subparsers = parser.add_subparsers(dest='subparser', required=True, help='Description',
                                        metavar='[edit-config|get-config]')

    edit_config_parser = subparsers.add_parser('edit-config',
                                               help='Choose to run edit-config NETCONF operations')
    edit_config_parser.add_argument('-config', type=FileType('rt'), required=True,
                                    help="Input file name used to edit change")
    edit_config_parser.set_defaults(func=connection_handler)

    get_config_parser = subparsers.add_parser('get-config',
                                              help='Choose to run get-config NETCONF operations')
    get_config_parser.add_argument('-filter', type=FileType('rt'),
                                   help="Input file name used to filter get operation")
    get_config_parser.set_defaults(func=connection_handler)

    args = parser.parse_args()

    # access namespace dictionary
    args_dict = vars(args)

    # callback function based on CLI input
    args.func(args_dict)
#!/usr/bin/env python3

import argparse
import getpass
import os


class Server:
    def __init__(self, fqdn='', ip='', port=22):
        """Create the Server instance

        Keyword Arguments:
            fqdn {str} -- Fully Qualified Domain Name for the server
                          (default: {''})
            ip {str} -- IP address for the server (default: {''})
            port {number} -- SSH port for the server (default: {22})
        """
        self.fqdn = fqdn.strip().lower()
        self.ip = ip.strip()
        self.port = int(port)

    @property
    def address(self):
        if self.fqdn:
            return self.fqdn
        return self.ip


class Launcher:
    def __init__(self, servers):
        """Initialize the Launcher instance

        Arguments:
            servers {list} -- List of dicts that define the servers that can
                              be connected to
        """
        # dictionary of servers that can be connected to
        #   listed by nickname, FQDN, and/or IP address
        self.servers = {}
        # list of servers that can be connected to
        #   each server only listed once
        self.displayable = []
        # build the list of Server instances to connect to
        for item in servers:
            displayed = False
            nickname = item.pop('nickname', '').strip().lower()
            server = Server(**item)
            if server.address:
                if nickname != '':
                    self.servers[nickname] = server
                    self.displayable.append(nickname)
                    displayed = True
                if server.fqdn != '':
                    self.servers[server.fqdn] = server
                    if not displayed:
                        self.displayable.append(fqdn)
                        displayed = True
                if server.ip != '':
                    self.servers[server.ip] = server
                    if not displayed:
                        self.displayable.append(ip)

    def connect(self, identifier):
        """Connect to the specified server via SSH

        Arguments:
            identifier {str} -- nickname, FQDN, or IP address of the server
                                to connect to
        """
        try:
            server = self.lookup(identifier)
        except KeyError:
            print('\nThe server you specified could not be found.\n')
        else:
            username = getpass.getuser()
            cmd = 'ssh -p {} {}@{}'.format(server.port, username, server.address)  # NOQA
            os.system(cmd)

    def display_list(self):
        """Displays a list of the available servers"""
        print('\nservers to connect to:')
        for identifier in self.displayable:
            print('  {}'.format(identifier))
        print('\n')

    def lookup(self, keyword):
        """Lookup the server by keyword (nickname, FQDN, or IP address)

        Arguments:
            keyword {str} -- nickname, FQDN, or IP address of the server

        Raises:
            KeyError -- Raised when no server can be found by the keyword

        Returns:
            {dict} -- Dict of server information
        """
        keyword = keyword.strip().lower()
        return self.servers[keyword]

    def tunnel(self, identifier):
        """Establish an SSH tunnel to the specified server

        Arguments:
            identifier {str} -- nickname, FQDN, or IP address of the server
                                to connect to
        """
        ### TODO: implement this
        print('This feature is not available at this time.')


if __name__ == '__main__':
    try:
        from servers import *
    except ImportError:
        print('\nNo servers defined!')
        print('Copy servers.dist to servers.py and '
              'edit the file to fix this problem.\n')

    launcher = Launcher()
    parser = argparse.ArgumentParser(
        description='Launch SSH connections and tunnels to other servers.'
    )
    parser.add_argument(
        'server',
        nargs='?',
        default='',
        help='nickname, FQDN, or IP address of the server to connect to'
    )
    parser.add_argument(
        '-l', '--list',
        dest='list_servers',
        action='store_true',
        help='list the available servers to connect to'
    )
    args = parser.parse_args()
    if args.server == '' or args.list_servers:
        parser.print_help()
        launcher.display_list()
    else:
        launcher.connect(args.server)

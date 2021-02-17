#!/usr/bin/env python3

import argparse
import getpass
import os


class Host:
    def __init__(self, fqdn='', ip='', port=22):
        """Create the Host instance

        Keyword Arguments:
            fqdn {str} -- Fully Qualified Domain Name for the host
                          (default: {''})
            ip {str} -- IP address for the host (default: {''})
            port {number} -- SSH port for the host (default: {22})
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
    def __init__(self, hosts):
        """Initialize the Launcher instance

        Arguments:
            hosts {list} -- List of dicts that define the hosts that can
                              be connected to
        """
        # dictionary of hosts that can be connected to
        #   listed by nickname, FQDN, and/or IP address
        self.hosts = {}
        # list of hosts that can be connected to
        #   each host only listed once
        self.displayable = []
        # build the list of host instances to connect to
        for item in hosts:
            displayed = False
            nickname = item.pop('nickname', '').strip().lower()
            host = Host(**item)
            if host.address:
                if nickname != '':
                    self.hosts[nickname] = host
                    self.displayable.append(nickname)
                    displayed = True
                if host.fqdn != '':
                    self.hosts[host.fqdn] = host
                    if not displayed:
                        self.displayable.append(host.fqdn)
                        displayed = True
                if host.ip != '':
                    self.hosts[host.ip] = host
                    if not displayed:
                        self.displayable.append(host.ip)

    def connect(self, identifier):
        """Connect to the specified host via SSH

        Arguments:
            identifier {str} -- nickname, FQDN, or IP address of the host
                                to connect to
        """
        try:
            host = self.lookup(identifier)
        except KeyError:
            print('\nThe host you specified could not be found.\n')
        else:
            username = getpass.getuser()
            cmd = 'ssh -p {} {}@{}'.format(host.port, username, host.address)  # NOQA
            os.system(cmd)

    def display_list(self):
        """Displays a list of the available hosts"""
        print('\nhosts to connect to:')
        for identifier in self.displayable:
            print('  {}'.format(identifier))
        print('\n')

    def lookup(self, keyword):
        """Lookup the host by keyword (nickname, FQDN, or IP address)

        Arguments:
            keyword {str} -- nickname, FQDN, or IP address of the host

        Raises:
            KeyError -- Raised when no host can be found by the keyword

        Returns:
            {dict} -- Dict of host information
        """
        keyword = keyword.strip().lower()
        return self.hosts[keyword]

    def tunnel(self, identifier):
        """Establish an SSH tunnel to the specified host

        Arguments:
            identifier {str} -- nickname, FQDN, or IP address of the host
                                to connect to
        """
        ### TODO: implement this
        raise NotImplemented('This feature is not available at this time.')


if __name__ == '__main__':
    try:
        from hosts import HOSTS
    except ImportError:
        try:
            # include for backwards compatibility
            from servers import SERVERS
        except ImportError:
            print('\nNo hosts defined!')
            print('Copy hosts.dist to hosts.py and '
                  'edit the file to fix this problem.\n')
        else:
            HOSTS = SERVERS

    launcher = Launcher(HOSTS)
    parser = argparse.ArgumentParser(
        description='Launch SSH connections and tunnels to other hosts.'
    )
    parser.add_argument(
        'host',
        nargs='?',
        default='',
        help='nickname, FQDN, or IP address of the host to connect to'
    )
    parser.add_argument(
        '-l', '--list',
        dest='list_hosts',
        action='store_true',
        help='list the available hosts to connect to'
    )
    args = parser.parse_args()
    if args.host == '' or args.list_hosts:
        parser.print_help()
        launcher.display_list()
    else:
        launcher.connect(args.host)

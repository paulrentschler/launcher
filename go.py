#!/usr/bin/env python

import argparse, getpass, os


class Servers:
    def __init__(self):
        self.servers = {}
        self.displayable = []
        for server in SERVERS:
            displayed = False
            if (('fqdn' in server.keys() and server['fqdn'] != '') or
                ('ip' in server.keys() and server['ip'] != '')):
                if 'port' not in server.keys():
                    server['port'] = 22
                if 'nickname' in server.keys() and server['nickname'] != '':
                    self.servers[server['nickname'].strip().lower()] = server
                    self.displayable.append(server['nickname'].strip().lower())
                    displayed = True
                if 'fqdn' in server.keys() and server['fqdn'] != '':
                    self.servers[server['fqdn'].strip().lower()] = server
                    if not displayed:
                        self.displayable.append(server['fqdn'].strip().lower())
                        displayed = True
                if 'ip' in server.keys() and server['ip'] != '':
                    self.servers[server['ip'].strip()] = server
                    if not displayed:
                        self.displayable.append(server['ip'].strip().lower())
                        displayed = True


    def connect(self, identifier):
        """
        Connects to the specified server via SSH. 'identifier' is either the
        nickname, FQDN, or IP address of the server to connect to.
        """
        server = self.lookup(identifier)
        if server is not None:
            if 'ip' in server.keys() and server['ip'] != '':
                address = server['ip']
            elif 'fqdn' in server.keys() and server['fqdn'] != '':
                address = server['fqdn']
            if address:
                username = getpass.getuser()
                cmd = 'ssh -p %s %s@%s' % (server['port'], username, address)
                os.system(cmd)
            else:
                print "\nNo server address to connect to.\n"
        else:
            print "\nThe server you specified could not be found.\n"


    def display_list(self):
        """
        Displays a list of the available servers for the user to pick from.
        """
        print "\nservers to connect to:"
        for identifier in self.displayable:
            print "  %s" % identifier
        print ""


    def lookup(self, keyword):
        """
        Looks up the server based on the keyword (nickname, FQDN, or IP address)
        and returns the entry.
        """
        keyword = keyword.strip().lower()
        if keyword in self.servers.keys():
            return self.servers[keyword]
        return None


    def tunnel(self, identifier):
        """
        Establishes an SSH tunnel tot he specified server. 'identifier' is
        either the nickname, FQDN, or IP address of the server to connect to.
        """
        ### TODO: implement this
        print "This feature is not available at this time."


if __name__ == '__main__':
    try:
        from servers import *
    except ImportError:
        print "\nNo servers defined!"
        print "Copy servers.dist to servers.py and edit the file to fix this problem.\n"

    launcher = Servers()
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



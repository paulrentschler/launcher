# launcher

Establish SSH connections and tunnels from the command line by referencing servers from a pre-configured list.

## Installation

1. Clone the repository somewhere on your computer.
1. Symlink the `go.py` file to `go` in a directory within your path.


## Define the servers to connect to

Copy the included `servers.dist` file to `servers.py` (excluded from the repo) and then edit that file to specify all of the servers you want to be able to connect to.

Each entry must specify the port and at least a fully qualified domain name (FQDN) or an IP address. Both the FQDN and IP address can be specified and the FQDN takes precedence.

A nickname can also be specified to be referenced when calling the `go.py` script to make it easier to reference the server.


## Bugs

Report bugs via a GitHub issue:
https://github.com/paulrentschler/launcher/issues


## Contributions

Contributions are welcome as pull requests.


## License

MIT (see LICENSE for details)


## Author

Created by Paul Rentschler in 2014

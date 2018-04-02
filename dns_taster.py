import sys
import click
from dns import resolver, rdatatype
from validators.domain import domain as valid_domain

from DNSTaster import DNSTaster 




@click.command()
@click.option('-d', '--domain', prompt=' # Please enter Domain name to test', help='Please enter a FQDN to taste for poison.')
@click.option('-v', '--verbose', count=True)
def taste(domain, verbose):
    """
    Compare known public DNS server zones for the given domain
    to the regitrar provided DNS server zone to try and find DNS
    cache poisoning attack.

    Public DNS server lists was taken from : https://wiki.ipfire.org/dns/public-servers
    """

    #click.clear()

    # First make sure we have a domain
    try:
        taster  = DNSTaster(domain)
    except ValueError():
        sys.exit(' ! Could not validate the domain.')

    """

    click.echo(' #  Thank you. Gonna taste some DNS records for {}'.format(domain))
    #Now we get the name server, clean them up and save in a list.
    name_servers = 
    

    #  If we didn't get any authretative name servers 
    if len(name_servers)<1:
        sys.exit(' E Could not get any primary name servers ')


    click.echo(' #  Got authoritative name servers. Constructing base image.')
    if verbose:
        click.echo(' #  Name servers found:')
        click.echo('\n'.join(['    * {}'.format(ns) for ns in name_servers]))

    """












if __name__ == '__main__':
    taste()

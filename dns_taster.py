import sys
import click
import dns.resolver


from validators.domain import domain as valid_domain


@click.command()
@click.option('-d', '--domain', prompt='Domain name to test', help='Please enter a FQDN to taste for poison.')
@click.option('-v', '--verbose', count=True)

def taste(domain, verbose):
    """
    Compare known public DNS server zones for the given domain
    to the regitrar provided DNS server zone to try and find DNS
    cache poisoning attack.

    Public DNS server lists was taken from : https://wiki.ipfire.org/dns/public-servers
    """


    # First make sure we have a domain
    if valid_domain(domain):
        click.echo(' * Thank you. Gonna taste some DNS records for {}'.format(domain))
    else:
        sys.exit(' E This does not seem to be a domain.')


    #Now we get the name server
    name_servers = []
    for rdata in dns.resolver.query(domain, 'ns'):
        name_servers.append(str(rdata)[:-1])


    click.echo(name_servers)

if __name__ == '__main__':
    taste()

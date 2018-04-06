import sys, csv, pprint
import click
from dns import resolver, rdatatype
from dns.exception import  DNSException

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

    click.clear()
    click.echo(' '+'#'*60)
    click.echo(' #  Initiating DNS Taster for {}.'.format(domain))
    try:
        taster  = DNSTaster(domain)
    except DNSException as e:
        sys.exit(' ! Something went wrong: {}'.format(e))


    if verbose > 0:
        click.echo(' #  Validated {}.'.format(taster.domain))
        click.echo(' #  Found authoritative name servers.'.format(taster.domain))
    if verbose > 1:
        for ns in taster.name_servers:
            click.echo(' #     {}'.format(ns))
    if verbose > 0:
        click.echo(' #  Generated DNS base line.')
    if verbose > 1:
        for record in taster.baseline:
            print(' #    ',repr(record)[1:-1])


    results = {
        'Tasted Good':0,
        'Tasted Bad':0,
        'No Rules To Taste':0
    }

    click.echo(' '+'#'*60)
    click.echo(' #  Gonna taste some DNS records for {}.'.format(domain))

    with open('dns_server_list.csv', 'r') as ns_file:
        ns_list = csv.reader(ns_file)
        for ns in ns_list:
            if verbose > 1: click.echo(' #  Tasting {} ({}).'.format(ns[0],ns[1]))
            taste, funny_tasting_record_set = taster.taste(ns[1])

            if len(funny_tasting_record_set)==0:
                click.echo(' !    Name server {} did not return a rule set, skipping.'.format(ns[0]))
                results["No Rules To Taste"] += 1
                continue

            if not taste:
                click.echo(' !  Tasted something funny with {}.'.format(ns[0]))
                results["Tasted Bad"] += 1

                if verbose > 2:
                    click.echo(' !  Funny tasting records:')
                    for record in funny_tasting_record_set:
                        print(' !    ',repr(record)[1:-1])

                diff = taster.baseline.difference(funny_tasting_record_set)
                click.echo(' !  Diff from baseline:')
                for record in diff:
                    print(' !    ',repr(record)[1:-1])
            else:
                if verbose > 0: click.echo(' #    {} tasted fine.'.format(ns[0]))
                results["Tasted Good"] += 1


    click.echo(' '+'#'*60)
    click.echo(' # Taste test results:')
    for r in results:
        click.echo(' # {} Name server {}'.format(results[r],r))
    click.echo(' '+'#'*60)


if __name__ == '__main__':
    taste()

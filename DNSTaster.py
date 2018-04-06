import sys, socket
import click

from dns import resolver, rdatatype
from dns.exception import  DNSException
from dns.resolver import NoAnswer, NoMetaqueries, NoNameservers, Timeout
from validators.domain import domain as valid_domain




class DNSTaster():

    def __init__(self, domain):

        self.resolver = resolver.Resolver()
        self.resolver.timeout = 1
        self.resolver.lifetime = 1


        #Validate the domain.
        if valid_domain(domain):
            self.domain = domain
        else:
            raise DNSException('Could not validate domain')

        # Get name server
        self.name_servers = self._get_name_servers()

        if len(self.name_servers)<1:
            raise DNSException('Could not get authoritative name servers.')

        # Get the DNS baseline
        self.baseline = self._get_baseline()


    def taste(self,name_server):
        """
        Compare the available records for the domain from the provided
        name server to the base line. Returns True or False and the record set.
        """
        dish = self._get_record_set(name_server)
        if  dish == self.baseline:
            return True, dish
        else:
            return False, dish

    def _get_name_servers(self, ns = '9.9.9.9'):
        """
        Get the primary name servers to establish a baseline using a trusted
        name servers. Default is Quad9 (ibm)

        return a list of string.
        """
        self.resolver.nameservers=[ns]

        name_servers = []
        [name_servers.append(rdata.to_text()) for rdata in self.resolver.query(self.domain, 'NS')]

        return name_servers


    def _get_record_set(self,name_server):
        """
        Return a list of dictionaries representing all the supported records
        for the provided domain from the provided name server 
        """
        self.resolver.nameservers=[socket.gethostbyname(name_server)]
        records = set()
        for records_type in rdatatype._by_text.keys():
            try:
                answesrs = self.resolver.query(self.domain, records_type)
            except (NoAnswer, NoMetaqueries, NoNameservers, Timeout) as e:
                continue

            for rdata in answesrs:
                records.add(rdata)
        return records

    def _get_baseline(self):
        """
        Create a baseline records set
        """
        res = {}
        base = False
        for name_server in self.name_servers:
            if base:
                if set(self._get_record_set(name_server)) == base:
                    continue
                else:
                    raise DNSException('Authoritative Name Servers do not agree.')
            else:
                base = self._get_record_set(name_server)
        return base

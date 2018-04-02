import sys, socket
import click

from dns import resolver, rdatatype
from dns.exception import  DNSException
from dns.resolver import NoAnswer, NoMetaqueries
from validators.domain import domain as valid_domain




class DNSTaster():

    def __init__(self, domain):

        self.resolver = resolver.Resolver()

        #Validate the domain.
        if valid_domain(domain):
            self.domain = domain
        else:
            raise ValueError('Could not validate domain')

        # Get name server
        self.name_servers = self._get_name_servers()

        if len(self.name_servers)<1:
            raise ValueError('Could not get authoritative name servers.')
        self.baseline = self._get_baseline()


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
        records = []
        for records_type in rdatatype._by_text.keys():
            try:
                answesrs = self.resolver.query(self.domain, records_type)
            except NoAnswer:
                continue

            for rdata in answesrs:
                records.append(rdata.to_text())
        return records

    def _get_baseline(self):
        """
        Create a baseline records set
        """
        res = {}
        for name_server in self.name_servers:
            res[name_server] = self._get_record_set(name_server)

        print(res)

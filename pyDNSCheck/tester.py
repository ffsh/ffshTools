#!python3
"""
Checks if dns servers in the Freifunk Südholstein Network are consistent
"""
import json
import dns.resolver
import dnsresult
from terminaltables import AsciiTable

class DnsChecker():
    """Query each server defined in self.dns_resolvers for each domain in self.targets"""
    def querry(self, resolvers, targets):
        """performs a nice querry"""
        resolver = dns.resolver.Resolver()
        test_resolvers = {}
        dnsresults = dnsresult.DNSResult()
        # Convert DNS Server list to ip -> name dict
        for name, value in sorted(resolvers["Servers"].items()):
            if value["active"] is True:
                test_resolvers[value["IPv6"]] = name

        # For each domain in targets query each dns server
        for [domain, record] in sorted(targets["Targets"]):
            for name in sorted(test_resolvers):
                resolver.nameservers = [name]
                try:
                    response = resolver.resolve(domain, record)
                    # get the query result
                    for ip_address in response:
                        dnsresults.add(domain, test_resolvers[name], str(ip_address))

                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
                    # No answer or no entry
                    dnsresults.add(domain, test_resolvers[name], "None")
        return dnsresults.get_all()

    def display (self, result):
        """display all the results"""
        table = [
            ["Domain", "IP", "Hosts"]
        ]
        for domain, value in result.items():
            for ip_address, hosts in value.items():
                if ip_address != "None":
                    table.append([domain, ip_address, str(hosts)])
                else:
                    table.append([domain, '\033[0;31m'+ip_address+'\033[0m', str(hosts)])
        ascii_table = AsciiTable(table)
        print(ascii_table.table)



def main():
    """init all the things"""
    with open("targets.json") as file:
        targets = json.load(file)

    with open("dns-resolvers.json") as file:
        resolvers = json.load(file)

    checker = DnsChecker()
    result = checker.querry(resolvers, targets)
    checker.display(result)

if __name__ == '__main__':
    main()

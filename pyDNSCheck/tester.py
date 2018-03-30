#!/usr/bin/python3
"""
Checks if dns servers in the Freifunk Südholstein Network are consistent
"""
import dns.resolver
import json

class DNS_checker():
    """Query each server defined in self.dns_resolvers for each domain in self.targets"""
    def querry(self, resolvers, targets):
        resolver = dns.resolver.Resolver()
        test_resolvers = {}
        for name, value in sorted(resolvers["Servers"].items()):
            if value["active"] is True:
                test_resolvers[value["IPv4"]] = name
        resolver.nameservers = [name for name in test_resolvers]


        for domain in sorted(targets["Targets"]):
            try:
                response = resolver.query(domain, "A")
            except dns.resolver.NoAnswer:
                pass

            for rdata in response:
                print(rdata)

        if self.consistent():
            return True
        return False

    def results(self):
        """prints pretty results"""
        pass
    def consistent(self):
        return True


def main():
    """init all the things"""
    with open("targets.json") as file:
        targets = json.load(file)

    with open("dns-resolvers.json") as file:
        resolvers = json.load(file)
    #print(targets)
    #print(resolvers)
    checker = DNS_checker()
    checker.querry(resolvers, targets)

if __name__ == '__main__':
    main()

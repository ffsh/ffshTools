#!/usr/bin/python3
"""
Checks if dns servers in the Freifunk Südholstein Network are consistent
"""
import json
import dns.resolver
import collections

class DnsChecker():
    """Query each server defined in self.dns_resolvers for each domain in self.targets"""
    def querry(self, resolvers, targets):
        """performs a nice querry"""
        resolver = dns.resolver.Resolver()
        results = {}
        test_resolvers = {}
        for name, value in sorted(resolvers["Servers"].items()):
            if value["active"] is True:
                test_resolvers[value["IPv6"]] = name
        for [domain, record] in sorted(targets["Targets"]):
            results[domain] = {}
            results[domain][record] = {}
            #print("Testing Domain {}:".format(domain))
            for name in sorted(test_resolvers):
                resolver.nameservers = [name]
                try:
                    response = resolver.query(domain, record)
                    for rdata in response:
                        results[domain][record][test_resolvers[name]] = str(rdata)
                        #print(test_resolvers[name], rdata, sep=": ")
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    results[domain][record][test_resolvers[name]] = "None"
                    #print(test_resolvers[name], "None")
        with open("something.json", "w") as filep:
            #print(results)
            json.dump(results, filep, indent=4)

        self.consistent(results)

    def results(self):
        """prints pretty results"""
        pass
    def consistent(self, results):
        """will test for consistent stuff"""
        for key, value in sorted(results.items()):
            print(key)
            for key1, value1 in sorted(results[key].items()):
                value_to_key = collections.defaultdict(list)
                for key2, value2 in sorted(results[key][key1].items()):
                    value_to_key[value2].append(key2)
                for key3, value3 in value_to_key.items():
                    #if len(value3) == 5:
                    #    print("ok")
                    #else:
                        print(value3, key3, sep=": ")


def main():
    """init all the things"""
    with open("targets.json") as file:
        targets = json.load(file)

    with open("dns-resolvers.json") as file:
        resolvers = json.load(file)
    #print(targets)
    #print(resolvers)
    checker = DnsChecker()
    checker.querry(resolvers, targets)

if __name__ == '__main__':
    main()

#!/usr/bin/python3
""" Holds DNS Resulsts """
import pprint
class DNSResult():
    """ Holds DNS Resulsts """

    def __init__(self):
        #self.results = {
        #   "map.freifunk-suedholstein.de": {
        #        "1.2.3.4": ["viehbach", "hopfenbach"]
        #    }
        #}
        self.results = {}

    def add(self, domain, hostname, ip_address):
        """ add a entry to the dns results """
        if domain in self.results.keys():
            # domain exists
            if ip_address in self.results[domain].keys():
                # ip exists
                temp = self.results[domain][ip_address]
                temp.append(hostname)
                self.results[domain][ip_address] = temp
            else:
                # ip does not exist create new ip_address entry
                self.results[domain][ip_address] = [hostname]
        else:
            # domain does not exist create new domain
            temp = {}
            temp[ip_address] = [hostname]
            self.results[domain] = temp

    def get_all(self):
        """resturns all results"""
        if __name__ == '__main__':
            pprint.pprint(self.results)
        return self.results

def main():
    """just for testing this module"""
    dns_results = DNSResult()
    dns_results.add("map.freifunk-suedholstein.de", "beste", "1.2.3.4")
    dns_results.add("map.freifunk-suedholstein.de", "barnitz", "1.2.3.5")
    dns_results.add("map.freifunk-stormarn.de", "barnitz", "1.2.3.6")
    dns_results.add("map.freifunk-stormarn.de", "trave", "1.2.3.6")

    dns_results.get_all()
if __name__ == '__main__':
    main()

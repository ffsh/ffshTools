#!/usr/bin/python3
"""Adapter batctl influxdb"""
import subprocess
import argparse
import time
import re
# import pprint
import unicodedata
from influxdb import InfluxDBClient

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-host", metavar="Host", dest="host",
                    help="Host Name",
                    required=True)
ARGS = PARSER.parse_args()

class Batman():
    """does batman stuff"""
    def __init__(self, host, timestamp):
        self.batman = {
            "measurement": "batman",
            "tags": {
                "host": host
            },
            "time": timestamp,
            "fields": {}
            }
    @staticmethod
    def remove_control_characters(string):
        """remove control_characters"""
        return "".join(ch for ch in string if unicodedata.category(ch)[0] != "C")

    def pase(self):
        """parses output of batctl s"""
        cmd = subprocess.Popen('batctl s', shell=True, stdout=subprocess.PIPE)
        pattern = re.compile("(.+): ([0-9]+)")
        for line in cmd.stdout:
            line = self.remove_control_characters(line.decode("utf-8"))
            result = re.search(pattern, line)
            self.batman["fields"][result.group(1)] = str(result.group(2))

    def send(self):
        """send data to infuxdb"""
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.batman)
        json_body = [].append(self.batman)
        client = InfluxDBClient('localhost', 8086, '', '', 'ffsh')
        client.write_points(json_body)


def main():
    """start all the things"""
    batman = Batman(ARGS.host, int(time.time()))
    batman.pase()
    batman.send()

if __name__ == '__main__':
    main()

#!/usr/bin/python3
"""Adapter batctl influxdb"""
import subprocess
import argparse
from datetime import datetime
import re
import pprint
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
            "tags": {
                "host": str(host)
                },
            "points": [
                {
                    "measurement": "batman",
                    "fields": {
                        },
                    "time": str(timestamp),
                }
            ]
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
            self.batman["points"][0]["fields"][result.group(1)] = str(result.group(2))

    def send(self):
        """send data to infuxdb"""
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.batman)
        client = InfluxDBClient('localhost', 8086, '', '', 'ffsh')
        client.write(self.batman)


def main():
    """start all the things"""
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    batman = Batman(ARGS.host, current_time)
    batman.pase()
    batman.send()

if __name__ == '__main__':
    main()

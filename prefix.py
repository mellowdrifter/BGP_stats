#!/usr/bin/python

import subprocess
import re

class prefixInfo:
    'Class to hold prefix and associated information'

    def __init__(self, prefix, mask):
        self.prefix = prefix
        self.mask = mask
        self.origin = ""
        self.aspath = []
        self.communities = []
        self.sourceas = ""

    def setSourceAS(self):
        """Source AS will be the last AS in the list presented"""
        self.sourceas = self.aspath[-1]

    def setTransitAS(self):
        """Transit AS is the list of AS's this prefix has passed
        through, exluding the first and last AS"""
        self.transitas = self.aspath[1:-1]

        

    
def getSubnets(family):
    subnets = []
    v6Address = ('[0-9a-f]{0,4}:([0-9a-f]{0,4}:){0,6}[0-9a-f]{0,4}:{1,2}/\d{1,3}')
    if family == 4:
        with open (r"C:\Users\mellowd\Desktop\ipv4.txt") as f:
            lines = f.readlines()
    elif family == 6:
        with open (r"C:\Users\mellowd\Desktop\table6.txt") as f:
            routes = f.readlines()
    else:
        return False
    for route in routes:
        "First find the IPv6 prefix"
        address = re.search(v6Address, route)
        if address:
            "Split it up so we can get the address and mask separately"
            addressMask = address.group().split("/")

            "Create a new prefix object"
            prefix = prefixInfo(addressMask[0], addressMask[1])

            "Add this prefix to our list of prefixInfos"
            subnets.append(prefix)

    return subnets



if __name__ == "__main__":
    ipv6 = getSubnets(6)
    print ('ipv6 = {}, and length is {}'.format(ipv6, len(ipv6)))
    for ip in ipv6:
        print ('the address is = {} and the mask is {}'.format(ip.prefix, ip.mask))
    input("Press Enter to continue...")


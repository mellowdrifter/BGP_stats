#!/usr/bin/python

import subprocess
import re

class Prefix:
    'Class to hold prefix and associated information'

    def __init__(self, prefix, mask):
        self.prefix = prefix
        self.mask = mask
        self.origin = None
        self.med = None
        self.aspath = None
        self.sourceas = 0
        self.atomicAgg = None
        self.aggregatorAS = None
        self.aggregatorRID = None
        self.largeCommunity = False

    def setSourceAS(self):
        """Source AS will be the last AS in the list presented"""
        self.sourceas = int(self.aspath[-1])

    def setTransitAS(self):
        """Transit AS is the list of AS's this prefix has passed
        through, exluding the first and last AS"""
        self.transitas = self.aspath[1:-1]
    
    def is32bitASN(self):
        """If source ASN is bigger than 65535, it's 32bit"""
        return self.sourceas > 65535
    
    def hasLargeCommunity(self):
        """Returns True if prefix has an attached large community.
        False otherwise"""
        return self.largeCommunity

     
def getPrefix(fullPrefix, family):
    "Split it up so we can get the address and mask separately"
    addressMask = fullPrefix.split("/")

    "Create a new prefix object"
    prefix = Prefix(addressMask[0], addressMask[1])

    return prefix

def getAttributes(info):
    """Pull out all the prefix attributes so we can tie them to the prefix"""
    info = info.splitlines()

    origin = ""
    aspath = []
    largeComm = False
    for line in info:
        line = line.strip()
        if line.startswith("BGP.origin:"):
            if "IGP" in line:
                origin = "IGP"
            elif "Incomplete" in line:
                origin = "Incomplete"
            else:
                origin = "EGP"
        if line.startswith("BGP.as_path:"):
            """Need to handle as-sets"""
            aspath = line[13:].split()
        if line.startswith("BGP.large_community:"):
            largeComm = True
        

    return origin, aspath, largeComm
    
    


def splitPrefixes(family):
    """Split the output so we can first get the actual address.
    A list will be returned. The first item is the address, the
    second item it's attributes. Third item is an address, fourth
    attributes. And so on
    """
    v4regex = '((?:\d{1,3}.){3}0\/\d{1,2})'
    v6regex = '([0-9a-f]{1,4}:(?:[0-9a-f]{1,4}:){0,6}(?:[0-9a-f]{1,4}:){0,1}:\/\d{1,3})'
    if family == 4:
        with open (r"C:\Users\mellowd\Desktop\ipv4.txt") as f:
        #with open (r"C:\Users\mellowd\Desktop\table4.txt") as f:
            routes = f.read()
        routes = re.split(v4regex, routes)
    elif family == 6:
        #with open (r"C:\Users\mellowd\Desktop\ipv6.txt") as f:
        with open (r"C:\Users\mellowd\Desktop\table6.txt") as f:
            routes = f.read()
        routes = re.split(v6regex, routes)
    return routes[1:]
        
            
if __name__ == "__main__":
    v4 = splitPrefixes(4)
    v6 = splitPrefixes(6)
    v4prefixes = []
    v6prefixes = []
    for i in range(len(v4)):
        if i % 2 == 0:
            newPrefix = getPrefix(v4[i], 4)
        else:
            newPrefix.origin, newPrefix.aspath, newPrefix.largeCommunity = getAttributes(v4[i])
            v4prefixes.append(newPrefix)
    for i in range(len(v6)):
        if i % 2 == 0:
            newPrefix = getPrefix(v6[i], 6)
        else:
            newPrefix.origin, newPrefix.aspath, newPrefix.largeCommunity = getAttributes(v6[i])
            v6prefixes.append(newPrefix)

    for prefix in v4prefixes:
        prefix.setSourceAS()
        prefix.setTransitAS()
        print(prefix.__dict__)

    for prefix in v6prefixes:
        prefix.setSourceAS()
        prefix.setTransitAS()
        print(prefix.__dict__)

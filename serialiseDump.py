#!/usr/bin/python

from prefixClass import Prefix
import pickle
import re

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
        with open ("ipv4.txt") as f:
            routes = f.read()
        routes = re.split(v4regex, routes)
    elif family == 6:
        with open ("ipv6.txt") as f:
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
        prefix.findASSet()
        prefix.setSourceAS()
        prefix.setTransitAS()
        #print(prefix.__dict__)
    with open("ipv4.pickle","wb") as f:
        pickle.dump(v4prefixes, f)
    with open("ipv4.pickle","rb") as f:
        v4test = pickle.load(f)
    for prefix in v4test:
        print(prefix.__dict__)

    for prefix in v6prefixes:
        prefix.findASSet()
        prefix.setSourceAS()
        prefix.setTransitAS()
        #print(prefix.__dict__)
    with open("ipv6.pickle","wb") as f:
        pickle.dump(v6prefixes, f)
        

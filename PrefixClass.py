class Prefix:
    'Class to hold prefix and associated information'

    def __init__(self, prefix, mask):
        self.prefix = prefix
        self.mask = mask
        self.origin = None
        self.med = None
        self.aspath = None
        self.hasAsSet = False
        self.sourceas = 0
        self.atomicAgg = None
        self.aggregatorAS = None
        self.aggregatorRID = None
        self.largeCommunity = False
        self.firstOctet = None
        self.family = None

    def setASPath(self, aspath):
        """Set the AS path, remove the AS-SET if there.
        Then set the source and transit AS numbers.
        Need all paths to be integers"""
        self.aspath = aspath
        self.findASSet()
        self.aspath = [int(i) for i in self.aspath]
        self.setSourceAS()
        self.setTransitAS()

    def getASPath(self):
        """Return the as-path"""
        return self.aspath
    
    def setOrigin(self, origin):
        """Set protocol origin"""
        self.origin = origin

    def getOrigin(self):
        """Return the protocol origin"""
        return self.origin
    
    def setPrefix(self):
        """Set the prefix family. Then work out the first octect"""
        if ":" in self.getPrefix():
            self.setFamily(6)
        else:
            self.setFamily(4)
        self.setFirstOctect()
    
    def getPrefix(self):
        """Returns the prefix"""
        return self.prefix

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

    def setLargeCommunity(self, exists):
        """Sets the Large community bit if it exists"""
        self.largeCommunity = exists
    
    def findASSet(self):
        """ Find AS Set information. Don't care about the AS's themselves.
        So remove them and set hasAsSet"""
        for i in range(len(self.aspath)):
            if "{" in self.aspath[i]:
                self.aspath = self.aspath[:i]
                self.hasAsSet = True
                break
    
    def setFirstOctect(self):
        """Set's the major /8 network for IPv4 prefixes"""
        if self.getFamily() == 4:
            self.firstOctet = int(self.getPrefix().split(".")[0])
    
    def getFirstOctet(self):
        """Return the first octet"""
        return self.firstOctet

    def inMajorNetwork(self, network):
        """Returns True if prefix is in the major network provided"""
        return self.getFirstOctet() == network
    
    def setFamily(self, family):
        """Set's the address family of the prefix"""
        self.family = family

    def getFamily(self):
        """Returns the address family"""
        return self.family

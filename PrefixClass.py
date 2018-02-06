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
    
    def findASSet(self):
        """ Find AS Set information. Don't care about the AS's themselves.
        So remove them as set hasAsSet"""
        for i in range(len(self.aspath)):
            if "{" in self.aspath[i]:
                self.aspath = self.aspath[:i]
                self.hasAsSet = True
                break

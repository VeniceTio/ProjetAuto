from State import *


class Link:
    def __init__(self, pFrom: State, pTo: State, pTag):
        self.origin = pFrom
        self.destination = pTo
        self.tag = []
        self.tag.append(pTag)

    def addTag(self, pTag):
        self.tag.append(pTag)
        self.origin.addLink(pTag,self.origin)
    
    def delTag(self, pTag):
        self.tag.remove(pTag)
        self.origin.dellLink(pTag,self.origin)

    def __str__(self):
        return "go from -{}- to -{}- with -{}".format(self.origin.id, self.destination.id, self.tag)

    def __add__(self, other):
        not_inTpl = set(self.tag) - set(other.tag)
        self.tag = list(self.tag) + list(not_inTpl)

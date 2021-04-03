from State import *


class Link:
    def __init__(self, pFrom: State, pTo: State, pTag):
        self.origin = pFrom
        self.destination = pTo
        self.tag = []
        self.tag.append(pTag)

    def addTag(self, pTag):
        self.tag.append(pTag)
        self.origin.addLink(pTag, self.origin)

    def delTag(self, pTag):
        self.tag.remove(pTag)
        self.origin.dellLink(pTag, self.destination)

    def changeDest(self, newdestination):
        self.origin.updatedestination(self.destination.id, newdestination.id)
        self.destination = newdestination

    def changeOrigin(self, newOrigin):

        self.origin = newOrigin

    def __str__(self):
        return "go from -{}- to -{}- with -{}".format(self.origin.id, self.destination.id, self.tag)

    def add(self, other):
        not_inTpl = set(self.tag) - set(other.tag)
        self.tag = list(not_inTpl) + other.tag


from State import *


class Link:
    def __init__(self, pFrom: State, pTo: State, pTag):
        self.origin = pFrom
        self.destination = pTo
        self.tag = []
        self.tag.append(pTag)

    def addTag(self, pTag):
        self.tag.append(pTag)

    def __str__(self):
        return "go from -{}- to -{}- with -{}".format(self.origin.id, self.destination.id, self.tag)

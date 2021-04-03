
class State:
    def __init__(self, pid=-1, pAlphabet=[]):
        self.id = pid
        self.nbLink = 0
        self.final = False
        self.initial = False
        self.next = {}
        for e in pAlphabet:
            self.next[e] = []

    def setFinal(self, pFinal):
        self.final = pFinal

    def setInitial(self, pInitial):
        self.initial = pInitial

    def isFinal(self):
        return self.final

    def isInitial(self):
        return self.initial

    def addLink(self, pTag, pState):
        self.next[pTag].append(pState.id)

    def dellLink(self, pTag, pState):
        self.next[pTag].remove(pState.id)

    def clear(self):
        self.nbLink = 0
        self.final = False
        self.initial = False
        self.next = {}

    def __eq__(self, other):
        return other.id in self.next["#"] and self.id in other.next["#"]

    def xfusion(self, other):
        for i in range(len(self.next)):
            if self.next[i] != other.next[i]:
                not_inTpl = set(self.next[i]) - set(other.next[i])
                self.next[i] = list(self.next[i]) + list(not_inTpl)
        other.clear()

    def __str__(self):
        desc = " State : {}\n    - number of link : {}".format(self.id, self.nbLink)
        if self.final:
            desc += "\n    - final State"
        if self.initial:
            desc += "\n    - initial State"
        desc += "\n    - connected to : " + str(self.next)
        return desc


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
        result = True
        for value in other.next.values():
            if self.id in value:
                result = False
        for value in self.next.values():
            if other.id in value:
                result = False
        return (other.id in self.next["#"] and self.id in other.next["#"]) or result

    def xfusion(self, other):
        for i in self.next.keys():
            if self.next[i] != other.next[i]:
                not_inTpl = set(self.next[i]) - set(other.next[i])
                self.next[i] = list(self.next[i]) + list(not_inTpl)
        if self.id in self.next["#"]:
            self.next["#"].remove(self.id)

    def updatedestination(self, pfrom, pto):
        for key in self.next.keys():
            list_replace(self.next[key], pfrom, pto)

    def __str__(self):
        desc = " State : {}\n    - number of link : {}".format(self.id, self.nbLink)
        if self.final:
            desc += "\n    - final State"
        if self.initial:
            desc += "\n    - initial State"
        desc += "\n    - connected to : " + str(self.next)
        return desc


def list_replace(lst, old=1, new=10):
    """replace list elements (inplace)"""
    i = -1
    try:
        while 1:
            i = lst.index(old, i + 1)
            lst[i] = new
    except ValueError:
        pass

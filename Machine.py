from State import *
from Link import *


class Machine:
    def __init__(self):
        self.alphabet = []
        self.nbState = 0
        self.states = []
        self.initial = []
        self.final = []
        self.links = []
        self.current = State()

    def loadFromFile(self, filename):
        try:
            file = open(filename, "r")
        except:
            print("Cannot open the file, abort")
            return False

        lines = file.readlines()
        for i in range(0, len(lines)):
            lines[i] = lines[i].rstrip()
        file.close()

        self.alphabet = [e for e in lines[0]]
        self.nbState = int(lines[1])
        self.initial = [int(e) for e in lines[2].split()]
        self.final = [int(e) for e in lines[3].split()]
        self.states = [State(i, self.alphabet) for i in range(0, self.nbState)]
        self.current = self.states[self.initial[0]]

        self.initStateStatus()

        for i in range(4, len(lines)):
            line = lines[i].split()
            origin = self.states[int(line[0])]
            destination = self.states[int(line[1])]
            link = self.isLink(origin, destination)
            if not (line[2] == '#' and origin.id == destination.id):
                if not link[0]:
                    self.links.append(Link(origin, destination, line[2]))
                else:
                    link[1].addTag(line[2])
                origin.nbLink += 1
                origin.addLink(line[2], destination)
                if origin != destination:
                    destination.nbLink += 1

    def initMachine(self, nbState, initial, final, states, links):
        self.nbState = nbState
        self.initial = initial
        self.final = final
        self.states = states
        self.initStateStatus()
        self.links = links
        self.current = self.states[self.initial[0]]

    def initStateStatus(self):
        for e in self.final:
            self.states[e].setFinal(True)
        for e in self.initial:
            self.states[e].setInitial(True)

    def isLink(self, pOrigin, pDestination, list=[], isList=False):
        if isList:
            links = list
        else:
            links = self.links
        result = [False]
        for link in links:
            if link.origin == pOrigin and link.destination == pDestination:
                result = [True, link]
                break
        return result

    def canPass(self, char):
        result = False
        for link in self.links:
            if link.origin == self.current and char in link.tag:
                result = True
                self.current = link.destination
        return result

    def testAFD(self, pword):
        result = 0
        if len(pword) != 0:
            if pword[0] in self.alphabet and self.canPass(pword[0]):
                result = self.testAFD(pword[1:])
        elif self.current.isFinal():
            result = 1
        return result

    def recAFN(self, pword, pcurrent):
        result = 0
        if len(pword) != 0:
            if pword[0] in self.alphabet:
                for link in self.links:
                    if link.origin.id == pcurrent and pword[0] in link.tag:
                        # print(" exec " + pword + " from " + str(link.origin.id) + " to " + str(
                        #    link.destination.id) + " by " + str(pcurrent))
                        result = self.recAFN(pword[1:], link.destination.id)
                    if result == 1:
                        break
        elif self.states[pcurrent].isFinal():
            result = 1
        return result

    def testAFN(self, pword):
        result = 0
        for initialState in self.initial:
            self.current = self.states[initialState]
            # print(" current " + str(initialState))
            if self.recAFN(pword, initialState) == 1:
                result = 1
                break
        return result

    def minMoore(self):
        min = [[0 for e in range(len(self.alphabet) + 2)] for i in range(self.nbState)]
        for i in range(self.nbState):
            if self.states[i].isFinal():
                min[i][0] = 2
            else:
                min[i][0] = 1
        print(min)
        self.moore(min)
        print(min)
        self.updatebyMoore(min)

    def moore(self, list):
        for i in range(self.nbState):
            for j in range(1, len(self.alphabet) + 1):
                list[i][j] = list[self.states[i].next[self.alphabet[j - 1]][0]][0]
        nbclasse = 1
        for i in range(self.nbState):
            if i == 0:
                list[i][len(self.alphabet) + 1] = nbclasse
                nbclasse += 1
            else:
                for j in range(0, i):
                    if list[i][1:len(self.alphabet)] == list[j][1:len(self.alphabet)]:
                        list[i][len(self.alphabet) + 1] = list[j][len(self.alphabet) + 1]
                        break
                    if j == i - 1 and list[i][1:len(self.alphabet)] != list[j][1:len(self.alphabet)]:
                        list[j][len(self.alphabet) + 1] = nbclasse
                        nbclasse += 1
                if list[i][len(self.alphabet) + 1] == 0:
                    list[i][len(self.alphabet) + 1] = nbclasse
                    nbclasse += 1
        result = True
        for i in range(self.nbState):
            if list[i][0] != list[i][len(self.alphabet) + 1]:
                result = False
                break
        if not result:
            for i in range(self.nbState):
                list[i][0] = list[i][len(self.alphabet) + 1]
                list[i][len(self.alphabet) + 1] = 0
            print(list)
            self.moore(list)
        else:
            return list

    def updatebyMoore(self, list):
        list = self.minusOne2D(list)
        newState = []
        for i in range(len(list)):
            if list[i][0] not in newState:
                newState.append(list[i][0])
        nbnewState = len(newState)
        states = [State(e, self.alphabet) for e in newState]
        finals = []
        inits = []
        for i in range(nbnewState):
            isFinal = True
            isInit = True
            for j in range(self.nbState):
                if list[j][0] == i:
                    if not self.states[j].isFinal():
                        isFinal = False
                    if not self.states[j].isInitial():
                        isInit = False
            if isFinal:
                finals.append(i)
            if isInit:
                inits.append(i)

        links = []
        for i in range(len(states)):
            for j in range(1, len(self.alphabet) + 1):
                origin = states[list[i][0]]
                dest = states[list[i][j]]
                link = self.isLink(origin, dest, links, True)
                if not link[0]:
                    links.append(Link(states[list[i][0]], states[list[i][j]], self.alphabet[j - 1]))
                else:
                    link[1].addTag(self.alphabet[j - 1])
                origin.nbLink += 1
                if origin != dest:
                    dest.nbLink += 1
                origin.addLink(self.alphabet[j - 1], dest)

        self.initMachine(nbnewState, inits, finals, states, links)

    def determineAFN(self):
        liste = [[self.initial,],]
        tpls = [tuple(self.initial)]
        nblettre = len(self.alphabet)
        j = 0
        #print(liste)
        while j != len(tpls):
            for idlettre in range(nblettre):
                tpl = []
                for e in liste[j][0]:
                    #print("state : " + str(e) + self.alphabet[idlettre])
                    direction2 = self.states[e].next[self.alphabet[idlettre]]
                    not_inTpl = set(direction2) - set(tpl)
                    tpl = list(tpl) + list(not_inTpl)
                #print(tpl)
                liste[j].append(tpl)
                if tuple(tpl) not in tpls:
                    tpls.append(tuple(tpl))
                    liste.append([tpl,])
            j+=1
        print(liste)
        return self.cleandeter(liste, tpls)


    def cleandeter(self, tab, tpls):
        g = 0
        tab2 = [[-1 for i in range(len(tab)+1)] for e in tpls]
        final = []
        init = []
        for j in range(len(tpls)):
            for i in range(len(tpls[j])):
                if tpls[j][i] in self.final and j not in final:
                    final.append(j)
            if len(tpls[j])==1 and tpls[j][0] in self.initial and j not in init:
                init.append(j)

        for e in tpls:
            for i in range(len(tpls)):
                for j in range(len(self.alphabet) + 1):
                    #print(str(tab[i][j]) + " i " + str(i) + " j " + str(j))
                    if tuple(tab[i][j]) == e:
                        tab2[i][j] = g
            g += 1
        return tab2, final, init

    def determineAFNtofile(self,tab, final, init, path="defaultAFD"):
        chaine = ""
        for l in self.alphabet:
            chaine += l
        chaine +="\n" + str(len(tab)) + "\n"
        for e in init:
            chaine += str(e) + " "
        chaine += "\n"
        for e in final:
            chaine += str(e) + " "
        for j in range(len(tab)):
            for i in range(1, len(self.alphabet)+1):
                chaine += "\n" + str(tab[j][0]) + " " + str(tab[j][i]) + " " + str(self.alphabet[i-1])
        file = open(path,"w")
        file.write(chaine)
        file.close()

    def fusionEquivalence(self):
        """Nettoie un automate de tout les état equivalent.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        lks = []
        for link in self.links:
            if link.tag == "#":
                for lik in self.links:
                    if link != lik and link.destination == lik.origin or link.destination ==

    def fusionState(self, origin, destination):
        """Fusion de deux états
        Cette fonction fusionne deux etats ensemble en se debarrassant des e-transition.
        l'etat d'origin deviendra innacecible car il ne sera plus relié

        Parameters
        ----------
        origin : State
            L'état d'origine de fusion
        destination : State
            L'état de destination de fusion

        Returns
        -------
        None

        """
        if origin.isInit():
            if not destination.isInit():
                destination.initial = True
                self.initial.append(destination.id)
            self.initial.remove(origin.id)
        if origin.isFinal():
            if not destination.isFinal():
                destination.final = True
                self.final.append(destination.id)
            self.final.remove(origin.id)
        for link in self.links:
            if link.origin.id == origin.id and link.destination.id == destination.id:
                if "#" in link.tag:
                    link.tag.remove('#')
                    if len(link.tag) > 0:
                        self.xLink(link, destination, destination)
                    else:
                        self.links.remove(link)
            elif link.origin.id == origin.id:
                self.xLink(link, destination, link.destination)
            elif link.destination.id == origin.id:
                self.xLink(link, link.origin, destination)
        origin.clear()

    def xLink(self, link, origin, destination):
        """Fusion de lien
        Cette fonction verifie si une liaison est deja existante
        Si c'est le cas elle va fusionner les tag de link avec la liaison trouver puis
        supprimer link

        Parameters
        ----------
        link : Link
            le lien changeant
        origin : State
            L'état d'origine du nouveau lien
        destination : State
            L'état de destination du nouveau lien

        Returns
        -------
        None

        """
        anotherlink = self.isLink(origin, destination)
        if anotherlink[0]:
            for tag in link.tag:
                if tag not in anotherlink[1].tag:
                    anotherlink[1].tag.append(tag)
                    anotherlink[1].origin.addLink(tag, destination)
            self.links.remove(link)
        else:
            link.origin = origin
            link.destination = destination
            for tag in link.tag:
                origin.addLink(tag, destination)

    def minusOne2D(self, list):
        for i in range(len(list)):
            for j in range(len(list[i])):
                list[i][j] -= 1
        return list

    def __str__(self):
        desc = "Machine : \n - Alphabet : {} \n - nbState : {}\n - initial state : {}\n - final state {}\n".format(
            self.alphabet, self.nbState, self.initial, self.final)
        desc += "\n STATES :"
        for i in range(self.nbState):
            desc += "\n  " + str(self.states[i])
        desc += "\n\n LINKS :\n"
        for link in self.links:
            desc += "  --> link {}\n".format(link)
        return desc

from Machine import *
import sys

def main(argv):

    mode, input = int(sys.argv[1]),sys.argv[2]
    if mode == 0:
        word, output = sys.argv[3], sys.argv[4]
    elif mode in [1, 2, 3]:
        output = sys.argv[3]
    else:
        raise Exception("Value not correct")

    machine = Machine()
    if mode == 0:
        machine.loadFromFile(input)
        try:
            file = open(word, "r")
        except:
            print("Cannot open the file, abort")
            return False
        words = file.readlines()
        for i in range(0, len(words)):
            words[i] = words[i].rstrip()
        file.close()
        #print("\n\n AFD TEST \n")
        chaine = ""
        for i in range(0, len(words)):
            machine.current = machine.states[machine.initial[0]]
            result = machine.testAFN(words[i])
            chaine += str(result) + "\n"
            #print(str(result) + " " + words[i])
    elif mode == 1:
        machine.loadFromFile(input)
        machine.minMoore()
        machine.toFile(output)
    elif mode == 2:
        machine.loadFromFile(input)
        list, final, init = machine.determineAFN()
        machine.determineAFNtofile(list,final,init,output)
    elif mode == 3:
        machine.loadFromFile(input,True)
        machine.fusionEquivalence()
        machine.supetransition()
        machine.toFile(output)



if __name__ == '__main__':
    main(sys.argv)


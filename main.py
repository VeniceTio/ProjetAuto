from Machine import *
import sys

def main(argv):
    """
    mode, input = int(sys.argv[1]),sys.argv[2]
    if mode == 0:
        word, output = sys.argv[3], sys.argv[4]
    elif mode in [1, 2, 3]:
        output = sys.argv[3]
    else:
        print("Value not correct")

    """
    machine = Machine()
    machine.loadFromFile("Instances/eAFN/eafn2.txt")

    print(machine)
    #list, final, init = machine.determineAFN()
    #machine.determineAFNtofile(list,final,init)
    machine.fusionEquivalence()
    print(machine)
    # print(machine)
    #machine.minMoore()
    #print(machine)

    """
    try:
        file = open("Instances/AFN/mots1.txt", "r")
    except:
        print("Cannot open the file, abort")
        return False
    words = file.readlines()
    for i in range(0, len(words)):
        words[i] = words[i].rstrip()
    file.close()
    print("\n\n AFD TEST \n")
    for i in range(0, len(words)):
        machine.current = machine.states[machine.initial[0]]
        print(str(machine.testAFN(words[i])) + " " + words[i])
    """



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

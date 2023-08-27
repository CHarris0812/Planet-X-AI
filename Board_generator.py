#Comets: 2 DONE
#Asteroids: 4 DONE
#Dwarf planets: 1 DONE
#Empty sectors: 2 DONE
#Gas clouds: 2 DONE
#Planet X: 1 DONE

def main():
    generateBoards()

def generateBoards():
    boards = generateAsteroids()
    boards = addDwarfPlanet(boards)
    boards = addEmptySectors(boards)
    boards = addComets(boards)
    boards = addPlanetX(boards)
    boards = addGasClouds(boards)

    locations = [0 for i in range(12)]
    for i in boards:
        for j in range(12):
            if i[j] == "A":
                locations[j] += 1


    print(locations)
    writeToFile(boards)
    display(boards)
    print(len(boards))

def removeDuplicates(boards):
    temp = []
    for i in boards:
        if i not in temp:
            temp.append(i)
    return temp#Working

def display(boards):
    for i in boards:
        print(i)#Working

def generateAsteroids():
    boards = addFirstTwoAsteroids()
    boards = addFinalAsteroids(boards)
    boards = removeDuplicates(boards)
    return boards#Working

def addFirstTwoAsteroids():
    boards = []
    for i in range(12):
        temp = ["" for j in range(12)]
        temp[i] = "A"
        temp[(i + 1) % 12] = "A"
        boards.append(temp)
    return boards#Working

def addFinalAsteroids(temp):
    boards = []
    for i in temp:
        for j in range(12):
            if i[j] == "" and i[(j + 1) % 12] == "":
                temp2 = [k for k in i]
                temp2[j] = "A"
                temp2[(j + 1) % 12] = "A"
                boards.append(temp2)
    return boards#Working

def addComets(boards):
    for i in range(2):
        boards = addComet(boards)
    boards = removeDuplicates(boards)
    return boards#Working

def addComet(boards):
    toReturn = []
    possible = [1, 2, 4, 6, 10]
    for i in boards:
        for j in possible:
            if i[j] == "":
                temp = [k for k in i]
                temp[j] = "C"
                toReturn.append(temp)
    return toReturn#Working

def addDwarfPlanet(boards):
    toReturn = []
    for i in boards:
        for j in range(12):
            if i[j] == "":
                temp = [k for k in i]
                temp[j] = "D"
                toReturn.append(temp)
    toReturn = removeDuplicates(toReturn)
    return toReturn#Working

def addEmptySectors(boards):
    for i in range(2):
        boards = addEmptySector(boards)
    boards = removeDuplicates(boards)
    return boards#Working

def addEmptySector(boards):
    toReturn = []
    for i in boards:
        for j in range(12):
            if i[j] == "":
                temp = [k for k in i]
                temp[j] = "E"
                toReturn.append(temp)
    toReturn = removeDuplicates(toReturn)
    return toReturn#Working

def addGasClouds(boards):
    for i in range(2):
        boards = addGasCloud(boards)
    boards = removeDuplicates(boards)
    return boards#Working

def addGasCloud(boards):
    toReturn = []
    for i in boards:
        for j in range(12):
            if i[j] == "" and (i[(j + 1) % 12] == "E" or i[(j + 11) % 12] == "E"):
                temp = [k for k in i]
                temp[j] = "G"
                toReturn.append(temp)
    return toReturn#Working

def addPlanetX(boards):
    toReturn = []
    for i in boards:
        for j in range(12):
            if i[j] == "" and i[(j + 1) % 12] != "D" and i[(j + 11) % 12] != "D":
                temp = [k for k in i]
                temp[j] = "X"
                toReturn.append(temp)
    return toReturn#Working

def writeToFile(boards):
    f = open("Board_list.txt", "w")
    for i in boards:
        f.write("".join(i))
        f.write("\n")
    f.close()

if __name__ == "__main__":
    main()

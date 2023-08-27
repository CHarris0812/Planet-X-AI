import re, random

def main():
    
    f = open("Board_list.txt", "r")
    boards = []
    for line in f:
        boards.append(line[:12])
    
    f = open("Games.txt")
    data = []
    for line in f:
        line = line.replace("\n", "")
        data.append(line.split("-"))
    
    data = ["0-0-0-0-GCCXAADAAGEE-22DA-31CA-21AG-33DC-0DG-54G-4XA-B7D2".split("-")]
    for i in data:
        startingInfo, board, research, conference = interpretGame(i)
        temp = int(input("What starting position? (number 0-3, spring is 0) "))
        runAI(boards, startingInfo[temp], research, conference, board)

def readStartingInfo(info):
    info = re.findall("\d+\w", info)
    return info

def runAI(boards, startingInfo, researches, conference, result):
    startingInfo = readStartingInfo(startingInfo)
    for i in startingInfo:
        sector = int(re.match("\d+", i).group(0))
        thing = re.search("[A-Z]", i).group(0)
        boards = removePossibilities(boards, sector - 1, sector - 1, thing, 0)

    researchedLastTurn = False
    researched = [False, False, False, False, False, False]
    mySector = 0
    known = [False for i in range(12)]
    while True:
        print("Currently at sector", mySector + 1)
        if len(boards) == 0:
            print("No valid boards")
            return
        loc = foundX(boards)
        if loc != None:
            print("X has been found")
            print("X is at", loc + 1)
            prev, temp = findObject(boards, (loc + 11) % 12)
            next, temp = findObject(boards, (loc + 1) % 12)
            print("Previous thing is " + prev)
            print("Next thing is " + next)
            return
        elif researchedLastTurn == False:
            val = pickRandom(researched)
            boards = interpretResearch(boards, researches[val])
            researched[val] = True
            researchedLastTurn = True
            print("Researched", "abcdef"[val])
            moved = 1
        else:
            move = findMove(boards, mySector)
            move[2] = move[2] % 12
            print("Surveying for " + move[0] + " in sectors " + str(move[1] + 1) + " to " + str(move[2] + 1))
            if move[2] < move[1]:
                moveLength = move[2] + 1 + (12 - move[1])
            else:
                moveLength = move[2] - move[1] + 1

            if moveLength <= 3:
                moved = 4
            else:
                moved = 3 

            count = survey(move[0], move[1], move[2], result)
            boards = removePossibilities(boards, move[1], move[2], move[0], count)
            if False in researched:
                researchedLastTurn = False

        if mySector < 10 and mySector + moved >= 10:
            print("Planet X conference")
            boards = interpretResearch(boards, conference)

        if passedTheory(mySector, moved):
            theory = generateTheory(boards, known)
            if theory[0] != -1:
                known[theory[0]] = True
                print()
                print(theory[1], "is at", theory[0] + 1)
            inp = input("What information was revealed (format as SectorObject)")
            print()
            boards, known = removeBoardsFromTheories(boards, known, inp)

        mySector = (mySector + moved) % 12
        print("Boards remaining:", len(boards))
    
def foundX(boards):
    xLoc = -1
    for i in range(12):
        obj, chance = findObject(boards, i)
        if obj == "X" and chance == 1:
            xLoc = i
    if xLoc != -1:
        prev, chance = findObject(boards, (xLoc + 11) % 12)
        if chance == 1:
            next, chance = findObject(boards, (xLoc + 1) % 12)
            if chance == 1:
                return xLoc
    return None

def findObject(boards, loc):
    objectType = {"A":0, "C":0, "D":0, "E":0, "G":0, "X":0}
    
    mostCommon = ""
    count = 0
    for i in boards:
        objectType[i[loc]] += 1
    for i in objectType:
        if objectType[i] > count:
            count = objectType[i]
            mostCommon = i
    return mostCommon, count / len(boards)

def survey(object, start, end, board):
    board *= 2
    if end < start:
        end += 12
    return board[start:end + 1].count(object)

def interpretGame(data):
    startingInfo = [data[0], data[1], data[2], data[3]]#Sping, summer, winter, fall
    board = data[4]
    research = [data[5], data[6], data[7], data[8], data[9], data[10]]
    conference = data[11]
    code = data[12]
    print("Game code", code)
    return startingInfo, board, research, conference 

def removePossibilities(boards, start, end, object, count):
    if end < start:
        end += 12
    newBoards = []
    for i in boards: 
        i *= 2
        if i[start:end + 1].count(object) == count:
            newBoards.append(i[:12])
    return newBoards

def findMove(remainingBoards, startSector):
    maxRemoved = 0
    maxMove = ""
    for i in range(startSector, startSector + 6):
        #CGEG
        #CGEX
        for j in range(i, startSector + 6):
            for k in ["A", "C", "D", "E", "G"]:
                temp = findExpectedRemoved(i, j, k, remainingBoards)
                if j - i < 3:
                    temp = temp / 4
                else:
                    temp = temp / 3
                if temp > maxRemoved:
                    maxRemoved = temp
                    maxMove = [k, i, j]
    if maxMove == "":
        maxMove = ["A", startSector, startSector + 6]
    return maxMove

def findExpectedRemoved(start, end, object, remainingBoards):
    numOfEachPossibility = [0, 0, 0, 0, 0]
    for i in remainingBoards:
        i *= 2
        numOfEachPossibility[i[start:end + 1].count(object)] += 1
        i = i[:12]

    expectedRemoved = 0
    for i in numOfEachPossibility:
        expectedRemoved += (len(remainingBoards) - i) * i / len(remainingBoards)
    return expectedRemoved

def pickRandom(researched):
    while True:
        loc = random.randint(0, 5)
        if researched[loc] == False:
            return loc

def interpretResearch(boards, research):
    #Opp, all within, 1 within, not within
    #0: one thing opp thing
    #1: all within x sectors
    #2: 1 within x sectors
    #3: all not within x sectors
    #4: all not opp thing
    #5: all in band <= x
    #Research format: [0-4], digit(maybe), object, object
    researchType = int(research[0])
    newBoards = []
    if researchType == 0:
        regex = research[1] + ".{5}" + research[2] + "|" + research[2] + ".{5}" + research[1]
        for b in boards:
            if re.search(regex, b) != None:
                newBoards.append(b)
    elif researchType == 1:
        regex1 = research[2] + ".?" * int(research[1]) + research[3]
        regex2 = research[3] + ".?" * int(research[1]) + research[2] + "$"
        for b in boards:
            locs = [m.start() for m in re.finditer(research[2], b)]
            allValid = True
            for l in locs:
                if re.match(regex1, b[l:]) == None and re.search(regex2, b[:l + 1]) == None:
                    allValid = False
            if allValid:
                newBoards.append(b)
    elif researchType == 2:
        regex = research[2] + ".?" * (int(research[1]) - 1) + research[3] + "|" + research[3] + ".?" * (int(research[1]) - 1) + research[2]
        for b in boards:
            if re.search(regex, b) != None:
                newBoards.append(b)
    elif researchType == 3:
        regex = research[2] + ".?" * (int(research[1]) - 1) + research[3] + "|" + research[3] + ".?" * (int(research[1]) - 1) + research[2]
        for b in boards:
            if re.search(regex, b) == None:
                newBoards.append(b)
    elif researchType == 4:
        regex = research[1] + ".{5}" + research[2] + "|" + research[2] + ".{5}" + research[1]
        for b in boards:
            if re.search(regex, b) == None:
                newBoards.append(b)
    elif researchType == 5:
        length = research[1]
        obj = research[2]
        if obj == "A":
            print("Not yet implemented")
        else:
            regex = obj + ".?" * (int(length) - 2) + obj
            for b in boards:
                temp = b * 2
                if re.search(regex, temp) != None:
                    newBoards.append(b)
    return newBoards

def removeBoardsFromTheories(boards, known, inputVals):
    inp = re.findall("\d+[ACDEG]", inputVals)
    for i in inp:
        sector = int(re.match("\d+", i).group(0)) - 1
        obj = i[-1]
        known[sector] = True
        newBoards = []
        for b in boards:
            if b[sector] == obj:
                newBoards.append(b)
        boards = [j for j in newBoards]
    return boards, known

def generateTheory(boards, known):
    mostLikely = -1
    chance = 0
    for i in range(12):
        obj, c = findObject(boards, i)
        if not known[i]:
            if c > chance and obj in "ACDG":
                chance = c
                mostLikely = i
    if chance == 1:
        return [mostLikely, findObject(boards, mostLikely)]
    return [-1, -1]

def passedTheory(sector, moveLength):
    theoryLocs = [2, 5, 8, 11]
    for i in theoryLocs:
        if sector <= i and sector + moveLength > i:
            return True
    return False

if __name__ == "__main__":
    main()

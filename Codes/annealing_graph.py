import math
import random
import copy
from tkinter import *
import time
import ujson

xaxis = []
yaxis = []

guiglobal = []
guiglobalstat = []


def annealing(fileName):
    st = time.time()
    # Initalize random place for the array using function and return it
    # Retrun [array , no of cells , no of connections ]
    file = open(fileName, "r")
    placement, dict, numberOfCells, numberOfConnections = random_initalize(file)

    size = [len(placement), len(placement[0])]
    global guiglobal
    global guiglobalstat
    guiglobal = size
    # Use HPWL and Get inital cose
    cf = {}
    HPWL_dict = {}
    [nets, cf] = getConnectionsArray(file, numberOfConnections, numberOfCells)

    cL, HPWL_dict = HPWL1(size, nets, dict)
    T = (500 * cL)   # initial temp

    Tf = pow(5 * 10, -6) * cL / numberOfConnections
    moves = int(10 * numberOfCells)
    count = 0
    # Animate
    # countG = 0
    countt = 0
    couf = 0
    while T > Tf:
        # pick 2 random number in the range of cells
        index1 = [
            random.randint(0,
                           len(placement) - 1),
            random.randint(0,
                           len(placement[0]) - 1)
        ]
        index2 = [
            random.randint(0,
                           len(placement) - 1),
            random.randint(0,
                           len(placement[0]) - 1)
        ]
        while index1 == index2:
            index2 = [
                random.randint(0,
                               len(placement) - 1),
                random.randint(0,
                               len(placement[0]) - 1)
            ]
        selected = []
        HPWL_newDict = {}
        # swap in the current array and return with new array
        newPlacement, newDict, selected = swap(placement, index1, index2, dict)
        n, HPWL_newDict = HPWL(size, nets, newDict, cf, selected, cL, HPWL_dict)

        deltaL = n - cL
        if deltaL < 0:
            placement = ujson.loads(ujson.dumps(newPlacement))
            dict = newDict.copy()
            cL = n
            storePlacement = ujson.loads(ujson.dumps(placement))
            HPWL_dict = HPWL_newDict.copy()
            storeL = cL

        else:
            value = -deltaL / T
            e = math.exp(value)
            rand = random.uniform(0, 1)
            if rand < e:
                placement = ujson.loads(ujson.dumps(newPlacement))
                dict = newDict.copy()
                HPWL_dict = HPWL_newDict.copy()
                cL = n

        count = count + 1

        # Animate
        # countG = countG+1

        if (count == moves or moves == 0):
            T = 0.9 * T

            ##taking a point syncoronized
            global xaxis

            xaxis.append(int(n))

            ##taking a point syncoronized end

            ##taking a point syncoronized

            global yaxis

            yaxis.append(int(T))

            ##taking a point syncoronized end

            count = 0

        # Animate
        # if(countG == 2000):
        #   guiglobalstat = placement
        #   gui()
        #   root.update()
        #   time.sleep(0.01)
        #   countG=0

    if (storeL < cL):
        placement = copy.ujson.loads(ujson.dumps(storePlacement))
        cL = storeL

    guiglobalstat = placement
    gui()
    root.update()

    sss = "--"
    for row in placement:
        temp = ""
        for item in row:
            if str(item) == "-1":
                temp = temp + '{:4}'.format(sss)
            else:
                temp = temp + str('{:4}'.format(str(item)))
        print(temp)

    print("\n")

    for row in placement:
        temp = ""
        for item in row:
            if str(item) == "-1":
                temp = temp + '{:4}'.format(str(1))
            else:
                temp = temp + str('{:4}'.format(str(0)))
        print(temp)

    print("\n\n The estimated wire length is " + str(cL))

    end = time.time()
    print("\n\n The run time of the programe is " + str(end - st) + " seconds")


##############################################################
def gui():
    for r in range(guiglobal[0]):
        for c in range(guiglobal[1]):

            Grid.rowconfigure(root, r, weight=1)
            Grid.columnconfigure(root, c, weight=1)

            if guiglobalstat[r][c] == -1:
                Button(root,
                       bg="green",
                       text='',
                       height=1,
                       justify="center",
                       state="disabled",
                       width=1).grid(row=r, column=c, sticky="NSEW")
            else:
                Button(root,
                       bg="yellow",
                       text='%s' % (guiglobalstat[r][c]),
                       fg="black",
                       height=1,
                       justify="center",
                       state="disabled",
                       width=1).grid(row=r, column=c, sticky="NSEW")


##############################################################
def random_initalize(file):
    line = file.readline()
    line = line.split()

    width = line[2]
    height = line[3]
    b = line[0]
    xx = line[1]
    # ##first validation
    if int(width)*int(height)<int(b):
        print("there is an error with the give input file")
        raise SystemExit
    # ##end of validation

    temp = int(height)

    tempx = int(width)
    tempb = int(b)
    tempff = int(xx)

    board = []
    for i in range(temp):
        board.append([-1] * tempx)

    counter = 0
    x = 0
    y = 0
    new_dict = {}
    for i in range(tempb):
        while (board[x][y] != -1):
            x = random.randint(0, temp - 1)
            y = random.randint(0, tempx - 1)
        board[x][y] = counter
        new_dict[counter] = [x, y]

        counter = counter + 1
    print("The First Random Placement:")
    for row in board:
        temp = ""
        for item in row:
            if str(item) == "-1":
                temp = temp + '{:4}'.format(str(1))
            else:
                temp = temp + str('{:4}'.format(str(0)))
        print(temp)

    print("\n")

    return board, new_dict, tempb, tempff


##############################################################
def getConnectionsArray(file, numberOfConnections, numberOfCells):
    nets = []

    cf = {}

    for i in range(numberOfCells):
        cf[i] = {}
    for i in range(numberOfConnections):
        l = file.readline()
        connection = l.split()

        # #validation
        if len(connection)!=(int(connection[0])+1):
            print("there is an error with the give input file")
            raise SystemExit
        # #end of validation

        connection.pop(0)
        con = []
        for j in connection:
            temp = int(j)
            con.append(temp)
            cf[temp][i] = i
        connection = con
        nets.append(connection)

    return nets, cf


##############################################################


def HPWL1(size, nets, dict):
    HPWL_dict = {}
    counter = 0
    iijj = []
    hpwl = 0
    temp = 0
    for i in nets:
        maxI = 0
        minI = size[0]
        maxJ = 0
        minJ = size[1]

        for j in i:
            iijj = []
            cellCurrent = j

            iijj = dict[cellCurrent]

            ii = iijj[0]
            jj = iijj[1]

            if (ii >= maxI):
                maxI = ii
            if (jj >= maxJ):
                maxJ = jj

            if (ii <= minI):
                minI = ii
            if (jj <= minJ):
                minJ = jj

        temp = (maxI - minI) + (maxJ - minJ)
        HPWL_dict[counter] = temp

        hpwl = hpwl + temp

        counter = counter + 1

    return hpwl, HPWL_dict


##############################################################


def HPWL(size, nets, dict, cf, selected, cL, HPWL_dict):
    finished = {}  ## see which line in the file you got its hpwl to net do it again
    iijj = []
    HPWL_dictNew = HPWL_dict.copy()
    hpwl = cL
    first = 0
    # for i in nets:
    #   maxI = 0
    #   minI = size[0]
    #   maxJ = 0
    #   minJ = size[1]

    #   for j in i:
    #     iijj = []
    #     cellCurrent = j

    #     iijj = dict[cellCurrent]

    #     ii = iijj[0]
    #     jj = iijj[1]

    #     if (ii >= maxI):
    #       maxI = ii
    #     if (jj >= maxJ):
    #       maxJ = jj

    #     if (ii <= minI):
    #       minI = ii
    #     if (jj <= minJ):
    #       minJ = jj
    #   hpwl = hpwl + (maxI - minI) + (maxJ - minJ)

    for i in selected:
        for j in cf[i]:
            maxI = 0
            minI = size[0]
            maxJ = 0
            minJ = size[1]
            if j not in finished:
                finished[j] = 1
                hpwl = hpwl - HPWL_dictNew[j]
                for k in nets[j]:
                    iijj = []
                    cellCurrent = k

                    iijj = dict[cellCurrent]

                    ii = iijj[0]
                    jj = iijj[1]

                    if (ii >= maxI):
                        maxI = ii
                    if (jj >= maxJ):
                        maxJ = jj

                    if (ii <= minI):
                        minI = ii
                    if (jj <= minJ):
                        minJ = jj
                temp = (maxI - minI) + (maxJ - minJ)

                HPWL_dictNew[j] = temp

                hpwl = hpwl + temp

    return hpwl, HPWL_dictNew


##############################################################
def swap(placement, i1, i2, dict):
    selected = []
    cell1 = placement[i1[0]][i1[1]]
    cell2 = placement[i2[0]][i2[1]]

    new_dict = dict.copy()

    if (cell1 == -1 and cell2 == -1):
        a = 0
    elif (cell1 == -1):
        new_dict[cell2] = i1
        selected.append(cell2)
    elif (cell2 == -1):
        new_dict[cell1] = i2
        selected.append(cell1)
    else:
        temp2 = new_dict[cell1]
        new_dict[cell1] = new_dict[cell2]
        new_dict[cell2] = temp2
        selected.append(cell1)
        selected.append(cell2)

    new_array = ujson.loads(ujson.dumps(placement))
    temp = new_array[i1[0]][i1[1]]
    new_array[i1[0]][i1[1]] = new_array[i2[0]][i2[1]]
    new_array[i2[0]][i2[1]] = temp

    return new_array, new_dict, selected


##############################################################
#####   MAIN  ######

rate = 0
fileName = ""
moveFactor = 0

print("Welcome to our programe ! Please put the file name that you want to test on: ")
fileName = input()

root = Tk()
root.geometry("500x500")
x = 0

annealing(str(fileName))

##ploting the graph

import matplotlib.pyplot as plt

# print(yaxis)
xnew = []
diff = int(len(xaxis) / len(yaxis))

# print(xnew)

plt.plot(yaxis, xaxis)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title("A simple line graph")

plt.show()
##ploting end

root.mainloop()
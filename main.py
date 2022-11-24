import math
import random
import copy
from tkinter import *
import time

guiglobal = []
guiglobalstat = []


def annealing(fileName):
  #Initalize random place for the array using function and return it
  # Retrun [array , no of cells , no of connections ]
  file = open(fileName, "r")
  placement, dict, numberOfCells, numberOfConnections = random_initalize(file)

  size = [len(placement), len(placement[0])]
  global guiglobal
  global guiglobalstat
  guiglobal = size
  #Use HPWL and Get inital cose

  nets = getConnectionsArray(file, numberOfConnections)

  cL = HPWL(size, nets, dict)
  T = 500 * cL  # initial temp

  Tf = pow(5 * 10, -6) * cL / numberOfConnections
  moves = int(10 * numberOfCells / 25)
  count = 0

  #Animate
  # countG = 0
  
  while T > Tf:
    #pick 2 random number in the range of cells
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

    #swap in the current array and return with new array
    newPlacement, newDict = swap(placement, index1, index2, dict)
    n = HPWL(size, nets, newDict)
    deltaL = n - cL
    if deltaL < 0:
      placement = copy.deepcopy(newPlacement)
      dict = newDict.copy()
      cL = n
      storePlacement = copy.deepcopy(placement)
      storeL = cL
    else:
      value = -deltaL / T
      e = math.exp(value)
      rand = random.uniform(0, 1)
      if rand < e:
        placement = copy.deepcopy(newPlacement)
        dict = newDict.copy()
        cL = n
    count = count + 1

     #Animate
    # countG = countG+1

    if (count == moves or moves == 0):
      T = 0.9 * T
      count = 0


    #Animate  
    # if(countG == 2000):
    #   guiglobalstat = placement
    #   gui()
    #   root.update()
    #   time.sleep(0.01)
    #   countG=0

  if (storeL < cL):
    placement = copy.deepcopy(storePlacement)
    cL = storeL


  
  guiglobalstat = placement
  gui()
  root.update()




  sss="--"
  for row in placement:
    temp=""
    for item in row:
      if str(item) =="-1":
        temp=temp + '{:4}'.format(sss)
      else:
        temp=temp + str('{:4}'.format(str(item)))
    print(temp)

  print("\n\n The estimated wire length is " + str(cL))


def gui():

  for r in range(guiglobal[0]):
    for c in range(guiglobal[1]):

      Grid.rowconfigure(root,r,weight=1)
      Grid.columnconfigure(root,c,weight=1)

      if guiglobalstat[r][c] == -1:
        Button(root,
                       bg="green",
                       text='',
                       height=1,
                       justify="center",
                       state="disabled",
                       width=1).grid(row=r, column=c,  sticky="NSEW")
      else:
        Button(root,
                       bg="yellow",
                       text='%s' % (guiglobalstat[r][c]),
                       fg="black",
                       height=1,
                       justify="center",
                       state="disabled",
                       width=1).grid(row=r, column=c,  sticky="NSEW")


def random_initalize(file):



  line = file.readline()
  line = line.split()

  width = line[2]
  height = line[3]
  b = line[0]
  xx = line[1]


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



  return board, new_dict, tempb, tempff


def getConnectionsArray(file, numberOfConnections):
  nets = []
  for i in range(numberOfConnections):
    l = file.readline()
    connection = l.split()
    connection.pop(0)
    con = []
    for j in connection:
      temp = int(j)
      con.append(temp)
    connection = con
    nets.append(connection)

  return nets





def HPWL(size, nets, dict):

  iijj = []
  hpwl = 0
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
    hpwl = hpwl + (maxI - minI) + (maxJ - minJ)
  return hpwl


def swap(placement, i1, i2, dict):

  cell1 = placement[i1[0]][i1[1]]
  cell2 = placement[i2[0]][i2[1]]

  new_dict = dict.copy()

  if (cell1 == -1 and cell2 == -1):
    a = 0
  elif (cell1 == -1):
    new_dict[cell2] = i1
  elif (cell2 == -1):
    new_dict[cell1] = i2
  else:
    temp2 = new_dict[cell1]
    new_dict[cell1] = new_dict[cell2]
    new_dict[cell2] = temp2

  new_array = copy.deepcopy(placement)
  temp = new_array[i1[0]][i1[1]]
  new_array[i1[0]][i1[1]] = new_array[i2[0]][i2[1]]
  new_array[i2[0]][i2[1]] = temp

  return new_array, new_dict


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

annealing(str(fileName) )

root.mainloop()

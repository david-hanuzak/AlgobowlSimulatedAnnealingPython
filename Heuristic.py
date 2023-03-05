import random
import numpy as np



def additions(lst, found, s):                      #find random solution for input
    outlst = s
    for i in lst:
        #print(found)
        while found[-1] < i:
            a = found[-1]

            blst = found[np.where(found <= (i - a))]
            b = np.random.choice(blst)

            if a+b not in found:
                outlst.append([a, b])
                found = np.append(found,a+b)
    return (outlst, found)

def adjacent(lst, found, s):
    n = random.randint(1,int(len(lst)/2)) #cut the list at a random point
    result = lst[:n]
    soln = s[0:n]
    i = int(np.where(found == result[-1])[0][0])
    f = np.asarray(found[:i+1])
    ind = lst[n-len(lst):]
    rest = additions(ind, f,soln)
    soln.append(rest[0])
    return (soln,rest[1]) #return the first portion of the list with a new end portion


def solve(inlst, maxIter, startTemp, alpha):
    f = np.asarray([1])
    imp = 0
    ann = 0
    currentTemp = startTemp
    iteration = 0
    interval = (int)(maxIter / 10)
    print("finding initial")
    soln = additions(inlst, f, [])
    s = soln[0]
    f = soln[1]
    best = s

    print("starting solution")
    while iteration < maxIter or len(soln[0]) == len(inlst):
        print("iteration: ", iteration)
        adj = adjacent(inlst,f,s)

        if len(adj[0]) < len(soln[0]): #adjacent is better
            soln = adj
            f = adj[1]
            s = adj[0]
            imp = imp + 1
            #print("imp: ", imp)
            if(len(s) < len(best)):
                best = s
                print("new best: ", len(s))
        else:  # adjacent is worse
            accept_p = np.exp((len(soln[0]) - len(adj)) / currentTemp)
            p = np.random.random_sample()
            if p < accept_p:  # accept anyway
                soln = adj
                f = adj[1]
                ann = ann + 1
                #print("ann: ",ann)
                # else don't accept

        if currentTemp < 0.00001:
            currentTemp = 0.00001
        else:
            currentTemp *= alpha
        iteration += 1

    return best

def readInput(name):
    inFile = open(name)
    inFile.readline() #ignore first line
    str = inFile.readline()

    strLst = str.split(" ")
    intLst = []

    for s in strLst:
        intLst.append(int(s))

    return intLst

inFile = readInput("input.txt")
max_iter = 10000
start_temperature = 10000.0
alpha = 0.99

soln = solve(inFile, max_iter, start_temperature, alpha)
print("done:", len(soln), soln)


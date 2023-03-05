import random
import numpy as np

def find(n, f, s):

    r1 = random.randint(1,n-1)
    r2 = n - r1

    if r1 == r2:
        if r1 in f:
            s.append([r1, r2])
            return n
        else:
            f.append(find(r1, f, s))
            s.append([r1,r2])
            return n


    if (r1 in f) & (r2 in f):
        s.append([r1, r2])
        return n
    elif r1 in f:
        a = find(r2, f, s)
        f.append(a)
        s.append([r1, r2])
        return n
    elif r2 in f:
        b = find(r1, f, s)
        f.append(b)
        s.append([r1, r2])
        return n
    else:
        a = find(r1, f, s)
        f.append(a)
        b = find(r2, f, s)
        f.append(b)
        s.append([r1, r2])
        return n

def findDoub(n, f, s):
    while (2*f[len(f)-1]) < n:
        f.append(2*f[len(f)-1])
        s.append(f[len(f)-1])

def additions(lst, found, s):                      #find random solution for input
    for i in lst:
        n = found[len(found)-1]
        diff = i - n
        if diff >= 2*n:
            findDoub(i,found,s)
            found.append(find(i, found, s))
        else:
            found.append(find(i,found,s))
        print(i)


    return (s, found)

def adjacent(lst, found, s):
    n = random.randint(1,int(len(lst)/2))#cut the list at a random point
    result = lst[:n]
    fn = np.asarray(found)
    soln = s[0:n]
    i = int(np.where(fn == result[-1])[0][0])
    f = found[:i+1]
    ind = lst[n-len(lst):]
    rest = additions(ind, f,soln)
    soln.append(rest[0])
    return (soln,rest[1]) #return the first portion of the list with a new end portion


def solve(inlst, maxIter, startTemp, alpha):
    f = [1,2]
    s = [[1,1]]
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
        print("iteration: ", iteration, " best: ", len(best))
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

inFile = readInput("input_group592.txt")
max_iter = 20000
start_temperature = 10000.0
alpha = 0.8

soln = solve(inFile, max_iter, start_temperature, alpha)
print("done:", len(soln), soln)


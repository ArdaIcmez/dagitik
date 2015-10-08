# Author : Arda ICMEZ
# Date : 04.10.15

import numpy as np
import matplotlib.pyplot as plt

def populate(arr):
    """
    Rounding up numbers from the given gaussian array, adding them into
    the dictionary with the calculated index
    
    arr : list<double>
    """
    roundedArr = {}
    for item in arr:
        keyItem = int(round(item))
        if roundedArr.has_key(keyItem):
            roundedArr[keyItem] += 1
        else:
            roundedArr[keyItem] = 1
    return roundedArr
def normalize(arr,sumNumbers):
    """
    Normalizing values of the array
    
    arr : dictionary<int,double>
    sumNumbers : int
    """
    for item in arr:
        arr[item] = round(arr[item]/sumNumbers,4)
    return arr
def getDistance(arr1,arr2):
    """
    Calculating the distance of 2 uniform distributions using Wasserstein metric method
    
    arr1, arr2 : dictionary<int,double>
    """

    mySum = 0.0
    distIndex = sorted(arr1.keys())[0] - sorted(arr2.keys())[0]
    if distIndex>0:
        tempArr = arr1
        arr1=arr2
        arr2=tempArr
    distIndex = abs(distIndex)
    tempArr = arr2.copy()
    for item in sorted(arr1.keys()):
        while arr1[item] > 0.0: # To eliminate the error of all the rounding
            myIndex = item+distIndex
            if arr2.has_key(myIndex):
                if(arr1[item]> arr2[item+distIndex]):
                    mySum += arr2[item+distIndex]*abs(distIndex)
                    arr1[item] -= arr2[item+distIndex]
                    del tempArr[item+distIndex]
                    distIndex+=1
                elif arr1[item] == arr2[item+distIndex]:
                    mySum+= arr1[item] *abs(distIndex)
                    arr1[item] = 0
                    del tempArr[item+distIndex]
                else:
                    mySum += arr1[item]*abs(distIndex)
                    arr2[item+distIndex] -= arr1[item]
                    arr1[item]=0
                    distIndex-=1
            else:
                if not tempArr:
                    print "HATA PAYI GELDI : ", arr1[item]
                    break
                else:
                    distIndex = sorted(tempArr.keys())[0] - item       
    return mySum

N = 10000
firstTuple = (round(np.random.uniform(-5,5),2),round(np.random.uniform(0.5,1.5),2),N) # (Sigma,Mu,N)
secondTuple = (round(np.random.uniform(-5,5),2),round(np.random.uniform(0.5,1.5),2),N)  # (Sigma,Mu,N)
gaussArr1 = np.random.normal(*firstTuple)
gaussArr2 = np.random.normal(*secondTuple)
roundedArr1 = populate(gaussArr1)
roundedArr2 = populate(gaussArr2)
sumNumbers = float(N) # Because uniform distribution, sum(roundedArr1|2) == N
roundedArr1 = normalize(roundedArr1,sumNumbers)
roundedArr2 = normalize(roundedArr2,sumNumbers)

mySum = getDistance(roundedArr1.copy(),roundedArr2.copy())
print "My distance is :  " , mySum
plt.figure(1)
plt.title("My Histogram")
p1 = plt.bar(roundedArr1.keys(),roundedArr1.values(),1.0, color='g')
p2 = plt.bar(roundedArr2.keys(),roundedArr2.values(),1.0, color='r')
plt.show()




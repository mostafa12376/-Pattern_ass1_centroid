import os
import sys

from keras.datasets import mnist
from keras.utils.np_utils import to_categorical

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape(60000,28, 28)
test_images = test_images.reshape(10000,28, 28)
train_labels = to_categorical(train_labels, dtype ="uint8")
test_labels = to_categorical(test_labels, dtype ="uint8")

class Point:
  x = 0
  y = 0
  def __init__(self, x, y):
      self.x = x
      self.y = y

def getCentroid(block, Height, width):
    centre_x = 0
    centre_y = 0
    pixels = 0
    for i in range(width):
        for j in range(Height):
            centre_x = centre_x + i * block[i][j]
            centre_y = centre_y + j * block[i][j]
            pixels = pixels + block[i][j]
    centre_x = centre_x / pixels if pixels > 0 else 0
    centre_y = centre_y / pixels if pixels > 0 else 0
    return Point(int(centre_x) ,int(centre_y))

def makeBlock(img, ystart, xstart, blockHieght, blockwidth, samples):
    return [[  ( 0 if (( (ystart + yOnBlock) >= 28) or ((xstart + xOnBlock) >= 28) ) else (samples [img] [ystart + yOnBlock] [xstart + xOnBlock]) )  for yOnBlock in range(blockHieght)] for xOnBlock in range(blockwidth)]


def toInt(arr):
    l=0
    for i in arr:
        if (i == 1): return l
        l+=1



def generateFeatureVectors(y, x, samples, numSamples):
    blockHieght= int(28 / x)
    if( (28 % x) != 0): blockHieght+=1
    blockwidth= int(28 / y)
    if ((28 % y) != 0): blockwidth+=1
    numBlocks=  x*y
    featureVectorType = [0 for f in range(numBlocks * 2)]
    trainData= [featureVectorType for i in range(numSamples)]
    for img in range(numSamples):
        # print(img)
        if(numSamples==10000):
            if ((img+1)%(numSamples/100) == 0):
                print(end="\r")
                print(str(int((img+1)/(numSamples/100))) + "%", end="")
        featureVector = [0 for f in range(numBlocks * 2)]
        blockCounter=0
        ystart = 0
        while ystart<y :
            xstart = 0
            ystart+= 1
            while xstart<x :
                block = makeBlock(img, ystart*blockHieght, xstart*blockwidth, blockHieght, blockwidth, samples)
                point= getCentroid(block, blockHieght, blockwidth)
                featureVector[blockCounter*2]= point.x
                # print(featureVector[blockCounter*2])
                featureVector[(blockCounter * 2) +1] = point.y
                # print(featureVector[blockCounter * 2 +1])
                blockCounter+=1
                xstart+=1
        trainData[img]= featureVector
    if(numSamples==10000): print()
    return trainData

def printImgInfo(line, img):
    print("[ ", end=' ')
    for i in line: print(i, " ", end='')
    print("]", " -> ", toInt(train_labels[img]), sep='')

def printTrainData(trainData):
    img=0
    for line in trainData:
        printImgInfo(line, img)
        img+=1
        # print(line)


def saveData(numBlocks, dataToSave, numOfSamples,  d):
    if(numOfSamples==10000): fileName= 'trainData.txt'
    else: fileName= 'testData.txt'
    with open(fileName, 'w') as file:
        file.write(d)
    for img in range(numOfSamples):
        line = ''
        for i in range(numBlocks * 2): line += str(dataToSave[img][i]) + ' '
        line += '\n'
        with open(fileName, 'a') as file:
            file.write(line)

def retrieveData():
    trainData= []
    testData = []
    r=0
    print("retrieving")
    for l in trainDataFile:
        if(r):
            line_list= l.split()
            trainData.append(line_list)
            r+=1
    r=0
    for l in testDataFile:
        if(r):
            line_list= l.split()
            testData.append(line_list)
            r+=1
    return trainData, testData

def changeData():
    trainDataFile = open("trainData.txt", 'w')
    testDataFile = open("testData.txt", 'w')
    d=str(h)+ ","+ str(w)+ "\n"
    trainDataFile.write(d)
    testDataFile.write(d)
    #trainDataFile = open("trainData.txt", "r")
    print("training")
    trainData = generateFeatureVectors(h, w, train_images, 10000)
    print("testing")
    testData = generateFeatureVectors(h, w, test_images, 1000)
    saveData(numBlocks, trainData, 10000, d)
    saveData(numBlocks, testData, 1000, d)
    trainDataFile.close()
    return trainData, testData

def calculateAccuracy(trainData, testData):
    accuracyFile = open("accuracy.txt", 'w')
    d = str(h) + "," + str(w) + ","
    accuracyFile.write(d)
    accuracy=0
    test_counter = 0
    for v1 in testData:
        minDistance = sys.maxsize
        nearest= -1
        train_counter=0
        for v2 in trainData:
            currentDistance=0
            element_counter=0
            for element in trainData[train_counter]:
                currentDistance+= abs(int(element)-int(testData[test_counter][element_counter]))
                element_counter+=1
            if(currentDistance<minDistance):
                minDistance=currentDistance
                nearest= toInt(train_labels[train_counter])
            train_counter += 1
        if (nearest==toInt(test_labels[test_counter])): accuracy+=1
        test_counter+=1
        if(test_counter%10==0):
            print(end="\r")
            print(str(int(test_counter / 10)) + "%", end="")
    print()
    accuracy/=10 #(/10)==(*100/1000)
    accuracyFile = open("accuracy.txt", 'a')
    #print(1, accuracy)
    acc= str(accuracy)
    #print(2, acc)
    accuracyFile.write(acc)
    return accuracy


h = int(input("Enter number of blocks on height: "))
w = int(input("Enter number of blocks on width: "))

numBlocks= h * w
if os.path.isfile("trainData.txt" and "testData.txt"):
    trainDataFile = open("trainData.txt", "r")
    testDataFile = open("testData.txt", 'r')
    dimentions = trainDataFile.readline().split(",")
    dimentions[1]=dimentions[1][:-1]
    #print(dimentions[0] , str(h), dimentions[1] , str(w))
    if (dimentions[0] == str(h) and dimentions[1] == str(w)):
        trainData, testData = retrieveData()
    else:
        trainData, testData = changeData()
else:
    trainData, testData= changeData()
if os.path.isfile("accuracy.txt"):
    accuracyFile = open("accuracy.txt", "r")
    dimentions2 = accuracyFile.readline().split(",")
    if (dimentions2[0] == str(h) and dimentions2[1] == str(w)):
        #print(1)
        accuracy= dimentions2[2]
        accuracyFile.close()
    else:
        #print(2)
        accuracy= calculateAccuracy(trainData, testData)
        accuracyFile.close()
else:
    #print(3)
    accuracy= calculateAccuracy(trainData, testData)
print("Accuracy=", accuracy , "%", end="")

trainDataFile.close()
testDataFile.close()
# print(trainDataFile.read())
# printTrainData(trainData)




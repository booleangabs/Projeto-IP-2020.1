import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

d = lambda p,q: np.sqrt((q[0]-p[0])**2 + (q[0]-p[0])**2)

playerPos, playerColor = (1, 2), np.uint8([1, 0, 1])
occupationMap = np.uint8([[0, 1, 1, 1, 1, 1],
                          [0, 0, 0, 1, 1, 0],
                          [1, 1, 0, 0, 1, 0],
                          [1, 0, 0, 0, 0, 0],
                          [1, 0, 1, 0, 0, 0],
                          [1, 0, 1 ,0 ,0, 0]])
occupationImageA = cv2.merge([occupationMap, occupationMap, occupationMap]) 
occupationImageA[playerPos[0]][playerPos[1]] = playerColor

openSet = []
for i in range(len(occupationMap)):
    for j in range(len(occupationMap[0])):
        if i<=playerPos[0] and j<=playerPos[1] and occupationMap[i][j]==0 and (i,j)!=playerPos:
            occupationMap[i][j] = 1
        elif occupationMap[i][j] == 0 and (i,j)!=playerPos:
            openSet.append((i, j))
        else:
            pass
            

dropIn = []
nDrops = 3
for i in range(nDrops):
    weights = np.random.random(len(openSet))
    e_w = np.exp(weights)
    weights = e_w / e_w.sum()
    choice = random.choices(population=openSet, weights=weights, k=1)[0]
    idx = openSet.index(choice)
    openSet.pop(idx)
    dropIn.append(choice)


occupationImageB = cv2.merge([occupationMap, occupationMap, occupationMap])
for i, j in dropIn:
    occupationImageB[i][j] = np.uint8([0, 170, 0])
occupationImageB[playerPos[0]][playerPos[1]] = playerColor

patch = np.uint8([[[65,65,65]],
                  [[65,65,65]],
                  [[65,65,65]],
                  [[65,65,65]],
                  [[65,65,65]],
                  [[65,65,65]]])
plt.imshow(np.hstack([occupationImageA*255, patch, occupationImageB*255]))
plt.show()
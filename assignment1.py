import sys
from math import sqrt
import re

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1, p2):
    return sqrt(pow(float(p1[0])-float(p2[0]),2) + pow(float(p1[1])-float(p2[1]),2))

#Run the divide-and-conquor nearest neighbor
def nearest_neighbor(points):
    return nearest_neighbor_recursion(points)

#Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance=dist(points[0],points[1])
    for i in range(len(points)):
        j = i + 1
        while j< len(points):
            if(dist(points[i],points[j]) < min_distance):
                min_distance = dist(points[i],points[j])
                #print ("The points found are %s and %s and the distance is: %5.3f" %(points[i],points[j],min_distance))
            j = j + 1
    return min_distance

def nearest_neighbor_recursion(points):
    min_distance=0
    midPoints = []
    if(len(points) > 3):
        midpoint = len(points)/2
        minLeft = nearest_neighbor_recursion(points[:midpoint])
        minRight = nearest_neighbor_recursion(points[midpoint+1:])
        midValue = float(points[midpoint][0])
        if(minLeft < minRight):
            min_distance = minLeft
        else:
            min_distance = minRight
        for k in range(len(points)):
            if(float(points[k][0]) < midValue-min_distance or float(points[k][0]) > midValue + min_distance):
                midPoints.append(points[k])
        midPoints.sort(key = lambda midPoints: float(midPoints[1]))
        for i in range(len(midPoints)):
            j = 0
            while (j < 8 and j < len(midPoints)):
                if(dist(midPoints[i],midPoints[j]) < min_distance and i != j):
                    min_distance = dist(midPoints[i],midPoints[j])
                    #print ("The points found are %s and %s and the distance is: %5.3f" %(midPoints[i],midPoints[j],min_distance))
                j = j + 1
    else:
        min_distance = brute_force_nearest_neighbor(points)

    return min_distance

def read_file(filename):
    points=[]
    # File format
    # x1 y1
    # x2 y2
    # ...
    in_file=open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match=pointRE.match(line)
        if point_match:
            x = point_match.group(1)
            y = point_match.group(2)
            points.append((x,y))
    points.sort(key = lambda points: float(points[0]))
    #print(points)
    return points

def main(filename,algorithm):
    algorithm=algorithm[1:]
    points=read_file(filename)
    if algorithm =='dc':
        print("Divide and Conquer: ", nearest_neighbor(points))
    if algorithm == 'bf':
        print("Brute Force: ", brute_force_nearest_neighbor(points))
    if algorithm == 'both':
        print("Divide and Conquer: ", nearest_neighbor(points))
        print("Brute Force: ", brute_force_nearest_neighbor(points))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])

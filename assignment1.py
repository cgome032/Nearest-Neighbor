import sys
from math import sqrt
import re
import timeit

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

#Run the divide-and-conquor nearest neighbor
def nearest_neighbor(points):
    return nearest_neighbor_recursion(points)

#Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance=dist(points[0],points[1])
    for i in range(len(points)//2):
        j = i + 1
        while j< len(points):
            if(dist(points[i],points[j]) < min_distance):
                min_distance = dist(points[i],points[j])
            j = j + 1
    return min_distance

def nearest_neighbor_recursion(points):
    min_distance=0
    midPoints = []
    if(len(points) > 10):
        #midpoint = len(points)/2
        midpoint = len(points)//2
        minLeft = nearest_neighbor_recursion(points[:midpoint])
        minRight = nearest_neighbor_recursion(points[midpoint:])
        midValue = points[midpoint][0]
        if(minLeft < minRight):
            min_distance = minLeft
        else:
            min_distance = minRight
        for k in range(len(points)):
            if(points[k][0] > midValue-min_distance and points[k][0] < midValue + min_distance):
                midPoints.append(points[k])
        midPoints.sort(key = lambda midPoints: midPoints[1])
        for i in range(len(midPoints)):
            j = i + 1
            y = 0
            while (y < 7 and j < len(midPoints)):
                if(dist(midPoints[i],midPoints[j]) < min_distance and i != j):
                    min_distance = dist(midPoints[i],midPoints[j])
                    #print ("The points found are %s and %s and the distance is: %5.3f" %(midPoints[i],midPoints[j],min_distance))
                j = j + 1
                y = y + 1
    else:
        """
        if(len(points) == 2):
            min_distance = dist(points[0],points[1])
        else:
            min_distance1 = dist(points[0],points[1])
            min_distance2 = dist(points[0],points[2])
            min_distance3 = dist(points[1],points[2])
            if(min_distance1 <= min_distance2 and min_distance1 <= min_distance3):
                min_distance = min_distance1
            if(min_distance2 <= min_distance1 and min_distance2 <= min_distance3):
                min_distance = min_distance2
            if(min_distance3 <= min_distance1 and min_distance3 <= min_distance2):
                min_distance = min_distance3
        """
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
            x = float(point_match.group(1))
            y = float(point_match.group(2))
            points.append((x,y))
    points.sort(key = lambda points: points[0])
    #print(points)
    return points

def main(filename,algorithm):
    algorithm=algorithm[1:]
    points=read_file(filename)
    inputFile = filename[:-4]
    inputFile = inputFile + "_distance.txt"
    outputFile = open(inputFile,'w')
    if algorithm =='dc':
        start = timeit.default_timer()
        min_distance = nearest_neighbor(points)
        print("Divide and Conquer: ", min_distance)
        stop = timeit.default_timer()
        print(stop - start)
        outputFile.write(str(min_distance))
        outputFile.write('\n')

    if algorithm == 'bf':
        start = timeit.default_timer()
        min_distance = brute_force_nearest_neighbor(points)
        print("Brute Force: ", min_distance)
        stop = timeit.default_timer()
        print(stop-start)
        outputFile.write(str(min_distance))
    if algorithm == 'both':
        # Divide and Conquer method
        start = timeit.default_timer()
        min_distance = nearest_neighbor(points)
        print("Divide and Conquer: ", min_distance)
        stop = timeit.default_timer()
        print(stop - start)
        outputFile.write('Divide and Conquer: ')
        outputFile.write(str(min_distance))
        outputFile.write('\n')

        # Brute Force method
        start = timeit.default_timer()
        min_distance = brute_force_nearest_neighbor(points)
        print("Brute Force: ", min_distance)
        stop = timeit.default_timer()
        print(stop-start)
        outputFile.write('Brute Force: ')
        outputFile.write(str(min_distance))
        outputFile.write('\n')
    outputFile.close()
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])

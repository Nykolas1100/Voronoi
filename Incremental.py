import matplotlib.pyplot as plt
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []

class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

def midpt(l):
    return Point((l.x0 + l.x1)/2.0, (l.y0 + l.y1)/2.0)

def slope(l):
    if l.x1-l.x0 != 0:
        return float(l.y1-l.y0)/(l.x1-l.x0)
    else:
        return 0
def intercept(l):
    if slope(l) != 0:
        return l.y0 - (slope(l)*l.x0)
    elif l.y1-l.y0 == 0:
        return l.y0
    else:
        return l.x0
def intersect(l0, l1):
    if slope(l0) != slope(l1):
        return True
    elif slope(l0) == 0 and slope(l1) == 0:
        if (l0.x0 != l0.x1 and l1.y0 != l1.y1) or (l0.y0 != l0.y1 and l1.x0 != l1.x1):
            return True
    else:
        return False

def intersectAt(l0, l1):
    #get x and y
    if l0.x1-l0.x0 == 0:
        x = intercept(l0)
        y = (slope(l1)*x) + intercept(l1)
    elif l1.x1-l1.x0 == 0:
        x = intercept(l1)
        y = (slope(l0)*x) + intercept(l0)
    else:
        x = (intercept(l1)-intercept(l0))/float(slope(l0)-slope(l1))
        y = (slope(l0)*x) + intercept(l0)

    return Point(x, y)

def isInRegion(test, new):
    tx = float(test.x)
    ty = float(test.y)
    nx = float(new.x)
    ny = float(new.y)
    for edge in test.edges:
        #print(slope(edge)*tx+intercept(edge)-ty)
        #print(slope(edge)*nx+intercept(edge)-ny)
        if(slope(edge)*tx+intercept(edge)-ty > 0 and slope(edge)*nx+intercept(edge)-ny < 0):
            return False
        if(slope(edge)*tx+intercept(edge)-ty < 0 and slope(edge)*nx+intercept(edge)-ny > 0):
            return False
    return True

def isNeighbor(test, new):
    for edgeTest in test.edges:
        for edgeNew in new.edges:
            if(int(edgeTest.x0) == float(edgeNew.x0) and float(edgeTest.y0) == float(edgeNew.y0) and float(edgeTest.x1) == float(edgeNew.x1) and float(edgeTest.y1) == float(edgeNew.y1)):
                #print("True")
                return True
    #print("False")
    return False

def perpBis(x0, y0, x1, y1):
    if not x0 == x1 and not y0 == y1:
        l = Line(x0, y0, x1, y1)
        mid = midpt(l)
        negReciprocal = -1.0*(1.0/slope(l))
        p0 = Point(mid.x+1, mid.y+negReciprocal)
        p1 = Point(mid.x-1, mid.y-negReciprocal)
        return Line(p0.x, p0.y, p1.x, p1.y)
    elif x0 == x1:
        halfway = (y0 + y1)/2.0
        return Line(x0 - halfway, halfway, x1 + halfway, halfway)
    else:
        halfway = float((x0 + x1)/2.0)
        return Line(halfway, y1 - halfway, halfway, y0 + halfway)

def angleBetween(l0, l1):
    originx = float(l0.x0)
    originy = float(l0.y0)
    l0x = float(l0.x1)
    l0y = float(l0.y1)
    l1x = float(l1.x1)
    l1y = float(l1.y1)
    angle = math.degrees(math.atan2(l1y-originy, l1x-originx) - math.atan2(l0y-originy, l0x-originx))
    return abs(angle)

def swap(list, p1, p2):
    list[p1], list[p2] = list[p2], list[p1]

#take points as input
points = []
cont = True
print("Please enter integer coordinates, enter any character when done")
while cont:
    x = input("Enter your x value: ")
    if not x.isdigit():
        cont = False
        break
    y = input("Enter your y value: ")
    if not y.isdigit():
        cont = False
    else:
        points.append(Point(x,y))

#sort points by increasing x-val
for i in range(0, len(points)):
    for j in range(len(points)-1):
        if float(points[j].x) > float(points[j+1].x):
            swap(points, j, j+1)

count = 1
for z in points:
    print("Point number " + str(count) + ": (" + z.x + ", " + z.y + ")")
    count += 1

xcoords = []
ycoords = []

#plot points
for k in points:
    xcoords.append(int(k.x))
    ycoords.append(int(k.y))
plt.plot(xcoords, ycoords, "k.", ms = 15)
print(xcoords)
print(ycoords)

lines = []
voronoi = []
#create voronoi diagram with first two points
if len(points) > 1:
    x0 = float(points[0].x)
    y0 = float(points[0].y)
    x1 = float(points[1].x)
    y1 = float(points[1].y)
    perpbis = perpBis(x0, y0, x1, y1)
    points[0].edges.append(perpbis)
    points[1].edges.append(perpbis)
    lines.append(perpbis)
    #plt.axline((perpbis.x0, perpbis.y0), (perpbis.x1, perpbis.y1), linewidth = 3, color='b', linestyle = '-')

#increment through rest of points
for i in range(2, len(points)):
    #find which region the point is
    for j in range(i-1, -1, -1):
        #print("Calling isInRegion on: " + str(j) + " and " + str(i))
        if(isInRegion(points[j], points[i])):
            print("Point: " + str(i) + " is in region of site: " + str(j))
            xi = float(points[i].x)
            yi = float(points[i].y)
            xj = float(points[j].x)
            yj = float(points[j].y)
            #add bisector inside of region
            newBis = perpBis(xi, yi, xj, yj)
            points[i].edges = points[j].edges.copy()
            points[i].edges.append(newBis)
            points[j].edges.append(newBis)
            lines.append(newBis)
            #go through neighbors of region
            for k in range(i-1, -1, -1):
                xk = float(points[k].x)
                yk = float(points[k].y)
                #print("Calling isNeighbor on: " + str(k) + " and " + str(j))
                if(isNeighbor(points[k], points[j])):
                    bis = perpBis(xi, yi, xk, yk)
                    points[i].edges.append(bis)
                    points[k].edges.append(bis)
                    lines.append(bis)
                    #go through edges of neighbor
                    for z in range(len(lines)-2, -1, -1):
                        if intersect(lines[z], bis):
                            intersection = intersectAt(lines[z], bis)
                            vZ = Line(float(lines[z].x0), float(lines[z].y0), float(intersection.x), float(intersection.y))
                            v0 = Line(float(intersection.x), float(intersection.y), float(bis.x0), float(bis.y0))
                            v1 = Line(float(intersection.x), float(intersection.y), float(bis.x1), float(bis.y1))
                            voronoi.append(vZ)

                            if(not isInRegion(points[j], Point(float(bis.x0), float(bis.y0)))):
                                voronoi.append(v0)
                            if(not isInRegion(points[j], Point(float(bis.x1), float(bis.y1)))):
                                voronoi.append(v1)

#for line in lines:
#plt.plot([float(line.x0), float(line.x1)], [float(line.y0), float(line.y1)], "r-", ms = 15)
#for line in lines:
#plt.plot([float(line.x0), float(line.x1)], [float(line.y0), float(line.y1)], "r:", ms = 30)
for vor in voronoi:
    print("Line is: " + str(vor.x0) + ", " + str(vor.y0) + ", " + str(vor.x1) + ", " + str(vor.y1))
    plt.plot([float(vor.x0), float(vor.x1)], [float(vor.y0), float(vor.y1)], "k:", ms = 30)
plt.axis('equal')
plt.show()
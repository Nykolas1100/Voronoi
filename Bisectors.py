import matplotlib.pyplot as plt

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
    for edge in test.edges:
        if(slope(edge)*test.x+intercept(edge)-test.y > 0 and slope(edge)*new.x+intercept(edge)-new.y < 0):
            return False
        if(slope(edge)*test.x+intercept(edge)-test.y < 0 and slope(edge)*new.x+intercept(edge)-new.y > 0):
            return False
    return True

def isNeighbor(test, new):
    for edgeTest in test.edges:
        for edgeNew in new.edges:
            if(edgeTest.x0 == edgeNew.x0 and edgeTest.y0 == edgeNew.y0 and edgeTest.x1 == edgeNew.x1 and edgeTest.y1 == edgeNew.y1):
                return True
    return False

def swap(list, p1, p2):
    list[p1], list[p2] = list[p2], list[p1]

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

for i in range(0, len(points)-1):
    for j in range(len(points)-1):
        if points[j].x > points[j+1].x:
            swap(points, j, j+1)

count = 1
for z in points:
    print("Point number " + str(count) + ": (" + z.x + ", " + z.y + ")")
    count += 1

xcoords = []
ycoords = []

for k in points:
    xcoords.append(int(k.x))
    ycoords.append(int(k.y))

plt.plot(xcoords, ycoords, "k.", ms = 15)

lines = []

i = 0
if len(points) > 1:
    for i in range(0, len(points) - 1):
        for j in range(i+1, len(points)):

            x0 = int(points[i].x)
            y0 = int(points[i].y)
            x1 = int(points[j].x)
            y1 = int(points[j].y)
            if not x0 == x1 and not y0 == y1:
                l = Line(x0, y0, x1, y1)
                mid = midpt(l)
                negReciprocal = -1.0*(1.0/slope(l))
                p0 = Point(mid.x+1, mid.y+negReciprocal)
                p1 = Point(mid.x-1, mid.y-negReciprocal)
                lines.append(Line(p0.x, p0.y, p1.x, p1.y))
                #points[i].edges.append(Line(p0.x, p0.y, p1.x, p1.y))
                #points[j].edges.append(Line(p0.x, p0.y, p1.x, p1.y))
                plt.axline((p0.x, p0.y), (p1.x, p1.y), linewidth = 3, color='b', linestyle = ':')
            elif x0 == x1:
                halfway = (y0 + y1)/2.0
                lines.append(Line(x0 - halfway, halfway, x1 + halfway, halfway))
                #points[i].edges.append(Line(x0 - halfway, halfway, x1 + halfway, halfway))
                #points[j].edges.append(Line(x0 - halfway, halfway, x1 + halfway, halfway))
                plt.axline((x0 - halfway, halfway), (x1 + halfway, halfway), linewidth = 3, color='b', linestyle = ':')
            else:
                halfway = int((x0 + x1)/2.0)
                lines.append(Line(halfway, y1 - halfway, halfway, y0 + halfway))
                #points[i].edges.append(Line(halfway, y1 - halfway, halfway, y0 + halfway))
                #points[j].edges.append(Line(halfway, y1 - halfway, halfway, y0 + halfway))
                plt.axline((halfway, y1 - halfway), (halfway, y0 + halfway), linewidth = 3, color='b', linestyle = ':')

intersections = []
#print("There are " + str(len(lines)) + " lines")
for i in range(0, len(lines)-1):
    for j in range(i+1, len(lines)):
        l0 = lines[i]
        l1 = lines[j]
        if intersect(l0, l1):
            inter = intersectAt(l0, l1)
            intersections.append(inter)
            #print("Intersect is: (" + str(inter.x) + ", " + str(inter.y) + ")")
            plt.plot([inter.x], [inter.y], "r.", ms = 15)
        else:
            continue

plt.axis('equal')
plt.show()
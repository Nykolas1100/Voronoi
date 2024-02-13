import matplotlib.pyplot as plt
import math

"""
The algorithm first takes in points from the user and calculates the perpendicular bisectors between each pair of points.
Since all voronoi edges are perpendicular bisectors, the voronoi diagram is a subset of the perpendicular bisectors.
The algorithm then calculates the intersection points between all of the perpendicular bisectors.
Voronoi edges meet at voronoi vertices, so the voronoi vertices are a subset of the perpendicular bisector intersections.
The algorithm then divides all of the perpendicular bisectors into line segments separated by intersection points.
Unless all sites are collinear, the voronoi diagram will be composed of bounded line segments and infinite lines at unbounded regions.
For each line segment the algorithm calculates the distances to all of the voronoi vertices.
If the shortest two distances are equal then the line segment is added to the voronoi diagram.
Any point on a voronoi edge is equidistant to the sites that it separates.
By theorem 4.9 a circle centered on a voronoi edge and through the sites it separates does not contain any other sites.
As such, the closest two points to a point on a voronoi edge are the two sites that it separates.
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        #store points where line intersects with other lines
        self.intersections = []
        #store points of line being perpendicularly bisected
        self.pts = []

def midpt(l):
    return Point((l.x0 + l.x1)/2.0, (l.y0 + l.y1)/2.0)

def slope(l):
    if l.x1-l.x0 != 0.0:
        return (l.y1-l.y0)/(l.x1-l.x0)
    else:
        return 0.0

def intercept(l):
    if slope(l) != 0.0:
        return l.y0 - (slope(l)*l.x0)
    #if horizontal provide y-intercept
    elif l.y1-l.y0 == 0.0:
        return l.y0
    else:
    #if vertical provide x-intercept
        return l.x0

def intersect(l0, l1):
    #make sure lines are not parallel
    if slope(l0) != slope(l1):
        return True
    #if slope is zero make sure that lines are neither both vertical nor both horizontal
    elif slope(l0) == 0.0 and slope(l1) == 0.0:
        if (l0.x0 != l0.x1 and l1.y0 != l1.y1) or (l0.y0 != l0.y1 and l1.x0 != l1.x1):
            return True
    else:
        return False

def intersectAt(l0, l1):
    #if l0 is vertical then intersect at x-intercept
    if l0.x1-l0.x0 == 0.0:
        x = intercept(l0)
        y = (slope(l1)*x) + intercept(l1)
    #if l1 is vertical then intersect at x-intercept
    elif l1.x1-l1.x0 == 0.0:
        x = intercept(l1)
        y = (slope(l0)*x) + intercept(l0)
    else:
        x = (intercept(l1)-intercept(l0))/(slope(l0)-slope(l1))
        y = (slope(l0)*x) + intercept(l0)
    return Point(x, y)

def distance(p0, p1):
    return math.sqrt(math.pow(p1.x-p0.x, 2)+math.pow(p1.y-p0.y, 2))

#used to help sort lists
def swap(list, p0, p1):
    list[p0], list[p1] = list[p1], list[p0]

#loop to take input from user and store it as a list of point objects
points = []
cont = True
print("Please enter integer coordinates, enter any non-integer character when done")
while cont:
    x = input("Enter your x value: ")
    firstx = x[:1]
    if not x.isdigit() and firstx != "-":
        cont = False
        break
    y = input("Enter your y value: ")
    firsty = y[:1]
    if not y.isdigit() and firsty != "-":
        cont = False
    else:
        if firstx == "-" and firsty == "-":
            points.append(Point(float(x),float(y)))
        elif firstx == "-":
            points.append(Point(float(x),float(y)))
        elif firsty == "-":
            points.append(Point(float(x),float(y)))
        else:
            points.append(Point(float(x),float(y)))

#sort points by increasing x-value
for i in range(0, len(points)):
    for j in range(len(points)-1):
        if points[j].x > points[j+1].x:
            swap(points, j, j+1)

#print out all points
count = 1
for z in points:
    print("Point number " + str(count) + ": (" + str(int(z.x)) + ", " + str(int(z.y)) + ")")
    count += 1

#get x and y values for each point and store them in separate arrays
xcoords = []
ycoords = []
for k in points:
    xcoords.append(k.x)
    ycoords.append(k.y)

#plot all of the points as voronoi sites
plt.plot(xcoords, ycoords, "k.", ms = 15)

#find the perpendicular bisectors between all pairs of points and store in a list of lines
#uncomment the plt lines to see the perpendicular bisectors represented as infinite lines
lines = []
if len(points) > 1:
    for i in range(0, len(points) - 1):
        for j in range(i+1, len(points)):

            x0 = points[i].x
            y0 = points[i].y
            x1 = points[j].x
            y1 = points[j].y
            if not x0 == x1 and not y0 == y1:
                l = Line(x0, y0, x1, y1)
                mid = midpt(l)
                negReciprocal = -1.0*(1.0/slope(l))
                p0 = Point(mid.x+1.0, mid.y+negReciprocal)
                p1 = Point(mid.x-1.0, mid.y-negReciprocal)
                lines.append(Line(p0.x, p0.y, p1.x, p1.y))
                lines[len(lines)-1].pts.append(Point(x0,y0))
                lines[len(lines)-1].pts.append(Point(x1,y1))
                #plt.axline((p0.x, p0.y), (p1.x, p1.y), linewidth = 3, color='b', linestyle = ':')
            elif x0 == x1:
                halfway = (y0 + y1)/2.0
                lines.append(Line(x0 - halfway, halfway, x1 + halfway, halfway))
                lines[len(lines)-1].pts.append(Point(x0,y0))
                lines[len(lines)-1].pts.append(Point(x1,y1))
                #plt.axline((x0 - halfway, halfway), (x1 + halfway, halfway), linewidth = 3, color='b', linestyle = ':')
            else:
                halfway = (x0 + x1)/2.0
                lines.append(Line(halfway, y1 - halfway, halfway, y0 + halfway))
                lines[len(lines)-1].pts.append(Point(x0,y0))
                lines[len(lines)-1].pts.append(Point(x1,y1))
                #plt.axline((halfway, y1 - halfway), (halfway, y0 + halfway), linewidth = 3, color='b', linestyle = ':')

#find all intersections between perpendicular bisectors and store them as points along with the perpendicular bisectors
for i in range(0, len(lines)-1):
    for j in range(i+1, len(lines)):
        l0 = lines[i]
        l1 = lines[j]
        if intersect(l0, l1):
            inter = intersectAt(l0, l1)
            l0.intersections.append(inter)
            l1.intersections.append(inter)
            #print("Intersect is: (" + str(inter.x) + ", " + str(inter.y) + ")")
            #uncomment to print intersection points
            #plt.plot([inter.x], [inter.y], "r.", ms = 15)
        else:
            continue

#break apart each perpendicular bisector into segments separated by intersection points and store the segments in a list
segments = []
if len(lines) == 1:
    segments.append(lines[0])
elif len(lines) > 1:
    for l in lines:
        inters = l.intersections
        m = slope(l)
        #sort intersection points of a perpendicular bisector by increasing x-value
        for i in range(0, len(inters)):
            for j in range(len(inters)-1):
                if inters[j].x > inters[j+1].x:
                    swap(inters, j, j+1)
        for i in range(0, len(inters)):
            for j in range(len(inters)-1):
                if inters[j].x == inters[j+1].x and inters[j].y > inters[j+1].y:
                    swap(inters, j, j+1)
        #check if there are intersections and if there are then add the two segments on either end of a perpendicular bisector
        if (len(inters) == 0):
            segments.append(l)
        elif (l.x0 != l.x1):
            seg1 = Line(inters[0].x-5.0, inters[0].y-5.0*m, inters[0].x, inters[0].y)
            seg1.pts.append(l.pts[0])
            seg1.pts.append(l.pts[1])
            seg2 = Line(inters[len(inters)-1].x, inters[len(inters)-1].y, inters[len(inters)-1].x+5.0, inters[len(inters)-1].y+5.0*m)
            seg2.pts.append(l.pts[0])
            seg2.pts.append(l.pts[1])
            segments.append(seg1)
            segments.append(seg2)
        else:
            seg1 = Line(inters[0].x, inters[0].y-5.0, inters[0].x, inters[0].y)
            seg1.pts.append(l.pts[0])
            seg1.pts.append(l.pts[1])
            seg2 = Line(inters[len(inters)-1].x, inters[len(inters)-1].y, inters[len(inters)-1].x, inters[len(inters)-1].y+5.0)
            seg2.pts.append(l.pts[0])
            seg2.pts.append(l.pts[1])
            segments.append(seg1)
            segments.append(seg2)
        #add the segments in between intersection points of a perpendicular bisector
        for i in range(0, len(inters)-1):
            seg1 = Line(inters[i].x, inters[i].y, inters[i+1].x, inters[i+1].y)
            seg1.pts.append(l.pts[0])
            seg1.pts.append(l.pts[1])
            segments.append(seg1)

#find which segments are voronoi segments
voronoi = []
for seg in segments:
    mid = midpt(seg)
    distances = []
    #find the distances from the midpoint of a perpendicular bisector to all of the voronoi sites
    for point in points:
        distances.append(round(distance(mid, point), 5))
    #sort the distances in increasing order
    for i in range(0, len(distances)):
        for j in range(len(distances)-1):
            if distances[j] > distances[j+1]:
                swap(distances, j, j+1)
    #print(distances)
    #print("Line from: (" + str(seg.x0) + ", " + str(seg.y0) + ") to (" + str(seg.x1) + ", " + str(seg.y1) + ")")
    #if closest two voronoi sites are equidistant then segment is part of the voronoi diagram
    if(distances[0] == distances[1] == round(distance(mid, seg.pts[0]), 5)):
        voronoi.append(seg)
        #print("Line from: (" + str(seg.x0) + ", " + str(seg.y0) + ") to (" + str(seg.x1) + ", " + str(seg.y1) + ")")
        #print("First point: (" + str(seg.pts[0].x) + ", " + str(seg.pts[0].y) + ") Second point: (" + str(seg.pts[1].x) + ", " + str(seg.pts[1].y) + ")")

#plot all of the segments
#color = 1
#for seg in segments:
    #if(color%2 == 0):
        #plt.plot([seg.x0, seg.x1], [seg.y0, seg.y1], "c-", ms = 30)
    #else:
        #plt.plot([seg.x0, seg.x1], [seg.y0, seg.y1], "m-", ms = 30)
    #color += 1

#plot all of the voronoi segments
for vor in voronoi:
    plt.plot([vor.x0, vor.x1], [vor.y0, vor.y1], "r:", ms = 15)
    #print lines between adjacent sites to create the delaunay triangulation
    plt.plot([vor.pts[0].x, vor.pts[1].x], [vor.pts[0].y, vor.pts[1].y], "c:", ms = 15)

plt.axis('equal')
plt.show()
from math import sin, cos, pi, sqrt, atan2

from numpy import matrix

def distance(p1, p2):
    # basic vector norm
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return sqrt(dx * dx + dy * dy)


def total_length(point_list):
    # calculate the sum of the distances of all points along the drawn stroke
    p1 = point_list[0]
    length = 0.0

    for i in range(1, len(point_list)):
        length += distance(p1, point_list[i])
        p1 = point_list[i]

    return length


def resample(point_list, step_count=64):
    # resample the given stroke's list of points
    # represent the stroke with the amount of step_count points
    # save here the resampled points
    new_points = []

    # the sum of the distances of all points along the originally drawn stroke
    length = total_length(point_list)

    print(length)

    # the distance the resampled points have to each other
    step_size = length / (step_count - 1)

    print(step_size)

    # current position along the strong in regard of step_size (see below)
    current_pos = 0

    # add the first point of the original stroke to the point list
    new_points.append(point_list[0])

    # iterate the stroke's point list
    i = 1
    while i < len(point_list):
        p1 = point_list[i - 1]

        # calculate the distance of the current pair of points
        d = distance(p1, point_list[i])

        if current_pos + d >= step_size:
            # once we reach or step over our desired distance, we push our resampled point
            # to the correct position based on our stepsize
            nx = p1[0] + ((step_size - current_pos) / d) * \
                (point_list[i][0] - p1[0])
            ny = p1[1] + ((step_size - current_pos) / d) * \
                (point_list[i][1] - p1[1])

            # store the new data
            new_points.append([nx, ny])
            point_list.insert(i, [nx, ny])

            # reset curpos
            current_pos = 0
        else:
            current_pos += d

        i += 1

    return new_points

def rotate(points, center, angle_degree):
    new_points = []
    
    # represent our angle in radians
    angle_rad = angle_degree * (pi / 180)
    
    # define a 3x3 rotation matrix for clockwise rotation 
    rot_matrix = matrix([[cos(angle_rad), -sin(angle_rad), 0],
                         [sin(angle_rad),  cos(angle_rad), 0], 
                         [      0,               0,        1]])
    
    t1 = matrix([[1, 0, -center[0]], 
                 [0, 1, -center[1]],
                 [0, 0,     1     ]])
    
    t2 = matrix([[1, 0,  center[0]], 
                 [0, 1,  center[1]],
                 [0, 0,     1     ]])
    
    # create our actual transformation matrix which rotates a point of points around the center of points
    transform = t2  @ rot_matrix @ t1 # beware of the order of multiplications, not commutative!
    
    for point in points:
        
        # homogenous point of the point to be rotated
        hom_point = matrix([[point[0]], [point[1]], [1]])  
        
        # rotated point
        rotated_point = transform @ hom_point
        
        # storing
        new_points.append(( (rotated_point[0] / rotated_point[2]),float(rotated_point[1] / rotated_point[2])))
        
    return new_points

def centroid(points):
    xs, ys = zip(*points)
    
    return (sum(xs) / len(xs), sum(ys) / len(ys))

def angle_between(point, centroid):
    dx = centroid[0] - point[0]
    dy = centroid[1] - point[1]
    
    # return the angle in degrees
    return atan2(dy, dx) * 180 / pi 
    
    # assert(angle_between((-10, -10), (0,0)) == 45.0) 
    # some 'unit testing' whether the function does what it is supposed to do

def scale(points):
    # the desired interval size
    size = 100
    
    xs, ys = zip(*points)
    
    # minimum and maximum occurrences of x and y values of the points
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    
    # calculate the range of the coordinates of the points
    x_range = x_max - x_min
    y_range = y_max - y_min
    
    points_new = []
    
    # map the points to the desired interval
    for p in points:
        p_new = ((p[0] - x_min) * size / x_range,
                 (p[1] - y_min) * size / y_range)
        points_new.append(p_new)
        
    return points_new

def normalize(points):
    # use all the processing functions from above to transform our set of points into the desired shape
    points_new = resample(points)
    angle = -angle_between(points_new[0], centroid(points_new))
    points_new = rotate(points_new, centroid(points_new), angle)
    points_new = scale(points_new)
    
    return points_new

def calculate_similarity(sample, template):
    dist_all = 0
    for p1, p2 in zip(sample,template):
        dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        dist_all += dist
        
    return dist_all

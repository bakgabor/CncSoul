import math


def distance(first_position, second_position):
    dist = 0
    for index, position in enumerate(first_position):
        dist += math.pow(second_position[index] - position, 2)
    return math.sqrt(dist)


def point_and_line_collision(point, line_begin, line_end, buffer_num=0.1):
    line_len = distance(line_begin, line_end)
    first_dist = distance(point, line_begin)
    second_dist = distance(point, line_end)
    if line_len - buffer_num <= first_dist + second_dist <= line_len + buffer_num:
        return True
    return False


def line_center(line_begin, line_end):
    array = []
    for index, position in enumerate(line_begin):
        center_pos = position + line_end[index]
        array.append(center_pos/2)
    return array


def arc_radius(prev_x_axis, prev_y_axis, i_val, j_val):
    start_x = prev_x_axis
    start_y = prev_y_axis

    centreX = start_x + i_val
    centreY = start_y + j_val

    dxStart = start_x - centreX
    dyStart = start_y - centreY
    return math.sqrt((dyStart * dyStart) + (dxStart * dxStart))


def expand_arc(gCmd, prevXaxisVal, prevYaxisVal, xAxisVal, yAxisVal, iVal, jVal):
    arcMoveList = []
    dirn = 'CW'
    if gCmd in ['G03', 'G3']:
        dirn = 'CCW'

    startX = prevXaxisVal
    startY = prevYaxisVal

    centreX = startX + iVal
    centreY = startY + jVal

    # calculate angle to start point
    dxStart = startX - centreX
    dyStart = startY - centreY
    startAngle = math.atan2(dyStart, dxStart) #* 180 / math.pi

    # calculate angle to end point
    dxEnd = xAxisVal - centreX
    dyEnd = yAxisVal - centreY
    endAngle = math.atan2(dyEnd, dxEnd) #* 180 / math.pi

    # make sure direction works
    if endAngle > startAngle:
        endAngle = endAngle - (math.pi * 2)

    radius = math.sqrt((dyStart * dyStart) + (dxStart * dxStart))

    sweep = endAngle - startAngle
    if dirn == 'CCW':
        # for 'CW' sweep will be negative
        sweep = (math.pi * 2) + sweep

    # ~ arcLen = abs(sweep) * radius

    # ~ numSegments = int(arcLen / mD.arcSegmentLength)
    numSegments = int(abs(sweep / (math.pi * 2) * 30))

    for x in range(numSegments):
        fraction =  float(x) / numSegments
        stepAngle = startAngle + (sweep * fraction)
        stepX = centreX + math.cos(stepAngle) * radius
        stepY = centreY + math.sin(stepAngle) * radius
        if dirn == 'CW':
            if sweep > 0:
                stepY = - stepY
        else:
            if sweep < 0:
                stepY = - stepY
        arcMoveList.append([round(stepX,4), round(stepY,4)])

    arcMoveList.append([xAxisVal, yAxisVal])

    # ~ print("ArcList  STARTx %s   STARTy %s" %(startX, startY))
    # ~ for m in arcMoveList:
        # ~ print (m)
        # ~ pass
    # ~ print ("--------\n")
    return arcMoveList

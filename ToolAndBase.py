# Tool and Base Generator V0.1

from warnings import catch_warnings
from vcCommand import *
import vcMatrix, vcVector, vcKinObject
import random
import math

app = getApplication()
cmd = getCommand()  #
cmd.Name = "ToolAndBase"

def OnStart():
    global program

    program = getProgram() #
    if not program:
        app.messageBox("No program selected, aborting.","Warning",VC_MESSAGE_TYPE_WARNING,VC_MESSAGE_BUTTONS_OK)
        return

    controller = program.Executor.Controller
    createProperties()
    executeInActionPanel()

def getProgram():
    teachcontext = app.TeachContext

    if teachcontext.ActiveRobot:
        executors = teachcontext.ActiveRobot.findBehavioursByType(VC_ROBOTEXECUTOR)

    if executors:
        return executors[0].Program

    return None

def createProperties():
    global all_props
    global genButton

    # createRestrainedProperty(VC_STRING, 'Flow', 'XYZ', ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZYX', 'ZXY'])

    createProperty(VC_REAL, 'Start X', None, None)
    createProperty(VC_REAL, 'Start Y', None, None)
    createProperty(VC_REAL, 'Start Z', None, None)
    createProperty(VC_REAL, 'X Travel', None, None)
    createProperty(VC_REAL, 'Y Travel', None, None)
    createProperty(VC_REAL, 'Z Travel', None, None)
    createProperty(VC_REAL, 'Min Distance', None, None)
    # createProperty(VC_INTEGER, 'X Sections', None,  None)
    # createProperty(VC_INTEGER, 'Y Sections', None, None)
    # createProperty(VC_INTEGER, 'Z Sections', None, None)
    # createProperty(VC_REAL, 'Rx', None, None)
    # createProperty(VC_REAL, 'Ry', None, None)
    # createProperty(VC_REAL, 'Rz', None, None)
    createProperty(VC_REAL, 'Speed', None, None)
    createRestrainedProperty(VC_STRING, 'Move Type', 'Linear', ['Linear', 'Joint'])
    # createProperty(VC_STRING, 'Point Name', 'P', None)

    genButton = createProperty(VC_BUTTON, 'Generate', None, callGenerator)

    all_props = [x for x in cmd.Properties]

def createProperty(type, name, defaultValue, callback):
    prop = cmd.getProperty(name)
    if prop == None:
        prop = cmd.createProperty(type, name)

    if defaultValue:
        prop.Value = defaultValue

    if callback:
        prop.OnChanged = callback

    return prop

def createPropertyOld(type, name, defaultValue, callback):
    prop = cmd.getProperty(name)
    if prop:
        return prop

    prop = cmd.createProperty(type, name)

    if defaultValue:
        prop.Value = defaultValue

    if callback:
        prop.OnChanged = callback

    return prop

def createRestrainedProperty(type, name, defaultValue, constraints):
    prop = cmd.getProperty(name)
    if prop:
        return prop

    prop = cmd.createProperty(type, name, VC_PROPERTY_STEP)
    prop.StepValues = constraints

    if defaultValue:
        prop.Value = defaultValue

    return prop

def callGenerator(arg = None):
    global all_props

    print 'Generating...'

    routine = app.TeachContext.ActiveRoutine
    routine.clear()

    moveType = cmd.getProperty('Move Type').Value


    addMesCall = False

    startX = cmd.getProperty('Start X').Value
    startY = cmd.getProperty('Start Y').Value
    startZ = cmd.getProperty('Start Z').Value

    xTravel = cmd.getProperty('X Travel').Value
    yTravel = cmd.getProperty('Y Travel').Value
    zTravel = cmd.getProperty('Z Travel').Value

    minDist = cmd.getProperty('Min Distance').Value

    # xSections = cmd.getProperty('X Sections').Value
    # ySections = cmd.getProperty('Y Sections').Value
    # zSections = cmd.getProperty('Z Sections').Value

    # xStep = xTravel / xSections
    # yStep = yTravel / ySections
    # zStep = zTravel / zSections

    p1 = (startX, startY, startZ)
    p2 = ((startX + xTravel), (startY + yTravel), (startZ + zTravel))

    index = 0

    point_list = []
    selected_points = []

    while len(selected_points) <= 14:
        point = GeneratePoint(p1, p2)
        point_list.append(point)

        if checkPoint(point, point_list, minDist, 0):
            selected_points.append(point)

        # for p in point_list:
        #     if distance(p, point) > minDist:
        #         if point not in selected_points:
        #             print "distance: ", distance(p, point)
        #             selected_points.append(point)
        #             point_count += 1
        #     else:
        #         break

    path = FindShortestPath(selected_points)
    # print(path)

    print("printing points...")
    for points in path:
        index += 1
        # print(f"p{index} {points}")
        addPosition(routine, moveType, str(index), points[0], points[1], points[2], addMesCall)

    all_props = None
    app.render()
    print 'Done.'

def addPosition(routine, moveType, name, x, y, z, addMesCall):
    speed = cmd.getProperty('Speed').Value
    rx = 180 + random.randrange(-45, 45)
    ry = 0 + random.randrange(-45, 45)
    rz = 0 + random.randrange(-45, 45)

    m = vcMatrix.new()
    m.translateAbs(x, y, z)
    m.setWPR(rx, ry, rz)

    stat = None
    if moveType == 'Linear':
        stat = routine.addStatement(VC_STATEMENT_LINMOTION)
    else:
        stat = routine.addStatement(VC_STATEMENT_PTPMOTION)

    stat.readIn()
    stat.Positions[0].Name = name
    stat.Positions[0].PositionInReference = m
    stat.AccuracyMethod = VC_MOTIONTARGET_AM_DISTANCE
    stat.AccuracyValue = 0.0

    if moveType == 'Linear':
        stat.MaxSpeed = speed
    else:
        clampedSpeed = max(min(speed, 100.0), 0.0)
        stat.JointSpeed = clampedSpeed / 100.0

    if addMesCall:
        stat = routine.addStatement(VC_STATEMENT_COMMENT)
        stat.Comment = 'USR_CMD GRID_MEASURE()'

def GeneratePoint(start, end):

    x = random.randrange(start[0], end[0])
    y = random.randrange(start[1], end[1])
    z = random.randrange(start[2], end[2])

    point = (x, y, z)
    return point

# Nearest Neighbour Algorithm
def FindShortestPath(listOfPoints):
    current_point = listOfPoints[0]
    ordered_path = [current_point]
    unvisited_points = listOfPoints[1:]

    while unvisited_points:
        nearest_point = min(unvisited_points, key=lambda point: distance(current_point, point))
        ordered_path.append(nearest_point)
        current_point = nearest_point
        unvisited_points.remove(nearest_point)

    ordered_path.append(ordered_path[0])

    return ordered_path

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) **2)

def checkPoint(point, point_list, minDist, index):
    if index > len(point_list):
        return False
    try:
        if distance(point_list[index], point) < minDist:
            checkPoint(point, point_list, minDist, (index + 1))

        # print "distance: ", distance(point_list[index], point)
        else:
            return True

    except:
        print "Index out of range"
        return False
    
import math

def statefulPathFinding(playerPosition, blockPosition, blockStatus, characterState);
    path = []
    time = 0
    playerSpeedHorizontal = 2
    playerSpeedVertical = 1

    reachableVertex = [playerPosition]

    return (path, time)

# direction represents vertical or horizontal, 0=horizontal, 1=vertical
def movementTimeDistance(direction, start, end):
    time = 0
    distance = 0
    # Horizontal
    if direction == 0:
        distance = euclidean_distance(start, end)
        time = distance / 2
    # Vertical
    else:
        distance = end[2] - start[2]
        time = distance
    
    return time, distance

def inspectNeighbour(vertex, fSafe):
    x = vertex[0]
    y = vertex[1]
    z = vertex[2]

    jumpAbility = 1
    # Examine in descending order of z
    for i in range((z-fSafe), (z+jumpAbility+1), -1):
        # 4 neighbours
        n1 = (x-1, y, i)
        n2 = (x+1, y, i)
        n3 = (x, y-1, i)
        n4 = (x, y+1, i)
    #TODO


def euclidean_distance(start, end):
    x1 = start[0]
    y1 = start[1]
    z1 = start[2]
    x2 = end[0]
    y2 = end[0]
    z2 = end[0]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

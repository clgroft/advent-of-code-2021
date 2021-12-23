TYPE_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOMS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}


def solution(day, lines):
    data = tuple(tuple(line.rstrip()) for line in lines)
    print(f'Part 1: {checkState(data)}')
    print(f'Part 2: {checkState(extend(data))}')


CACHE : dict[tuple[tuple[str]], int] = {}
def checkState(data):
    cached = CACHE.get(data)
    if cached is not None: return cached

    if roomsComplete(data): return 0

    result = None
    for y in range(1, len(data)):
        for x in range(1, len(data[y])):
            if not isAmphipod(data, x, y) or not canMove(data, x, y):
                continue
            room = ROOMS[data[y][x]]
            if hasRoomAvailable(data, x, y) and isPathEmpty(data, x, room):
                d, c = move(data, x, y, room, moveInPos(data, room))
                cost = checkState(d)
                if cost >= 0 and (result is None or c + cost < result):
                    result = c + cost
            elif isInAnyRoom(y):
                for i in stoppable(data):
                    if isPathEmpty(data, x, i):
                        d, c = move(data, x, y, i, 1)
                        cost = checkState(d)
                        if cost >= 0 and (result is None or c + cost < result):
                            result = c + cost

    if result is None: result = -1
    CACHE[data] = result
    return result


def extend(data):
    return (*data[:3], (*"  #D#C#B#A#",), (*"  #D#B#A#C#",), *data[3:],)


def roomsComplete(data):
    return all(isRoomComplete(data, x) for x in (3, 5, 7, 9))


def isAmphipod(data, x, y):
    return data[y][x] in ('A', 'B', 'C', 'D')


def canMove(data, x, y):
    return ((not isInOwnRoom(data, x, y) or isBlockingRoom(data, x, y)) and
            not isBlockedInRoom(data, x, y))


def stoppable(data):
    return [i for i in range(1, len(data[0])-1) if i not in [3,5,7,9]]


def isInOwnRoom(data, x, y):
    return ROOMS.get(data[y][x]) == x


def isInAnyRoom(y):
    return y > 1


def isRoomComplete(data, x):
    return all(isInOwnRoom(data, x, y) for y in range(2, len(data) - 1))


def isEmpty(data, x, y):
    return data[y][x] == '.'


def isRoomEmpty(data, x):
    return all(isEmpty(data, x, y) for y in range(2, len(data) - 1))


def isBlockingRoom(data, x, y):
    return any(isAmphipod(data, x, j) and not isInOwnRoom(data, x, j)
               for j in range(y+1, len(data) - 1))


def hasRoomAvailable(data, x, y):
    room = ROOMS[data[y][x]]
    return (isRoomEmpty(data, room) or
            all(isEmpty(data, room, y) or isInOwnRoom(data, room, y)
                for y in range(2, len(data) - 1)))


def isPathEmpty(data, x, targetX):
    while x != targetX:
        if x > targetX: x -= 1
        if x < targetX: x += 1
        if not isEmpty(data, x, 1): return False
    return True


def isBlockedInRoom(data, x, y):
    return y >= 3 and not isEmpty(data, x, y-1)


def moveInPos(data, room):
    return next(y for y in range(len(data) - 2, 1, -1) if isEmpty(data, room, y))


def moveCost(data, x, y, i, j):
    return ((y-1) + abs(x-i) + (j-1)) * TYPE_COST[data[y][x]]


def move(d, x, y, i, j):
    data = list(list(row) for row in d)
    data[y][x] = d[j][i]
    data[j][i] = d[y][x]
    data = tuple(tuple(row) for row in data)
    return (data, moveCost(d, x, y, i, j))

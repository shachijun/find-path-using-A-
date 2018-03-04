import environment
import heapq
from Tkinter import *

Step = [[1 for x in range(environment.w)] for y in range(environment.l)]
Plan = [[1 for x in range(environment.w)] for y in range(environment.l)]
sx = environment.sx
sy = environment.sy
gx = environment.gx
gy = environment.gy
Step[gy][gx] = 4
Step[sy][sx] = 3
Plan[gy][gx] = 4
Plan[sy][sx] = 3
MOVE = []  # left 1 right 2 top 3 down 4
BLOCKED = []
counter = 0

# prepare for A*
search = [[1 for x in range(environment.w)] for y in range(environment.l)]
# initialize search value for all cells to be zero
for i in range(environment.l):
    for j in range(environment.w):
        search[i][j] = 0
left = [sy, sx - 1]
right = [sy, sx + 1]
up = [sy - 1, sx]
down = [sy + 1, sx]
surrounding = [left, right, up, down]
# initialize Step and Plan arrays to be zero
for sur in surrounding:
    if 0 <= sur[0] < environment.l and 0 <= sur[1] < environment.w:
        if environment.Matrix[sur[0]][sur[1]] == 0:
            Step[sur[0]][sur[1]] = 0
            Plan[sur[0]][sur[1]] = 0



def run_once():
    global Step, Plan, gx, gy, counter, search
    # each execution of the loop is a backward A* search and one execution
    tree = [[0 for tx in range(environment.w)] for ty in range(environment.l)]
    gva = [[-1 for gvx in range(environment.w)] for gvy in range(environment.l)]
    hva = [[-1 for hvx in range(environment.w)] for hvy in range(environment.l)]
    fva = [[-1 for fvx in range(environment.w)] for fvy in range(environment.l)]
    counter = counter + 1
    gva[gy][gx] = 0
    search[gy][gx] = counter
    gva[sy][sx] = float('inf')
    search[sy][sx] = counter
    openlist = []
    heapq.heapify(openlist)
    closedlist = []
    hva[gy][gx] = abs(sx-gx) + abs(sy-gy)
    hva[sy][sx] = 0
    fva[gy][gx] = gva[gy][gx] + hva[gy][gx]
    heapq.heappush(openlist, (fva[gy][gx], gy, gx))
    # call computepath
    search, counter, gva, hva, fva, tree, openlist, closedlist = computepath(search, counter, gva, hva, fva, tree, openlist, closedlist)
    print "called computepath"






def computepath(search, counter, gva, hva, fva, tree, openlist, closedlist):
    global Step, Plan, MOVE
    if not openlist:
        return
    while gva[sy][sx] > openlist[0][0]:
        expands = heapq.heappop(openlist)
        closedlist.append(expands)
        left = [expands[1], expands[2] - 1]
        right = [expands[1], expands[2] + 1]
        up = [expands[1] - 1, expands[2]]
        down = [expands[1] + 1, expands[2]]
        action = [left, right, up, down]
        for a in action:
            if 0 <= a[0] < environment.l and 0 <= a[1] < environment.w:
                if Step[a[0]][a[1]] == 0:
                    continue
                if search[a[0]][a[1]] < counter:
                    gva[a[0]][a[1]] = float('inf')
                    search[a[0]][a[1]] = counter
                if gva[a[0]][a[1]] > gva[expands[1]][expands[2]] + 1:
                    tree[a[0]][a[1]] = [expands[1], expands[2]]
                    for node in openlist:
                        if node[1] == a[0] and node[2] == a[1]:
                            openlist.remove(node)
                    gva[a[0]][a[1]] = gva[expands[1]][expands[2]] + 1
                    hva[a[0]][a[1]] = abs(sy - a[0]) + abs(sx - a[1])
                    fva[a[0]][a[1]] = gva[a[0]][a[1]] + hva[a[0]][a[1]]
                    heapq.heappush(openlist, (fva[a[0]][a[1]], a[0], a[1]))

    # store planned path in Plan array
    curx = sx
    cury = sy
    planstep = tree[cury][curx]

    while 1:
        if cury == gy and curx == gx:
            break
        nxty = planstep[0]
        nxtx = planstep[1]
        if nxty == cury:
            if nxtx == curx - 1:  # left
                MOVE.append(1)
            elif nxtx == curx + 1:  # right
                MOVE.append(2)
        elif nxtx == curx:
            if nxty == cury - 1:  # up
                MOVE.append(3)
            elif nxty == cury + 1:  # down
                MOVE.append(4)
        cury = nxty
        curx = nxtx
        Plan[nxty][nxtx] = 5
        planstep = tree[nxty][nxtx]
    print MOVE
    return search, counter, gva, hva, fva, tree, openlist, closedlist


def main():
    print "backward called!"
    # prepare for A*
    global Step, Plan, sx, sy, gx, gy
    counter = 0
    search = [[1 for x in range(environment.w)] for y in range(environment.l)]
    # initialize search value for all cells to be zero
    for i in range(environment.l):
        for j in range(environment.w):
            search[i][j] = 0
    left = [sy, sx - 1]
    right = [sy, sx + 1]
    up = [sy - 1, sx]
    down = [sy + 1, sx]
    surrounding = [left, right, up, down]
    # initialize Step and Plan arrays to be zero
    for sur in surrounding:
        if 0 <= sur[0] < environment.l and 0 <= sur[1] < environment.w:
            if environment.Matrix[sur[0]][sur[1]] == 0:
                Step[sur[0]][sur[1]] = 0
                Plan[sur[0]][sur[1]] = 0

    # each execution of the loop is a backward A* search and one execution
    while sx != gx or sy != gy:
        tree = [[0 for tx in range(environment.w)] for ty in range(environment.l)]
        gva = [[-1 for gvx in range(environment.w)] for gvy in range(environment.l)]
        hva = [[-1 for hvx in range(environment.w)] for hvy in range(environment.l)]
        fva = [[-1 for fvx in range(environment.w)] for fvy in range(environment.l)]
        counter = counter + 1
        gva[gy][gx] = 0
        search[gy][gx] = counter
        gva[sy][sx] = float('inf')
        search[sy][sx] = counter
        openlist = []
        heapq.heapify(openlist)
        closedlist = []
        hva[gy][gx] = abs(sx-gx) + abs(sy-gy)
        hva[sy][sx] = 0
        fva[gy][gx] = gva[gy][gx] + hva[gy][gx]
        heapq.heappush(openlist, (fva[gy][gx], gy, gx))

        # call computepath
        search, counter, gva, hva, fva, tree, openlist, closedlist = computepath(search, counter, gva, hva, fva, tree, openlist, closedlist)
        print "called computepath"

        if not openlist:
            print "I cannot reach the target"
            return

        # store planned path in Plan array
        planstep = tree[sy][sx]
        curx = sx
        cury = sy
        while 1:
            if planstep[0] == gy and planstep[1] == gx:
                break
            nxty = planstep[0]
            nxtx = planstep[1]
            if nxty == cury:
                if nxtx == curx - 1: # left
                    MOVE.append(1)
                elif nxtx == curx + 1: # right
                    MOVE.append(2)
            elif nxtx == curx:
                if nxty == cury - 1: # up
                    MOVE.append(3)
                elif nxty == cury + 1: # down
                    MOVE.append(4)
            cury = nxty
            curx = nxtx
            Plan[nxty][nxtx] = 5
            planstep = tree[nxty][nxtx]

        # draw planned path
        print "Plan: "
        for i in range(environment.l):
            print Plan[i]
        # execute planned path
        nextstep = tree[sy][sx]
        while environment.Matrix[nextstep[0]][nextstep[1]] != 0:
            Step[sy][sx] = 1
            sy = nextstep[0]
            sx = nextstep[1]
            Step[sy][sx] = 3
            if sy == gy and sx == gx:
                print "I reached the target"
                return
            nextstep = tree[sy][sx]
        # see if agent blocked
        if environment.Matrix[nextstep[0]][nextstep[1]] == 0:
            print "Blocked: "
            Step[nextstep[0]][nextstep[1]] = 0
            for i in range(environment.l):
                print Step[i]
            # empty plan array, prepare to repeat backward A*
            Plan = [[1 for x in range(environment.w)] for y in range(environment.l)]
            Plan[gy][gx] = 4
            Plan[sy][sx] = 3

    print "I reached the target"
    return


if __name__ == '__main__': main()


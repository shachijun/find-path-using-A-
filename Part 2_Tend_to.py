import environment


Step = [[1 for x in range(environment.w)] for y in range(environment.l)]

stepx = environment.sx
stepy = environment.sy
Step[environment.gy][environment.gx] = 4
Step[stepy][stepx] = 3

gva = 0
fva = [float('inf'), float('inf'), float('inf'), float('inf')]

if stepx - 1 >= 0:                                                                                                   #left
    if environment.Matrix[stepy][stepx - 1] == 0:
        Step[stepy][stepx - 1] = 0
    else:
        hva = abs(environment.gx - (stepx - 1)) + abs(environment.gy - stepy)
        Step[stepy][stepx - 1] = [gva + 1, hva, hva + gva + 1]
        fva[0] = hva + gva + 1

if stepx + 1 < environment.w:                                                                                       #right
    if environment.Matrix[stepy][stepx + 1] == 0:
        Step[stepy][stepx + 1] = 0
    else:
        hva = abs(environment.gx - (stepx + 1)) + abs(environment.gy - stepy)
        Step[stepy][stepx + 1] = [gva + 1, hva, hva + gva + 1]
        fva[1] = hva + gva + 1

if stepy - 1 >= 0:                                                                                                  #up
    if environment.Matrix[stepy-1][stepx] == 0:
        Step[stepy-1][stepx] = 0
    else:
        hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy - 1))
        Step[stepy - 1][stepx] = [gva + 1, hva, hva + gva + 1]
        fva[2] = hva + gva + 1

if stepy + 1 < environment.l:                                                                                       #down
    if environment.Matrix[stepy+1][stepx] == 0:
        Step[stepy + 1][stepx] = 0
    else:
        hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy + 1))
        Step[stepy + 1][stepx] = [gva + 1, hva, hva + gva + 1]
        fva[3] = hva + gva + 1
locat = fva.index(min(fva))

if locat == 0:                                                                                                      #left
    stepx -= 1
    print "Move Left"

elif locat == 1:                                                                                                    #right
    stepx += 1
    print "Move Right"

elif locat == 2:                                                                                                    # up
    stepy -= 1
    print "Move UP"

else:                                                                                                               # down
    stepy += 1
    print "Move DOWN"

while stepx != environment.gx or stepy != environment.gy:
    fva = [float('inf'), float('inf'), float('inf'), float('inf')]
    gva += 1
    if stepx - 1 >= 0:  # left
        if Step[stepy][stepx - 1] != 0 and Step[stepy][stepx - 1] != 3:
            hva = abs(environment.gx - (stepx - 1)) + abs(environment.gy - stepy)
            Step[stepy][stepx - 1] = [gva + 1, hva, hva + gva + 1]
            fva[0] = hva + gva + 1

    if stepx + 1 < environment.w:  # right
        if Step[stepy][stepx + 1] != 0 and Step[stepy][stepx + 1] != 3:
            hva = abs(environment.gx - (stepx + 1)) + abs(environment.gy - stepy)
            Step[stepy][stepx + 1] = [gva + 1, hva, hva + gva + 1]
            fva[1] = hva + gva + 1

    if stepy - 1 >= 0:  # up
        if Step[stepy - 1][stepx] != 0 and  Step[stepy - 1][stepx] != 3:
            hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy - 1))
            Step[stepy - 1][stepx] = [gva + 1, hva, hva + gva + 1]
            fva[2] = hva + gva + 1

    if stepy + 1 < environment.l:  # down
        if Step[stepy + 1][stepx] != 0 and Step[stepy + 1][stepx] != 3:
            hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy + 1))
            Step[stepy + 1][stepx] = [gva + 1, hva, hva + gva + 1]
            fva[3] = hva + gva + 1
    locat = fva.index(min(fva))

    if locat == 0:  # left
        stepx -= 1
        print "Move Left"

    elif locat == 1:  # right
        stepx += 1
        print "Move Right"

    elif locat == 2:  # up
        stepy -= 1
        print "Move UP"

    else:  # down
        stepy += 1
        print "Move DOWN"

for i in range(environment.l):
    for j in range(environment.w):
        print format(Step[i][j], " ^20"),
    print

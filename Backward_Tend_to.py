import environment

def findMinG(dic,x,y): # get min of g values of surrounding points
    a,b,c,d=float('inf'),float('inf'),float('inf'),float('inf')
    if dic.has_key((x-1,y)): # if dic has left point
        a = dic.get((x-1,y)) # get g value of left point
    if dic.has_key((x + 1, y)): # if dic has right point
        b=dic.get((x + 1, y)) # get g value of right point
    if dic.has_key((x, y - 1)): # if dic has up point
        c=dic.get((x , y - 1)) # get g value of up point
    if dic.has_key((x, y + 1)): # if dic has down point
        d=dic.get((x, y + 1)) # get g value of down point
    gv = min(a,b,c,d) # min of 4 g value
    return gv

def replaceL(List,x,y,gva,dic): # update f value g value of node in open list
    for i in range(len(List)):
        if List[i][3] == x and List[i][4] == y: # search point already in open list
            if gva < List[i][1]: # if g value of search point becomes smaller
                hva = List[i][2] # h still manhattan distance
                List[i] = [gva + hva, gva, hva, x, y] # update f value and g value of search point in open list
                dic[x, y]=gva # update g value of search point
    return List,dic

def getPath(moves, x, y):
    indexl = len(moves) - 1  # index of last move
    MOVE = []
    for i in reversed(range(len(moves))):  # no need to reverse since i is not used in the body
        MOVE.append(moves[indexl])  # last move lm
        indexa, indexb, indexc, indexd = float('inf'), float('inf'), float('inf'), float('inf')  # four infinity
        if [moves[indexl][0] - 1, moves[indexl][1]] in moves:  # if left point of lm in MOVE
            indexa = moves.index([moves[indexl][0] - 1, moves[indexl][1]])  # get index of left point -> indexa
        if [moves[indexl][0], moves[indexl][1] - 1] in moves:  # if up point of lm in MOVE
            indexb = moves.index([moves[indexl][0], moves[indexl][1] - 1])  # get index of up point -> indexb
        if [moves[indexl][0] + 1, moves[indexl][1]] in moves:  # if right point of lm in MOVE
            indexc = moves.index([moves[indexl][0] + 1, moves[indexl][1]])  # get index of right point -> indexc
        if [moves[indexl][0], moves[indexl][1] + 1] in moves:  # if down point of lm in MOVE
            indexd = moves.index([moves[indexl][0], moves[indexl][1] + 1])  # get index of down point -> indexd
        # if any of left right up down point of lm is current position of agent, stop
        if [moves[indexl][0] - 1, moves[indexl][1]] == [x, y] \
                or [moves[indexl][0], moves[indexl][1] - 1] == [x, y] \
                or [moves[indexl][0] + 1, moves[indexl][1]] == [x, y] \
                or [moves[indexl][0], moves[indexl][1] + 1] == [x, y]:
            MOVE.append([x,y])
            break
        indexl = min(indexa, indexb, indexc, indexd)
        if indexl == float('inf'):
            break
    MOVE = list(reversed(MOVE))
    return MOVE

class TendTo:
    def __init__(self,startx,starty,Step):
        self.startx = startx # currx and curry
        self.starty = starty
        self.Step=Step


    def imaginemove(self):
        List=[]
        CheckDup=[]
        checkEX=self.startx # current position of agent
        checkEY=self.starty
        stepx = environment.gx # start A* search at goal
        stepy = environment.gy
        CheckDup.append([stepx, stepy])
        dictionary={} # store g value
        dictionary[stepx,stepy]=0 # g value of goal is 0
        MOVE = []
        MOVE.append([environment.gx,environment.gy])
        expanded=[]
        if stepx == checkEX and stepy == checkEY: ## if == environment.sy sx
            return MOVE, self.Step, True
        # update block info around current position of agent
        if checkEX - 1 >= 0:                                                                                                   #left of curr
            if environment.Matrix[checkEY][checkEX - 1] == 0:
                self.Step[checkEY][checkEX - 1] = 0
        if checkEX + 1 < environment.w:                                                                                       #right
            if environment.Matrix[checkEY][checkEX + 1] == 0:
                self.Step[checkEY][checkEX + 1] = 0
        if checkEY - 1 >= 0:                                                                                                  #up
            if environment.Matrix[checkEY-1][checkEX] == 0:
                self.Step[checkEY-1][checkEX] = 0
        if checkEY + 1 < environment.l:                                                                                       #down
            if environment.Matrix[checkEY+1][checkEX] == 0:
                self.Step[checkEY + 1][checkEX] = 0

        while stepx != checkEX or stepy != checkEY:  ## search point != current position of agent
            environment.expand_counter+=1
            expanded.append([stepx, stepy])
            if stepx - 1 >= 0:  # left
                if self.Step[stepy][stepx - 1] != 0:
                    hva = abs(checkEX - (stepx - 1)) + abs(checkEY - stepy)
                    if [stepx - 1, stepy] not in CheckDup:
                        CheckDup.append([stepx - 1, stepy])
                        gva = dictionary.get((stepx,stepy)) + 1  #gva = findMinG(dictionary, stepx-1, stepy)+1
                        dictionary[stepx-1, stepy]= gva
                        List.append([gva+hva, gva, hva, stepx - 1, stepy])
                    else:  # in closed list or open list, may need to update f
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx -1, stepy) + 1
                        List, dictionary = replaceL(List, stepx-1, stepy,gva,dictionary)
            if stepx + 1 < environment.w:  # right
                if self.Step[stepy][stepx + 1] != 0:
                    hva = abs(checkEX - (stepx + 1)) + abs(checkEY - stepy)
                    if [stepx + 1, stepy] not in CheckDup:
                        CheckDup.append([stepx + 1, stepy])
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx+1, stepy)+1
                        dictionary[stepx + 1, stepy] = gva
                        List.append([gva+hva, gva, hva, stepx + 1, stepy])
                    else:  # in closed list or open list, may need to update f
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx +1, stepy) + 1
                        List, dictionary = replaceL(List, stepx+1, stepy,gva,dictionary)
            if stepy - 1 >= 0:  # up
                if self.Step[stepy - 1][stepx] != 0:
                    hva = abs(checkEX - stepx) + abs(checkEY - (stepy - 1))
                    if [stepx, stepy - 1] not in CheckDup:
                        CheckDup.append([stepx, stepy - 1])
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx, stepy-1)+1
                        dictionary[stepx, stepy-1] = gva
                        List.append([gva + hva, gva, hva, stepx, stepy - 1])
                    else:  # in closed list or open list, may need to update f
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx, stepy - 1) + 1
                        List, dictionary = replaceL(List, stepx, stepy - 1,gva,dictionary)
            if stepy + 1 < environment.l:  # down
                if self.Step[stepy + 1][stepx] != 0:
                    hva = abs(checkEX - stepx) + abs(checkEY - (stepy + 1))
                    if [stepx, stepy + 1] not in CheckDup:
                        CheckDup.append([stepx, stepy + 1])
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx, stepy+1)+1
                        dictionary[stepx, stepy+1] = gva
                        List.append([gva + hva, gva, hva, stepx, stepy + 1])
                    else:  # in closed list or open list, may need to update f
                        gva = dictionary.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx, stepy + 1) + 1
                        List, dictionary = replaceL(List, stepx, stepy + 1, gva, dictionary)
            if len(List) == 0:
                MOVE=[]
                return list(reversed(MOVE)), self.Step, False
            """it will pick min g around it, and that may cause a problem, if it has the g val but I never really
             expend g val, think about if this will happen into forward""" #not sure why you need findMinG
            List = sorted(sorted(List, key=lambda listo: listo[1],reverse=True), key=lambda listo: listo[0])  # sort by f value
            locat = List.pop(0)
            stepx, stepy = locat[3], locat[4]
            MOVE.append([locat[3], locat[4]])
        # print "start (envir goal) is"
        # print [environment.gx,environment.gy]
        # print "goal (curr) is"
        # print [self.startx,self.starty]
        # print "entire plan is"
        # print expanded
        MOVE=getPath(MOVE, environment.gx, environment.gy) # backtrace to get final planned route
        plan=list(reversed(MOVE))
        # print "plan is"
        # print plan
        return plan, self.Step, True

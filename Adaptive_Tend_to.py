import environment

def findMinG(dic,x,y):
    a,b,c,d=float('inf'),float('inf'),float('inf'),float('inf')
    if dic.has_key((x-1,y)):
        a = dic.get((x-1,y))
    if dic.has_key((x + 1, y)):
        b=dic.get((x + 1, y))
    if dic.has_key((x, y - 1)):
        c=dic.get((x , y - 1))
    if dic.has_key((x, y + 1)):
        d=dic.get((x, y + 1))
    gv = min(a,b,c,d)
    return gv

def getPath(moves, x, y): # return { [gx,gy]...[sx,sy]}
    indexl = len(moves) - 1  # index of last move
    MOVE = []
    for i in range(len(moves)):  # no need to reverse since i is not used in the body
        MOVE.append(moves[indexl])  # append last move lm, which initially is gx gy
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
            break
        indexl = min(indexa, indexb, indexc, indexd)
        if indexl == float('inf'):
            break
    MOVE = list(reversed(MOVE))  # should do this
    return MOVE

class TendTo:
    def __init__(self,startx,starty,Step):
        self.startx = startx ##so seems that this is currx and curry
        self.starty = starty
        self.Step=Step


    def imaginemove(self): #put in open list and close list, close list memerize parent
        List=[]
        CheckDup=[]
        stepx = self.startx
        stepy = self.starty
        CheckDup.append([stepx,stepy])
        environment.ada_g[stepx,stepy]=0
        expanded_cell_array = []
        expanded_cell_array.append([self.startx, self.starty])
        gva = 1
        MOVE = []
        environment.expand_counter+=1
        if stepx == environment.gx and stepy == environment.gy: ## if == environment.sy sx
            return MOVE, self.Step, True

        if stepx - 1 >= 0:                                                                                                   #left
            if environment.Matrix[stepy][stepx - 1] == 0:
                self.Step[stepy][stepx - 1] = 0
            else:
                if environment.h_new.has_key((stepx-1, stepy)):
                    hva = environment.h_new.get((stepx-1, stepy))
                else:
                    hva = abs(environment.gx - (stepx - 1)) + abs(environment.gy - stepy) ### check h_new_array in runnable first to see if this cells has a h_new from last time, if so use h_new;
                if [stepx - 1, stepy] not in CheckDup:                                ### otherwise use manhattan distance; do this for all left, right, up, down
                    CheckDup.append([stepx - 1, stepy])
                    environment.ada_g[stepx - 1, stepy] = 1
                    List.append([gva+hva, gva, hva, stepx - 1, stepy])
        if stepx + 1 < environment.w:                                                                                       #right
            if environment.Matrix[stepy][stepx + 1] == 0:
                self.Step[stepy][stepx + 1] = 0
            else:
                if environment.h_new.has_key((stepx+1,stepy)):
                    hva=environment.h_new.get((stepx+1,stepy))
                else:
                    hva = abs(environment.gx - (stepx + 1)) + abs(environment.gy - stepy)
                if [stepx + 1, stepy] not in CheckDup:
                    CheckDup.append([stepx + 1, stepy])
                    environment.ada_g[stepx + 1, stepy] = 1
                    List.append([gva+hva, gva, hva, stepx + 1, stepy])

        if stepy - 1 >= 0:                                                                                                  #up
            if environment.Matrix[stepy-1][stepx] == 0:
                self.Step[stepy-1][stepx] = 0
            else:
                if environment.h_new.has_key((stepx,stepy-1)):
                    hva = environment.h_new.get((stepx,stepy-1))
                else:
                    hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy - 1))
                if [stepx, stepy - 1] not in CheckDup:
                    CheckDup.append([stepx, stepy - 1])
                    environment.ada_g[stepx, stepy -1] = 1
                    List.append([gva+hva, gva, hva, stepx, stepy - 1])
        if stepy + 1 < environment.l:                                                                                       #down
            if environment.Matrix[stepy+1][stepx] == 0:
                self.Step[stepy + 1][stepx] = 0
            else:
                if environment.h_new.has_key((stepx,stepy+1)):
                    hva=environment.h_new.get((stepx,stepy+1))
                else:
                    hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy + 1))
                if [stepx, stepy + 1] not in CheckDup:
                    CheckDup.append([stepx, stepy + 1])
                    environment.ada_g[stepx, stepy + 1] = 1
                    List.append([gva+hva, gva, hva, stepx, stepy + 1])
        if len(List) == 0:
            return MOVE, self.Step, False
        List = sorted(sorted(List, key=lambda listo: listo[1],reverse=True), key=lambda listo: listo[0])  # sort by age

        locat = List.pop(0)
        stepx, stepy = locat[3], locat[4]
        MOVE.append([locat[3], locat[4]]) # first move

        while stepx != environment.gx or stepy != environment.gy: ## != environment.sx sy
            expanded_cell_array.append([stepx, stepy])
            environment.expand_counter += 1
            if stepx - 1 >= 0:  # left
                if self.Step[stepy][stepx - 1] != 0:
                    if environment.h_new.has_key((stepx - 1,stepy)):
                        hva = environment.h_new.get((stepx - 1,stepy))
                    else:
                        hva = abs(environment.gx - (stepx - 1)) + abs(environment.gy - stepy)
                    if [stepx - 1, stepy] not in CheckDup:
                        CheckDup.append([stepx - 1, stepy])
                        gva = environment.ada_g.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx-1, stepy)+1
                        environment.ada_g[stepx-1, stepy] = gva
                        List.append([gva+hva, gva, hva, stepx - 1, stepy])
                    else: # may need to update f
                        for i in range(len(List)):
                            if List[i][3] == stepx - 1 and List[i][4] == stepy and List[i][0] > gva + hva:
                                List[i] = [gva + hva, gva, hva, stepx - 1, stepy]
                                break
            if stepx + 1 < environment.w:  # right
                if self.Step[stepy][stepx + 1] != 0:
                    if environment.h_new.has_key((stepx + 1,stepy)):
                        hva = environment.h_new.get((stepx + 1,stepy))
                    else:
                        hva = abs(environment.gx - (stepx + 1)) + abs(environment.gy - stepy)
                    if [stepx + 1, stepy] not in CheckDup:
                        CheckDup.append([stepx + 1, stepy])
                        gva = environment.ada_g.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx+1, stepy)+1
                        environment.ada_g[stepx + 1, stepy] = gva
                        List.append([gva+hva, gva, hva, stepx + 1, stepy])
                    else:# may need to update f
                        for i in range(len(List)):
                            if List[i][3] == stepx - 1 and List[i][4] == stepy and List[i][0] > gva + hva:
                                List[i] = [gva + hva, gva, hva, stepx - 1, stepy]
                                break
            if stepy - 1 >= 0:  # up
                if self.Step[stepy - 1][stepx] != 0:
                    if environment.h_new.has_key((stepx,stepy - 1)):
                        hva = environment.h_new.get((stepx,stepy - 1))
                    else:
                        hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy - 1))
                    if [stepx, stepy - 1] not in CheckDup:
                        CheckDup.append([stepx, stepy - 1])
                        gva = environment.ada_g.get((stepx, stepy)) + 1  #gva = findMinG(dictionary, stepx, stepy-1)+1
                        environment.ada_g[stepx, stepy -1] = gva
                        List.append([gva + hva, gva, hva, stepx, stepy - 1])
                    else:# may need to update f
                        for i in range(len(List)):
                            if List[i][3] == stepx - 1 and List[i][4] == stepy and List[i][0] > gva + hva:
                                List[i] = [gva + hva, gva, hva, stepx - 1, stepy]
                                break
            if stepy + 1 < environment.l:  # down
                if self.Step[stepy + 1][stepx] != 0:
                    if environment.h_new.has_key((stepx, stepy + 1)):
                        hva = environment.h_new.get((stepx, stepy + 1))
                    else:
                        hva = abs(environment.gx - stepx) + abs(environment.gy - (stepy + 1))
                    if [stepx, stepy + 1] not in CheckDup:
                        CheckDup.append([stepx, stepy + 1])
                        gva = environment.ada_g.get((stepx,stepy))+1 # gva = findMinG(dictionary, stepx, stepy+1)+1
                        environment.ada_g[stepx, stepy+1] = gva
                        List.append([gva + hva, gva, hva, stepx, stepy + 1])
                    else:# may need to update f
                        for i in range(len(List)):
                            if List[i][3] == stepx - 1 and List[i][4] == stepy and List[i][0] > gva + hva:
                                List[i] = [gva + hva, gva, hva, stepx - 1, stepy]
                                break
            if len(List) == 0:
                MOVE=[]
                return MOVE, self.Step, False
            List = sorted(sorted(List, key=lambda listo: listo[1],reverse=True), key=lambda listo: listo[0])  # sort by f value
            locat = List.pop(0)
            stepx, stepy = locat[3], locat[4]
            MOVE.append([locat[3], locat[4]])
        MOVE=getPath(MOVE,self.startx,self.starty)  # back trace tree pointer
        # print "start is " + str([self.startx, self.starty])
        # print "goal is " + str([environment.gx, environment.gy])
        # print "move is", MOVE
        ggoal = len(MOVE)
        # print "so ggoal is", ggoal
        for j in range(len(expanded_cell_array)):
            cell=expanded_cell_array[j]
            gvalue= environment.ada_g.get((cell[0], cell[1]))
            old_h = environment.h_new.get((cell[0],cell[1]))
            new_h = ggoal - gvalue
            if old_h != new_h:
                # if old_h is not None:
                    # print "Updated h_new", [cell[0], cell[1]], old_h, new_h
                environment.h_new[cell[0], cell[1]] = new_h
        # print "planned move " + str(MOVE)
        # print "g goal " + str(ggoal)
        # print "h new " + str(environment.h_new)
        # print "expanded cell " + str(len(expanded_cell_array))
        return MOVE, self.Step, True
### assign h_new for all expanded cells (cells in the closed list) into h_new_array in runnable
### h_new (s) = MOVE.length - g(s)
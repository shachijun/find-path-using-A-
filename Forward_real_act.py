import environment
class realMove:
    def __init__(self,Imgmove,LIST):

        self.Imgmove=Imgmove
        self.LIST=LIST
    def makemove(self): # execute move and update overall path, report if reached the goal or not and if encounter block, mark down prev pos
        MOVE=[]
        count = 0
        # ParentList = []
        findgoal = False
        for i in range(len(self.Imgmove)): # go thru moves
            if environment.Matrix[self.Imgmove[i][1]][self.Imgmove[i][0]] == 0: # this move is blocked
                count = i # index of blocked move
                break
            if environment.Matrix[self.Imgmove[i][1]][self.Imgmove[i][0]] == 4: # this move is goal
                count = i # index of goal in move
                findgoal= True # found the goal
                break
            MOVE.append(self.Imgmove[i]) # otherwise append move
            if self.Imgmove[i] not in self.LIST: # never visited before
                self.LIST.append(self.Imgmove[i]) # add those moves to overall path taken

        """in the past, these steps seems to be find the most recent move until I reach the wall
        to do this because Im not sure if the last thing in the LIST is the last move, so I did this
        However, in this back track seems not need to because the move might be some where else, 
        not even continue the start point, in this point, I will just make the agent move to the LIST Last
        location"""
        a, b, c, d = float('inf'), float('inf'), float('inf'), float('inf')
        if [self.Imgmove[count][0],self.Imgmove[count][1] - 1] in self.LIST: # up point of move visited
            a = self.LIST.index([self.Imgmove[count][0],self.Imgmove[count][1] - 1]) # get index of up point
        elif [self.Imgmove[count][0],self.Imgmove[count][1] + 1] in self.LIST:
            b = self.LIST.index([self.Imgmove[count][0],self.Imgmove[count][1] + 1])
        elif [self.Imgmove[count][0] - 1,self.Imgmove[count][1]] in self.LIST:
            c = self.LIST.index([self.Imgmove[count][0] - 1,self.Imgmove[count][1]])
        elif [self.Imgmove[count][0] + 1,self.Imgmove[count][1]] in self.LIST:
            d = self.LIST.index([self.Imgmove[count][0] + 1,self.Imgmove[count][1]])

        ParentList = self.LIST[min(a,b,c,d)] # previous step before I step on a block

        return self.LIST, MOVE, ParentList,findgoal


    def makemoveB(self,x,y):
        # print "move to be made"
        # print self.Imgmove
        MOVE=[]
        MOVE.append([x,y])
        findgoal = False

        for i in range(len(self.Imgmove)):
            if environment.Matrix[self.Imgmove[i][1]][self.Imgmove[i][0]] == 0: # this move is blocked
                # print "block is"
                # print [self.Imgmove[i][0],self.Imgmove[i][1]]
                break
            if environment.Matrix[self.Imgmove[i][1]][self.Imgmove[i][0]] == 4: # this move is goal
                findgoal= True
                break
            if [self.Imgmove[i][0], self.Imgmove[i][1] - 1] in MOVE \
                    or [self.Imgmove[i][0], self.Imgmove[i][1] + 1] in MOVE \
                    or [self.Imgmove[i][0] - 1, self.Imgmove[i][1]] in MOVE \
                    or [self.Imgmove[i][0] + 1, self.Imgmove[i][1]] in MOVE:

                MOVE.append(self.Imgmove[i])
                if self.Imgmove[i] not in self.LIST:
                    self.LIST.append(self.Imgmove[i])

        ParentList = MOVE[len(MOVE)-1]
        # print "before pop off"
        # print(MOVE)
        MOVE.pop(0) # pop off start point so blue not cover start
        # print "to act move"
        # print MOVE
        # print "found goal?"
        # print findgoal
        return self.LIST, MOVE, ParentList,findgoal


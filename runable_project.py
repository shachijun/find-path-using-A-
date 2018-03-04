# from graphics import *
import environment
import Forward_real_act
import Forward_Tend_to
import Forward_Tend_to_gs
import Backward_Tend_to
from Tkinter import *
import tkMessageBox
import  Adaptive_Tend_to
import time
from collections import defaultdict


root = Tk()
root.geometry("1200x700")
canvas = Canvas(root, width=620, height=620)
canvas.pack()
imaginedDrawn = 0
start_time = 0
end_time = 0
Imgmove=[]

def origGrap(): #this is create the original graph
    for i in range(environment.w):
        for j in range(environment.l):
            if environment.Matrix[j][i] == 0:
                canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6,fill="black")
            elif environment.Matrix[j][i] == 3:
                canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6, fill="red")
            elif environment.Matrix[j][i] == 4:
                canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6,fill="gold")
            # elif environment.Matrix[j][i] == 1:
            #     canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6,fill="white", outline="white")


origGrap()  # draw environment
currentx = environment.sx
currenty = environment.sy
Step = [[1 for x in range(environment.w)] for y in range(environment.l)] # knowledge about environment
Step[environment.gy][environment.gx] = 4
Step[environment.sy][environment.sx] = 3
List=[] # overall path I executed


def reset(): # used to compare different A*
    environment.ada_g={}
    environment.expand_counter=0
    environment.h_new={}
    global currentx,currenty,Step,List, start_time, end_time, Imgmove
    Imgmove=[]
    currentx = environment.sx
    currenty = environment.sy
    Step = [[1 for x in range(environment.w)] for y in range(environment.l)]  # knowledge about environment
    Step[environment.gy][environment.gx] = 4
    Step[environment.sy][environment.sx] = 3
    List = []  # overall path I executed
    for i in range(environment.w):
        for j in range(environment.l):
            if environment.Matrix[j][i] == 1:
                canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6,fill="white", outline="white")
    origGrap()
    Label_expCount['text'] = "expand: 0"
    Label_time['text'] = "time: 0"
    start_time=0
    end_time=0

def flushThenMove(): # takes too long, need to find ways to remove last search's green and blue line
    global currentx,currenty
    for i in range(environment.w):
        for j in range(environment.l):
            if environment.Matrix[j][i] == 1:
                canvas.create_rectangle((i+1)*6, (j+1)*6, (i+2)*6, (j+2)*6,fill="white", outline="white")
    for i in range(environment.w):
        for j in range(environment.l):
            if environment.Matrix[j][i] == 0:
                canvas.create_rectangle((i + 1) * 6, (j + 1) * 6, (i + 2) * 6, (j + 2) * 6, fill="black")
            elif environment.Matrix[j][i] == 4:
                canvas.create_rectangle((i + 1) * 6, (j + 1) * 6, (i + 2) * 6, (j + 2) * 6, fill="gold")
            elif environment.Matrix[j][i] == 3:
                canvas.create_rectangle((i + 1) * 6, (j + 1) * 6, (i + 2) * 6, (j + 2) * 6, fill="pink")
            if i==currentx and j==currenty:
                canvas.create_rectangle((i + 1) * 6, (j + 1) * 6, (i + 2) * 6, (j + 2) * 6, fill="red")


def findPath(list):
    indexl = len(list)-1
    LIST=[]
    for i in reversed(range(len(list))):
        LIST.append(list[indexl])
        indexa ,indexb ,indexc,indexd = float('inf'), float('inf'), float('inf'),float('inf')
        if [list[indexl][0]-1,list[indexl][1]] in list:
            indexa = list.index([list[indexl][0]-1,list[indexl][1]])
        if [list[indexl][0],list[indexl][1]-1] in list:
            indexb = list.index([list[indexl][0],list[indexl][1]-1])
        if [list[indexl][0]+1,list[indexl][1]] in list:
            indexc = list.index([list[indexl][0]+1,list[indexl][1]])
        if [list[indexl][0],list[indexl][1]+1] in list:
            indexd = list.index([list[indexl][0],list[indexl][1]+1])

        if [list[indexl][0] - 1, list[indexl][1]] ==[environment.sx,environment.sy]\
                or [list[indexl][0], list[indexl][1] - 1]==[environment.sx,environment.sy]\
                or [list[indexl][0] + 1, list[indexl][1]]==[environment.sx,environment.sy]\
                or [list[indexl][0], list[indexl][1] + 1] ==[environment.sx,environment.sy]:
            break
        indexl = min(indexa, indexb, indexc, indexd)
        if indexl == float('inf'):
            break
    return LIST


def TendTo(movex,movey,matrix):# this is making the immagine graph
    global Imgmove, Step
    Imgmove, Step, con = Forward_Tend_to.TendTo.imaginemove(Forward_Tend_to.TendTo(movex, movey, matrix))
    if con == False:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
    else:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
    for i in range(len(Imgmove)-1):
        canvas.create_rectangle((Imgmove[i][0]+1) * 6, (Imgmove[i][1]+1) * 6,  (Imgmove[i][0]+2) * 6, (Imgmove[i][1]+2) * 6, fill="green")
# movex movey are current location of agent; matrix is Step, li is List


def ActMove(movex,movey,matrix,li, whole): #return current locate, probabily not need to
    # print environment.expand_counter
    global start_time, end_time, Imgmove, Step
    if whole: # running whole process, need to do planning
        Imgmove, Step, findGoal = Forward_Tend_to.TendTo.imaginemove(Forward_Tend_to.TendTo(movex, movey, matrix)) # compute path
        for i in range(len(Imgmove) - 1): # show computed path
            canvas.create_rectangle((Imgmove[i][0] + 1) * 6, (Imgmove[i][1] + 1) * 6, (Imgmove[i][0] + 2) * 6, (Imgmove[i][1] + 2) * 6, fill="green")
        origGrap()  # draw original environment
        if not findGoal: # goal is unreachable according to our planning; false for
            end_time = time.time()
            Label_expCount['text'] = "expand: " + str(environment.expand_counter)
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
            tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
            return False, True
    if not whole:
        origGrap()
    # lo is List with added moves, ParentList is previous pos before step onto block
    lo, MOVE, ParentList,findg = Forward_real_act.realMove.makemove(Forward_real_act.realMove(Imgmove,li))
    global currentx, currenty, List
    if not findg: # blocked
        Step[ParentList[1]][ParentList[0]] = 3 # set previous pos before block as new start
        currentx, currenty = ParentList[0],ParentList[1] # set current position as new start
        List = lo # set knowledge map and overall path to updated version
    arlen = len(MOVE) # number of moves
    for i in range(arlen):
        canvas.create_rectangle((MOVE[i][0]+1) * 6, (MOVE[i][1]+1) * 6,  (MOVE[i][0]+2) * 6, (MOVE[i][1]+2) * 6, fill="blue")
    if findg:  # found the goal
        if whole:
            end_time = time.time()
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished","We find the GOAL!")
        Lis = findPath(List)
        for i in reversed(range(len(Lis))):
            canvas.create_rectangle((Lis[i][0] + 1) * 6, (Lis[i][1] + 1) * 6, (Lis[i][0] + 2) * 6,(Lis[i][1] + 2) * 6, fill="brown")
        return True, True
    return False, False


def Fall():
    # print environment.expand_counter
    global start_time
    start_time=time.time()
    fina=False
    global currentx, currenty, Step,List
    """if cannot find the goal the just break"""
    while not fina:
        fina, nevergoal = ActMove(currentx, currenty, Step,List, True)
        if nevergoal:
            break


def TendToB(movex,movey,matrix):# this is making the immagine graph
    global Imgmove, Step
    Imgmove, Step, con = Backward_Tend_to.TendTo.imaginemove(Backward_Tend_to.TendTo(movex, movey, matrix))
    if con == False:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
    else:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
    Imgmove.pop(0) # pop off start point
    for i in range(len(Imgmove)-1): # -1 so green not cover goal
        canvas.create_rectangle((Imgmove[i][0]+1) * 6, (Imgmove[i][1]+1) * 6,  (Imgmove[i][0]+2) * 6, (Imgmove[i][1]+2) * 6, fill="green")

def ActMoveB(movex,movey,matrix,li, whole): #return current locate, probabily not need to
    # print environment.expand_counter
    global start_time, end_time, Imgmove, Step, currentx, currenty, List
    origGrap()
    if whole:
        Imgmove, Step, findGoal = Backward_Tend_to.TendTo.imaginemove(Backward_Tend_to.TendTo(movex, movey, matrix))
        for i in range(len(Imgmove) - 1): # show computed path
            canvas.create_rectangle((Imgmove[i][0] + 1) * 6, (Imgmove[i][1] + 1) * 6, (Imgmove[i][0] + 2) * 6,(Imgmove[i][1] + 2) * 6, fill="green")
        if not findGoal:
            end_time=time.time()
            Label_expCount['text'] = "expand: " + str(environment.expand_counter)
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
            tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
            return False,True
        Imgmove.pop(0) # pop off start point
    lo, MOVE, ParentList,findg = Forward_real_act.realMove.makemoveB(Forward_real_act.realMove(Imgmove,li),movex, movey)
    if not findg: # blocked
        Step[ParentList[1]][ParentList[0]] = 3
        currentx, currenty = ParentList[0], ParentList[1]
        List = lo
    arlen = len(MOVE)
    for i in range(arlen):
        canvas.create_rectangle((MOVE[i][0]+1) * 6, (MOVE[i][1]+1) * 6,  (MOVE[i][0]+2) * 6, (MOVE[i][1]+2) * 6, fill="blue")
    if findg:
        if whole:
            end_time=time.time()
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished","We find the GOAL!")
        Lis = findPath(List)
        for i in reversed(range(len(Lis))):
            canvas.create_rectangle((Lis[i][0] + 1) * 6, (Lis[i][1] + 1) * 6, (Lis[i][0] + 2) * 6,(Lis[i][1] + 2) * 6, fill="brown")
        return True, True
    return False, False


def Ball():
    global start_time
    start_time=time.time()
    fina=False
    global currentx, currenty, Step,List
    while not fina :
        fina,nevergoal = ActMoveB(currentx, currenty, Step,List,True)
        if nevergoal:
            break


def AdaTendTo(movex,movey,matrix):# this is making the immagine graph
    global Imgmove, Step
    Imgmove, Step, con = Adaptive_Tend_to.TendTo.imaginemove(Adaptive_Tend_to.TendTo(movex, movey, matrix))
    if con == False:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
    else:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
    for i in range(len(Imgmove)-1):
        canvas.create_rectangle((Imgmove[i][0]+1) * 6, (Imgmove[i][1]+1) * 6,  (Imgmove[i][0]+2) * 6, (Imgmove[i][1]+2) * 6, fill="green")
# movex movey are current location of agent; matrix is Step, li is List


def AdaActMove(movex,movey,matrix,li, whole): # return current locate, probabily not need to
    global start_time, end_time, Imgmove, Step, currentx, currenty, List
    origGrap() # draw original environment
    if whole:
        Imgmove, Step, findGoal = Adaptive_Tend_to.TendTo.imaginemove(Adaptive_Tend_to.TendTo(movex, movey, matrix)) # compute path
        for i in range(len(Imgmove) - 1): # show computed path
            canvas.create_rectangle((Imgmove[i][0] + 1) * 6, (Imgmove[i][1] + 1) * 6, (Imgmove[i][0] + 2) * 6, (Imgmove[i][1] + 2) * 6, fill="green")
        if not findGoal: # goal is unreachable according to our planning; false for
            end_time=time.time()
            Label_expCount['text'] = "expand: " + str(environment.expand_counter)
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
            tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
            return False, True
    # lo is List with added moves, ParentList is previous pos before step onto block
    lo, MOVE, ParentList,findg = Forward_real_act.realMove.makemove(Forward_real_act.realMove(Imgmove,li))
    if not findg: # blocked
        Step[ParentList[1]][ParentList[0]] = 3 # set previous pos before block as new start
        currentx, currenty = ParentList[0],ParentList[1] # set current position as new start
        List = lo # set knowledge map and overall path to updated version
    arlen = len(MOVE) # number of moves
    for i in range(arlen):
        canvas.create_rectangle((MOVE[i][0]+1) * 6, (MOVE[i][1]+1) * 6,  (MOVE[i][0]+2) * 6, (MOVE[i][1]+2) * 6, fill="blue")
    if findg: # found the goal
        if whole:
            end_time=time.time()
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished","We find the GOAL!")
        Lis = findPath(List)
        for i in reversed(range(len(Lis))):
            canvas.create_rectangle((Lis[i][0] + 1) * 6, (Lis[i][1] + 1) * 6, (Lis[i][0] + 2) * 6,(Lis[i][1] + 2) * 6, fill="brown")
        return True, True
    return False, False


def Adall():
    global start_time
    start_time=time.time()
    fina=False
    global currentx, currenty, Step,List
    """if cannot find the goal the just break"""
    while not fina:
        fina, nevergoal = AdaActMove(currentx, currenty, Step, List, True)
        if nevergoal:
            break

def TendToGS(movex,movey,matrix):# this is making the immagine graph
    global Imgmove, Step
    Imgmove, Step, con = Forward_Tend_to_gs.TendTo.imaginemove(Forward_Tend_to_gs.TendTo(movex, movey, matrix))
    if con == False:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
    else:
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
    for i in range(len(Imgmove)-1):
        canvas.create_rectangle((Imgmove[i][0]+1) * 6, (Imgmove[i][1]+1) * 6,  (Imgmove[i][0]+2) * 6, (Imgmove[i][1]+2) * 6, fill="green")
    Label_expCount['text'] = "expand: " + str(environment.expand_counter)

# movex movey are current location of agent; matrix is Step, li is List


def ActMoveGS(movex,movey,matrix,li, whole): #return current locate, probabily not need to
    global start_time, end_time, Step, Imgmove, currentx, currenty, List
    if whole:
        Imgmove, Step, findGoal = Forward_Tend_to_gs.TendTo.imaginemove(Forward_Tend_to_gs.TendTo(movex, movey, matrix)) # compute path
        for i in range(len(Imgmove) - 1): # show computed path
            canvas.create_rectangle((Imgmove[i][0] + 1) * 6, (Imgmove[i][1] + 1) * 6, (Imgmove[i][0] + 2) * 6, (Imgmove[i][1] + 2) * 6, fill="green")
        origGrap()  # draw original environment
        if not findGoal: # goal is unreachable according to our planning; false for
            end_time=time.time()
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
            Label_expCount['text'] = "expand: " + str(environment.expand_counter)
            tkMessageBox.showinfo("Finished", "We cannot find the Goal!")
            return False, True
    if not whole:
        origGrap()
    # lo is List with added moves, ParentList is previous pos before step onto block
    lo, MOVE, ParentList,findg = Forward_real_act.realMove.makemove(Forward_real_act.realMove(Imgmove,li))
    if not findg: # blocked
        Step[ParentList[1]][ParentList[0]] = 3 # set previous pos before block as new start
        currentx, currenty = ParentList[0],ParentList[1] # set current position as new start
        Step, List = Step, lo # set knowledge map and overall path to updated version
    arlen = len(MOVE) # number of moves
    for i in range(arlen):
        canvas.create_rectangle((MOVE[i][0]+1) * 6, (MOVE[i][1]+1) * 6,  (MOVE[i][0]+2) * 6, (MOVE[i][1]+2) * 6, fill="blue")
    if findg: # found the goal
        if whole:
            end_time=time.time()
            Label_time['text'] = "time: " + "{0:.3f}".format(round(end_time - start_time, 3))
        Label_expCount['text'] = "expand: " + str(environment.expand_counter)
        tkMessageBox.showinfo("Finished","We find the GOAL!")
        Lis = findPath(List)
        for i in reversed(range(len(Lis))):
            canvas.create_rectangle((Lis[i][0] + 1) * 6, (Lis[i][1] + 1) * 6, (Lis[i][0] + 2) * 6,(Lis[i][1] + 2) * 6, fill="brown")
        return True, True
    return False, False


def FallGS():
    # print environment.expand_counter
    global start_time
    start_time=time.time()
    fina=False
    global currentx, currenty, Step,List
    """if cannot find the goal the just break"""
    while not fina:
        fina, nevergoal = ActMoveGS(currentx, currenty, Step,List, True)
        if nevergoal:
            break


# button with commands
Button_fimg = Button(root,text="Fim", command=lambda: TendTo(currentx, currenty, Step))
Button_fimg.pack(side=LEFT)
Button_freal = Button(root,text="Fre", command=lambda: ActMove(currentx, currenty, Step, List, False))
Button_freal.pack(side=LEFT)
Button_ffinal = Button(root,text="Ffin", command=Fall)
Button_ffinal.pack(side=LEFT)

Button_fimggs = Button(root,text="FimGS", command=lambda: TendToGS(currentx, currenty, Step))
Button_fimggs.pack(side=LEFT)
Button_frealgs = Button(root,text="FreGS", command=lambda: ActMoveGS(currentx, currenty, Step, List, False))
Button_frealgs.pack(side=LEFT)
Button_ffinalgs = Button(root,text="FfinGS", command=FallGS)
Button_ffinalgs.pack(side=LEFT)

Button_bimg = Button(root,text="Bim", command=lambda: TendToB(currentx, currenty, Step))
Button_bimg.pack(side=LEFT)
Button_breal = Button(root,text="Bre", command=lambda: ActMoveB(currentx, currenty, Step,List,False))
Button_breal.pack(side=LEFT)
Button_bfinal = Button(root,text="Bfin", command=Ball)
Button_bfinal.pack(side=LEFT)


Button_bimg = Button(root,text="ADim", command=lambda: AdaTendTo(currentx, currenty, Step))
Button_bimg.pack(side=LEFT)
Button_breal = Button(root,text="ADre", command=lambda: AdaActMove(currentx, currenty, Step, List, False))
Button_breal.pack(side=LEFT)
Button_bfinal = Button(root,text="ADfin", command=Adall)
Button_bfinal.pack(side=LEFT)

Button_exit = Button(root,text="exit", command=root.destroy)
Button_exit.pack(side=RIGHT)

Button_exit = Button(root,text="Original", command=origGrap)
Button_exit.pack(side=RIGHT)

Button_fimg = Button(root,text="Flush&Move", command=flushThenMove)
Button_fimg.pack(side=RIGHT)

Button_fimg = Button(root,text="Reset", command=reset)
Button_fimg.pack(side=RIGHT)

Label_time = Label(root, text="time: 0")
Label_time.pack(side=LEFT)

Label_expCount = Label(root, text="expand: 0")
Label_expCount.pack(side=LEFT)

root.mainloop()

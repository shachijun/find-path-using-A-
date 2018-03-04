import random
expand_counter = 0
h_new={}  # [(x,y), h_new]
ada_g={}
w = 101  # input("Please input matrix width ")
l = 101  # input("Please input matrix length ")
Matrix = [[0 for x in range(w)] for y in range(l)]
# print Matrix[9][0] w=1 l=10
for i in range(l):
    for a in range(w):
        if random.randint(0,10) <= 7:
            Matrix[i][a] = 1
        else:
            Matrix[i][a] = 0
gx=random.randint(0,w-1)
gy=random.randint(0,l-1)
sx=random.randint(0,w-1)
sy=random.randint(0,l-1)
while gx == sx and gy == sy:
    gx = random.randint(0, w-1)
    gy = random.randint(0, l-1)
# sy=0
# sx=0
# gy=100
# gx=100
Matrix[gy][gx] = 4
Matrix[sy][sx] = 3



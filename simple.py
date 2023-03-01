import pandas as pd

board = [[0, 0, 0], [0, 0, -1], [-1, 0, 1]]

player = (0, 0)

# def probability(pos, dir):
#     x, y = pos

#     if dir == "up" and x == 0:
#         return 0
#     elif dir == "down" and x == 2:
#         return 0
#     elif dir == "left" and y == 0:
#         return 0
#     elif dir == "right" and y == 2:
#         return 0
#     else:
#         return 1
        # if dir == "up":
        #     x -= 1
        # elif dir == "down":
        #     x += 1
        # if dir == "left":
        #     y -= 1
        # elif dir == "right":
        #     y += 1


def reward(pos, dir):
    x, y = pos

    if dir == "up":
        x -= 1
    elif dir == "down":
        x += 1
    if dir == "left":
        y -= 1
    elif dir == "right":
        y += 1

    return board[x][y]


def make_move(pos,r_move):
    x,y=pos
    if r_move=="left":
        y-=1
        return (x,y),r_move
    elif r_move=="right":
        y+=1
        return (x,y),r_move
    elif r_move=="up":
        x-=1
        return (x,y),r_move
    elif r_move=="down":
        x+=1
        return (x,y),r_move

def possi_moves(pos):
    x,y=pos
    mv=["up","down","right","left"]
    if y==0:
        mv.remove("left")
    elif y==2:
        mv.remove("right")
    if x==0:
        mv.remove("up")
    elif x==2:
        mv.remove("down")
    return mv
    # return list(q_table["dir"][(q_table["x"] == x) & (q_table["y"] == y)])

def step(pos, action):
    new_pos,_ = make_move(pos, action)
    rew = reward(pos, action)
    return new_pos, rew

q_table = pd.DataFrame()
for i in range(3):
    for j in range(3):
        for dir in ["up", "down", "left", "right"]:
            if dir == "up" and i == 0:
                continue
            elif dir == "down" and i == 2:
                continue
            elif dir == "left" and j == 0:
                continue
            elif dir == "right" and j == 2:
                continue
            else:
                row = pd.DataFrame({"x": i, "y": j, "dir": dir,
                                    "Q": 0, "reward": reward((i,j), dir), "V": 0}, index=[0])
                q_table = pd.concat([q_table, row])
    q_table.reset_index(drop=True, inplace=True)

print(q_table)

# def main():
#   pos=(1,2)
#   A=[]
#   B=[]
#   l=possi_moves(pos)
#   for i in l:
#     r=reward(pos,i)
#     A.append(r)
#     B.append(make_move(pos,i))

#   c=list(zip(A,B))
#   print(c)

# main()

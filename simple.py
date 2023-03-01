import pandas as pd

board = [[0, 0, 0], [0, 0, -1], [-1, 0, 1]]

player = (0, 0)

def reward(pos):
    x, y = pos
    return board[x][y]

def make_move(pos, action):
    x,y=pos
    if action=="left":
        y-=1
        return (x,y)
    elif action=="right":
        y+=1
        return (x,y)
    elif action=="up":
        x-=1
        return (x,y)
    elif action=="down":
        x+=1
        return (x,y)

def step(state, action):
    new_state,_ = make_move(state, action)

    return new_state, reward(new_state)

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
                                    "Q": 0, "reward": reward((i,j)), "V": 0}, index=[0])
                q_table = pd.concat([q_table, row])
    q_table.reset_index(drop=True, inplace=True)


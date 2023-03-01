import pandas as pd

board = [[0.1, 0.1, 0.1], [0.1, 0.1, -1], [-1, 0.1, 1]]

def reward(state):
    x, y = state
    return board[x][y]

def make_move(state, action):
    x, y = state
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
    else:
        print(action)
        return action, None

def make_step(state, action):
    new_state = make_move(state, action)
    rew = reward(new_state)
    done = True if rew in [1, -1] else False

    return new_state, rew, done

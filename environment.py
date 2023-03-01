board = [[1, 1, 1], [1, 1, -10], [-10, 1, 10]]

def distance(state, target=(2, 2)):
    x1, y1 = state
    x2, y2 = target

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

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

def make_step(state, action):
    new_state = make_move(state, action)
    new_reward = reward(new_state)
    done = True if new_reward in [10, -10] else False
    if not done:
        # try to give reward based on how close we are to the target
        old_distance = distance(state)
        new_distance = distance(new_state)
        diff = new_distance - old_distance
        new_reward = -diff

    return new_state, new_reward, done

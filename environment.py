NUM_ROWS = 10
NUM_COLUMNS = 10
board = [[0 for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

start_states = list()
for x in range(NUM_ROWS):
    for y in range(NUM_COLUMNS):
        start_states.append((x, y))
target = (NUM_ROWS//2, NUM_COLUMNS//2)
start_states.remove(target)
target_x, target_y = target
TARGET_REWARD = 10
board[target_x][target_y] = TARGET_REWARD

def distance(state, target):
    x1, y1 = state
    x2, y2 = target

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def reward(state, action):
    new_state = make_move(state, action)
    x, y = new_state
    new_reward = board[x][y]
    if new_reward != TARGET_REWARD:
        # try to give reward based on how close we are to the target
        old_distance = distance(state, target)
        new_distance = distance(new_state, target)
        diff = new_distance - old_distance
        new_reward = -diff

    return new_state, new_reward

def valid_move(state, action):
    x, y = state
    if "upper" in action and x == 0:
        return False
    elif "lower" in action and x == NUM_ROWS - 1:
        return False

    if "left" in action and y == 0:
        return False
    if "right" in action and y == NUM_COLUMNS - 1:
        return False
    elif action == "up" and x == 0:
        return False
    elif action == "down" and x == NUM_ROWS - 1:
        return False

    return True

def make_move(state, action):
    x, y = state
    if "upper" in action:
        x-=1
    elif "lower" in action:
        x+=1

    if "left" in action:
        y-=1
    elif "right" in action:
        y+=1
    elif action == "up":
        x-=1
    elif action == "down":
        x+=1

    return (x,y)

def make_step(state, action):
    new_state, new_reward = reward(state, action)
    game_over = True if new_reward == TARGET_REWARD else False

    return new_state, new_reward, game_over

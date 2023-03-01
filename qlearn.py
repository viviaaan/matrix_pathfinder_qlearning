from environment import *
import random
import numpy as np
import pandas as pd

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
                                    "Q": 0, "reward": reward(make_move((i,j), dir)), "value": 0}, index=[0])
                q_table = pd.concat([q_table, row])
    q_table.reset_index(drop=True, inplace=True)

print(q_table)

num_episodes = 1000
# max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01

exploration_decay_rate = 0.01 #if we decrease it, will learn slower

rewards_all_episodes = []

# Q-Learning algorithm
for episode in range(num_episodes):
    print("Episode:", episode)
    state = (0, 0)

    done = False
    rewards_current_episode = 0

    # for step in range(max_steps_per_episode):
    while True:
        # print("Step", step, "of", "episode", episode)
        q_table_for_state = q_table[(q_table["x"] == state[0]) & (q_table["y"] == state[1])]

        # Exploration -exploitation trade-off
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            # action = np.argmax(q_table[state,:])
            action = q_table_for_state["dir"][(q_table_for_state["value"]).idxmax()]
        else:
            action = np.random.choice(q_table_for_state["dir"])

        new_state, reward, done = make_step(state, action)

        # Update Q-table for Q(s,a)
        # q_table[state, action] = (1 - learning_rate) * q_table[state, action] + \
            # learning_rate * (reward + discount_rate * np.max(q_table[new_state,:]))


        q_table.loc[(q_table["x"] == state[0]) & (q_table["y"] == state[1]) & (q_table["dir"] == action), "value"] = (1 - learning_rate) * q_table_for_state[q_table_for_state["dir"] == action]["value"] + \
            learning_rate * (reward + discount_rate * np.max(q_table_for_state["value"]))

        state = new_state
        rewards_current_episode += reward

        if done:
            break

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)

# Calculate and print the average reward per 100 episodes
rewards_per_hundred_episodes = np.split(np.array(rewards_all_episodes), num_episodes // 100)
count = 100
print("********** Average  reward per hundred episodes **********\n")

for r in rewards_per_hundred_episodes:
    print(count, ": ", sum(r)/100)
    count += 100

# Print updated Q-table
print("\n\n********** Q-table **********\n")
print(q_table)

# print((q_table[(q_table["x"] == 0) & (q_table["y"] == 2)]["value"]).idxmax())
# print(q_table[(q_table["x"] == 0) & (q_table["y"] == 2)]["dir"][np.argmax(q_table[(q_table["x"] == 0) & (q_table["y"] == 2)]["value"])])

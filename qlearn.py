from environment import *
import random
import numpy as np
import pandas as pd

q_table = pd.DataFrame()
for i in range(3):
    for j in range(3):
        for action in ["up", "down", "left", "right"]:
            if action == "up" and i == 0:
                continue
            elif action == "down" and i == 2:
                continue
            elif action == "left" and j == 0:
                continue
            elif action == "right" and j == 2:
                continue
            else:
                row = pd.DataFrame({"state": [(i, j)],"action": action, "reward": reward((i, j), action)[1], "value": 0}, index=[0])
                q_table = pd.concat([q_table, row])
q_table.reset_index(drop=True, inplace=True)

num_episodes = 1000

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01

exploration_decay_rate = 0.01 # if we decrease it, will learn slower

rewards_all_episodes = []

# Q-Learning algorithm
for episode in range(num_episodes):
    print("Episode:", episode)
    state = (0, 0) # starting state

    done = False
    rewards_current_episode = 0

    while not done: # while game is not over
        q_table_for_current_state = q_table[q_table["state"] == state]

        # choose whether to exploit or explore based on exploration_rate
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            action = q_table_for_current_state["action"][(q_table_for_current_state["value"]).idxmax()]
        else:
            action = np.random.choice(q_table_for_current_state["action"])

        new_state, reward, done = make_step(state, action)

        # Update Q-table for Q(s,a)
        q_table.loc[(q_table["state"] == state) & (q_table["action"] == action), "value"] = \
            (1 - learning_rate) * q_table_for_current_state[q_table_for_current_state["action"] == action]["value"] + \
            learning_rate * (reward + discount_rate * np.max(q_table_for_current_state["value"]))

        state = new_state
        rewards_current_episode += reward

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)

# Calculate and print the average reward per 100 episodes
rewards_per_hundred_episodes = np.split(np.array(rewards_all_episodes), num_episodes // 100)
count = 100
print("********** Average  reward per hundred episodes **********\n")

for r in rewards_per_hundred_episodes:
    print(count, ":", sum(r)/100)
    count += 100

# Print updated Q-table
print("\n\n********** Q-table **********\n")
print(q_table)

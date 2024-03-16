
import matplotlib.pyplot as plt
import numpy as np

# Define the utility function
def utility(n_going):
    is_crowded = n_going >= threshold_crowded
    if not is_crowded:
        if n_going == 0:
            return 0  # If no one is going, utility is 0
        elif n_going == threshold_crowded:
            return 1
        else:
            return (1 / threshold_crowded) * n_going
    else:
        if n_going == n_agents:
            return -1  # If all agents are going, utility is -1
        else:
            return -((1 / (n_agents - threshold_crowded)) * (n_going - threshold_crowded))

# Define the payoff function
def payoff(n_going, decision):
    if decision == 1:
        return utility(n_going)
    else:
        return -utility(n_going)  # Assuming staying has the opposite utility effect

# Choose strategy function
def choose_strategy(strategy_id):
    strategies = {
        1: strategy_1,
        2: strategy_2,
        3: strategy_3,
        4: strategy_4,
        5: strategy_5,
        6: strategy_6,
    }
    return strategies.get(strategy_id, strategy_1)  # Default to strategy_1 if not found

# Pure Strategies
def strategy_1(X=1, p=0.561):
    if len(history) < X:
        return p
    avg_n_going = np.mean(history[-X:]) if len(history) >= X else 0
    return 0 if avg_n_going > threshold_crowded else 1

def strategy_2(X=1,  p=0.561, factor=0.1):
    if len(history) < X:
        return p
    last_n_going = np.mean(history[-X:]) if len(history) >= X else 0
    difference = last_n_going - threshold_crowded
    adjustment = -difference * (1 / (n_agents - threshold_crowded))  * factor
    new_p = min(1, max(0, p + adjustment))
    return new_p

def strategy_3(X=1,  p=0.561):
    if len(history) < X:
        return p
    last_n_going = np.mean(history[-X:]) if len(history) >= X else 0
    difference = threshold_crowded - last_n_going

    # Ensure that the probability stays within [0, 1]
    probability = max(0, min(1, (difference + threshold_crowded) / (2 * threshold_crowded)))
    return probability

# Trend-Based Strategy
def strategy_4(X=3, p=0.561, threshold=0.1):
    if len(history) < X:
        return p
    recent_trend = np.polyfit(range(X), history[-X:], 1)[0]  # Linear fit to the last X days
    if recent_trend > threshold:  # Bar is becoming more crowded
        return max(0, p - 0.1)
    elif recent_trend < -threshold:  # Bar is becoming less crowded
        return min(1, p + 0.1)
    else:
        return p

# Weighted Average Strategy
def strategy_5(X=5, p=0.561, adjustment_rate=0.05):
    if len(history) < X:
        return p
    weights = np.linspace(1, 0, X)  # Higher weights for more recent days
    weighted_avg = np.average(history[-X:], weights=weights)
    adjustment = adjustment_rate * (threshold_crowded - weighted_avg) / threshold_crowded
    return max(0, min(1, p + adjustment))


# Adaptive Threshold Strategy
def strategy_6(X=5, p=0.561, adapt_rate=0.05, adjustment_rate=0.05):
    if len(history) < X:
        return p
    avg_n_going = np.mean(history[-X:])
    adaptive_threshold = threshold_crowded + adapt_rate * (avg_n_going - threshold_crowded)
    adjustment = adjustment_rate * (adaptive_threshold - avg_n_going) / n_agents
    return max(0, min(1, p + adjustment))



# Simulation parameters
days = 1000  # Number of times the simulation is run for testing
n_agents = 101  # Total number of agents
threshold_crowded = 50  # Threshold for the bar to be considered crowded
n_strats = 6  # Number of strategies


history = []
history_seperated = {i: [] for i in range(1, n_strats + 1)}

# Initialize agent profiles with unique IDs and strategies
agent_profiles = []
agents_per_strategy = n_agents // n_strats
print(agents_per_strategy)







for i in range(n_agents):
    strategy_id = (i // agents_per_strategy) % n_strats + 1  # Ensure strategy_id ranges between 1 and n_strats
    
    agent_profiles.append({
        'id': i,
        'strategy_id': strategy_id,
        'strategy_factor': 0.1,  # Randomly choose a strategy probability between 0 and 1
        # 'strategy_factor': np.random.rand(),  # Randomly choose a strategy probability between 0 and 1
        'strategy_days': 5, 
        # 'p': 0.561,  # Initial probability
        'p':  np.random.rand(),  # Initial probability
        'history': [],
        'cumulative_utility': 0,
        'utility_going': 0,
        'utility_staying': 0
    })

# Create a list of agent IDs
agent_ids = [agent['id'] for agent in agent_profiles]

# Simulation
for day in range(days):

    for i in range(1,n_strats+1):
        history_seperated[i].append(0)

    decisions = []
    # Randomize the order of agent IDs
    np.random.shuffle(agent_ids)
    
    for agent_id in agent_ids:
        agent = next(filter(lambda x: x['id'] == agent_id, agent_profiles))

        # Determine decision based on strategy
        strategy_func = choose_strategy(agent['strategy_id'])
        if callable(strategy_func):  # Check if strategy function is callable
            if (agent['strategy_id'] == 2):
                agent['p'] = strategy_func(agent['strategy_days'], agent['p'], agent['strategy_factor'])
            elif (agent['strategy_id'] == 3):
                agent['p'] = strategy_func(agent['strategy_days'], agent['p'])
            else: 
                agent['p'] = strategy_func(agent['strategy_days'], agent['p']) 

        decision = np.random.binomial(1, agent['p'])
        decisions.append(decision)
        
        # if (agent['strategy_id'] == 1):
        history_seperated[agent['strategy_id']][day]+=decision
        # # elif (agent['strategy_id'] == 2):
        #     history_seperated[2]+=decision
        # else:
        #     history_seperated[3]+=decision

    n_going = np.sum(decisions)
    history.append(n_going)

    for agent_id, decision in zip(agent_ids, decisions):
        agent = next(filter(lambda x: x['id'] == agent_id, agent_profiles))
        agent_utility = payoff(n_going, decision)  # Use the payoff function here
        agent['cumulative_utility'] += agent_utility  # Update cumulative utility
        agent['utility_going'] += agent_utility if decision == 1 else 0
        agent['utility_staying'] += agent_utility if decision == 0 else 0
        
        agent['history'].append({
            'day': day,
            'decision': decision,
            'n_going': n_going,
            'utility': agent_utility
        })

# Calculate average utilities for agents going and staying
average_utilities_going = [agent['utility_going'] for agent in agent_profiles]
average_utilities_staying = [agent['utility_staying'] for agent in agent_profiles]
cumulative_utilities = [agent['cumulative_utility'] for agent in agent_profiles]

# Determine the colors and shapes for each cluster
color_mapping = {
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'red',
    5: 'purple',
    6: 'brown',
}
shapes = ['o', 's']  # Circles for going, squares for staying

# Plotting average utilities for agents going and staying
plt.figure(figsize=(12, 6))

for agent in agent_profiles:
    color = color_mapping[agent['strategy_id']]  # Get the color based on the agent's strategy ID
    plt.scatter(agent['id'], agent['cumulative_utility'], c=color, marker='x')

plt.xlabel('Agent ID')
plt.ylabel('Cumulative Utility')
plt.title(f'Cumulative Utility of Agents by Strategy over {days} Days')
plt.grid(True)
plt.show()


# Plotting the history of the number of agents going to the bar over time
plt.figure(figsize=(12, 6))

plt.plot(range(1, days + 1), history, label='Overall', color='black', linewidth=1)

# # Plot history for each strategy
# for strategy_id, counts in history_seperated.items():
#     color = color_mapping[strategy_id]  # Get the color based on the strategy ID
#     plt.plot(range(1, len(counts) + 1), counts, label=f'Strategy {strategy_id}', color=color, linestyle='--')

plt.xlabel('Day')
plt.ylabel('Number of Agents at Bar')
plt.title('Bar attendance over time')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the history of the number of agents going to the bar over time
# plt.figure(figsize=(12, 6))

# bottom = np.zeros(days)  # Initialize the bottom of the bars to zero

# Plotting a stacked bar chart for each strategy
# for strategy_id, counts in history_seperated.items():
#     color = color_mapping[strategy_id]  # Get the color based on the strategy ID
#     plt.bar(range(1, len(counts) + 1), counts, label=f'Strategy {strategy_id}', color=color, alpha=0.6, bottom=bottom)
#     bottom += np.array(counts)  # Update the bottom for the next set of bars

# plt.xlabel('Day')
# plt.ylabel('Number of Agents at Bar')
# plt.title('Bar attendance over time by strategy')
# plt.legend()
# plt.grid(True)
# plt.show()


cumulative_utilities_by_strategy = {i: [0] * days for i in range(1, n_strats + 1)}  # Initialize with zeros for each day

for agent in agent_profiles:
    strategy_id = agent['strategy_id']
    cumulative_utility = 0
    for day in range(days):
        total_utility = sum(agent['history'][d]['utility'] for d in range(day + 1) if agent['strategy_id'] == strategy_id)
        cumulative_utility += total_utility
        cumulative_utilities_by_strategy[strategy_id][day] = total_utility

for strategy_id, cumulative_utilities in cumulative_utilities_by_strategy.items():
    color = color_mapping[strategy_id]  # Get the color based on the strategy ID
    plt.plot(range(1, days + 1), cumulative_utilities, label=f'Strategy {strategy_id}', color=color)

plt.xlabel('Day')
plt.ylabel('Cumulative Utility')
plt.title('Cumulative Utility by Strategy Over Time')
plt.legend()
plt.grid(True)
plt.show()
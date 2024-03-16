import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
n_simulations = 1000  # Number of times the simulation is run
n_agents = 101  # Total number of agents
threshold_crowded = 50  # Threshold for the bar to be considered crowded
p = 0.495  # Probability of each agent deciding to go to the bar
# p = 0.548  # Probability of each agent deciding to go to the bar

# Initialize counters
times_crowded = 0
go_decisions = []

# Run simulations
for _ in range(n_simulations):
    decisions = np.random.binomial(1, p, n_agents)  # Each agent's decision to go (1) or not go (0)
    n_going = np.sum(decisions)  # Number of agents deciding to go
    go_decisions.append(n_going)
    
    if n_going >= threshold_crowded:
        times_crowded += 1

# Plot the results
plt.figure(figsize=(10, 6))
plt.hist(go_decisions, bins=range(n_agents+1), alpha=0.7, color='blue', edgecolor='black')
plt.axvline(x=threshold_crowded, color='red', linestyle='dashed', linewidth=2, label='Crowded Threshold (50)')
plt.title('Distribution of Number of Agents Going to the Bar')
plt.xlabel('Number of Agents Going to the Bar')
plt.ylabel('Frequency')
plt.legend()
plt.show()

times_crowded, np.mean(go_decisions)

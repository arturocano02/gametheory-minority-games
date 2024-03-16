import numpy as np
import matplotlib.pyplot as plt

def utility(n_going, total_agents, threshold):
    if n_going >= threshold:
        return -((1 / (total_agents - threshold)) * (n_going - threshold))
    else:
        return (1 / threshold) * n_going

def expected_utilities(p, total_agents, threshold):
    # Expected number going based on p
    n_going_expected = p * total_agents
    
    # Calculate expected utility for going and staying
    E_G = utility(n_going_expected, total_agents, threshold)  # Include self in going
    E_S = -utility(n_going_expected, total_agents, threshold)  # Not including self
    
    return E_G, E_S

# Simulation parameters
total_agents = 101  # Total agents excluding self
threshold = 50

# Vary p to find when E_G = E_S
ps = np.linspace(0, 1, 10000)  # Varying p from 0 to 1
E_Gs = []
E_Ss = []

for p in ps:
    E_G, E_S = expected_utilities(p, total_agents, threshold)
    E_Gs.append(E_G)
    E_Ss.append(E_S)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(ps, E_Gs, label='$E_G$ (Expected Utility of Going)')
plt.plot(ps, E_Ss, label='$E_S$ (Expected Utility of Staying)')
plt.xlabel('Probability of Going ($p$)')
plt.ylabel('Expected Utility')
plt.title('Expected Utility of Going vs. Staying as a Function of $p$')
plt.axhline(y=0, color='gray', linestyle='--')  # Reference line at y=0
plt.legend()
plt.grid(True)
plt.show()

# Finding p where E_G and E_S intersect
# For a more analytical approach, one could use root finding on the difference between E_G and E_S,
# but given the direct relationship, we can visually identify the equilibrium from the plot.

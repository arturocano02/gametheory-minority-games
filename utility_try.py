import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def utility_going(n_going, n_agents, threshold_crowded):
    if n_going >= threshold_crowded:
        return -((1 / (n_agents - threshold_crowded)) * (n_going - threshold_crowded))
    else:
        return (1 / threshold_crowded) * n_going

def utility_staying(n_going, n_agents, threshold_crowded):
    return -utility_going(n_going, n_agents, threshold_crowded)  # Assuming the utility of staying is the negative of going

def calculate_expected_utilities(p, n_agents, threshold_crowded):
    E_G, E_S = 0, 0
    for n_going in range(n_agents + 1):
        prob = comb(n_agents, n_going) * (p ** n_going) * ((1 - p) ** (n_agents - n_going))
        E_G += prob * utility_going(n_going , n_agents , threshold_crowded)  # +1 for including the player of interest
        E_S += prob * utility_staying(n_going, n_agents, threshold_crowded)
    return E_G, E_S

# Simulation parameters
n_agents = 101
threshold_crowded = 50

# Varying p and calculating expected utilities
ps = np.linspace(0, 1, 50000)
E_Gs = []
E_Ss = []

for p in ps:
    E_G, E_S = calculate_expected_utilities(p, n_agents, threshold_crowded)
    E_Gs.append(E_G)
    E_Ss.append(E_S)

# Finding where E_G and E_S are approximately equal
# equilibrium_ps = ps[np.isclose(E_Gs, E_Ss, atol=1e-2)]  # Adjust atol based on acceptable tolerance

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(ps, E_Gs, label='Expected Utility of Going')
plt.plot(ps, E_Ss, label='Expected Utility of Staying')
# if len(equilibrium_ps) > 0:
#     for eq_p in equilibrium_ps:
#         plt.axvline(x=eq_p, color='r', linestyle='--', label=f'Equilibrium at p ~ {eq_p:.2f}')
plt.xlabel('Probability of Going (p)')
plt.ylabel('Expected Utility')
plt.title('Expected Utilities of Going vs. Staying')
plt.legend()
plt.grid(True)
plt.show()

print(f"Equilibrium probabilities where E_G = E_S: {equilibrium_ps}")

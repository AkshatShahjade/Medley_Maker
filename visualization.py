import math
from storage.crud import search_pieces
import matplotlib.pyplot as plt
import numpy as np

def skew_norm(x, mu, sig, alpha):
    """
    Skew-Normal Distribution PDF.
    Better models the 'Musical Reminiscence Bump' where recognizability
    peaks at a specific coming-of-age year, but has an asymmetric tail 
    (e.g., dropping off sharply for older adults but tailing slowly for younger listeners).
    """
    # Standardize x
    t = (x - mu) / sig
    
    # Standard normal PDF
    pdf = (1 / (math.sqrt(2 * math.pi))) * math.exp(-0.5 * t**2)
    
    # Standard normal CDF
    cdf = 0.5 * (1 + math.erf((alpha * t) / math.sqrt(2)))
    
    return (2 / sig) * pdf * cdf

# SIG = 5.0 models a 5-year standard deviation spread, more realistic than 0.1
SIG = 5.0  
# ALPHA > 0 creates a right-skewed tail 
ALPHA = 2.0  

def visualize(medley_name: str):
    M_i = [piece.song.getDemographic() for piece in search_pieces(medley_name=medley_name)]
    
    if not M_i:
        print(f"No pieces found for medley: {medley_name}")
        return None

    # Use our new Skew-Normal function
    demo_distribution = lambda x: sum(skew_norm(x, demo, SIG, ALPHA) for demo in M_i)
           
    x_values = np.linspace(0, 100, 500)
    y_values = [demo_distribution(x) for x in x_values]
    
    # Create a new figure so multiple medleys don't overwrite the same graph
    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, label=f'"{medley_name}" Demographic', color='blue')
    plt.xlabel("Demographic Age")
    plt.ylabel("Recognizability Density")
    plt.title(f"Target Audience Distribution: {medley_name}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Make the plot non-blocking so the CLI REPL can continue!
    plt.show(block=False)
    plt.pause(0.1) # Required to force matplotlib to render the non-blocking window
    
    return demo_distribution

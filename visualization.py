import matplotlib.pyplot as plt
import numpy as np
from storage.crud import search_pieces
from storage.math_model.core_math import calculate_medley_recognizability, normalize_distribution

def visualize(medley_name: str):
    pieces = search_pieces(medley_name=medley_name)
    
    if not pieces:
        print(f"No pieces found for medley: {medley_name}")
        return None

    # X-axis is now current Listener Ages from 0 to 100
    target_ages = list(range(101))
    
    # Get the convolved mathematically perfect recognizability curve (dict)
    raw_curve = calculate_medley_recognizability(pieces, target_ages)
    
    # Normalize so the probabilities sum to 1.0
    normalized_curve = normalize_distribution(raw_curve)
    
    # Extract X and Y values for matplotlib
    x_values = list(normalized_curve.keys())
    y_values = list(normalized_curve.values())
    
    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, label=f'"{medley_name}" Recognizability', color='blue')
    plt.xlabel("Listener Current Age")
    plt.ylabel("Normalized Recognizability Probability")
    plt.title(f"Medley Audience Fit: {medley_name}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Make the plot non-blocking so the CLI REPL can continue!
    plt.show(block=False)
    plt.pause(0.1) 
    
    return normalized_curve

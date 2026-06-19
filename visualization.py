import matplotlib.pyplot as plt
import numpy as np
from storage.crud import search_pieces
from storage.math_model.core_math import calculate_medley_recognizability, normalize_distribution, human_susceptibility, get_provider, HISTORICAL_YEAR_START, CURRENT_YEAR

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

def visualize_human_susceptibility():
    ages = list(range(101))
    susceptibility = [human_susceptibility(age) for age in ages]
    
    plt.figure(figsize=(8, 5))
    plt.plot(ages, susceptibility, label='Human Memory Susceptibility', color='green')
    plt.xlabel("Age at the Time")
    plt.ylabel("Susceptibility Multiplier")
    plt.title("The Musical Reminiscence Bump")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.show(block=False)
    plt.pause(0.1)

def visualize_song_popularity(song):
    provider = get_provider()
    # Let's say range 1940 to current_year + 5
    year_range = list(range(HISTORICAL_YEAR_START, CURRENT_YEAR + 5))
    popularity_data = provider.get_popularity_timeseries(song, year_range)
    
    x_values = year_range
    y_values = [popularity_data.get(y, 0.0) for y in year_range]
    
    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, label=f'Popularity: "{song.name}"', color='purple')
    plt.xlabel("Year")
    plt.ylabel("Popularity (0.0 - 1.0)")
    plt.title(f"Historical Popularity Curve: {song.name}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.show(block=False)
    plt.pause(0.1)

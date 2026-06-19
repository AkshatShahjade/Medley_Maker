import math
import datetime
from storage.sql_schema import Song, Piece
from .song_data_switch import get_provider

# Constants for convolution
CURRENT_YEAR = datetime.datetime.now().year
HISTORICAL_YEAR_START = 1940
HISTORICAL_YEAR_END = CURRENT_YEAR

def skew_norm(x, mu, sig, alpha):
    """
    Skew-Normal Distribution PDF.
    Used for human memory susceptibility.
    """
    t = (x - mu) / sig
    pdf = (1 / (math.sqrt(2 * math.pi))) * math.exp(-0.5 * t**2)
    cdf = 0.5 * (1 + math.erf((alpha * t) / math.sqrt(2)))
    return (2 / sig) * pdf * cdf

def human_susceptibility(age: int) -> float:
    """
    Returns the susceptibility of forming a long-term musical memory at a given age.
    Peaks around 15, drops sharply for older adults, tails off for younger kids.
    If age is negative (they weren't born yet), susceptibility is 0.
    """
    if age < 0:
        return 0.0
    # Mu=12, Sig=5, Alpha=3 creates a beautiful curve peaking around 14-16
    return skew_norm(age, mu=12.0, sig=5.0, alpha=3.0)

def calculate_song_recognizability(song: Song, target_ages: list[int]) -> list[float]:
    """
    Convolves the song's popularity over time with human memory susceptibility.
    
    Returns a list of recognizability scores corresponding to the target_ages.
    """
    provider = get_provider()
    year_range = list(range(HISTORICAL_YEAR_START, HISTORICAL_YEAR_END + 1))
    
    # 1. Get the data-driven popularity curve for this song
    popularity_data = provider.get_popularity_timeseries(song, year_range)
    
    recognizability_scores = []
    
    for age in target_ages:
        birth_year = CURRENT_YEAR - age
        total_recognizability = 0.0
        
        # 2. Integrate (sum) the overlap across all historical years
        for year in year_range:
            pop = popularity_data.get(year, 0.0)
            
            listener_age_in_year = year - birth_year
            susceptibility = human_susceptibility(listener_age_in_year)
            
            # The memory formed that year is popularity * how susceptible they were
            total_recognizability += (pop * susceptibility)
            
        recognizability_scores.append(total_recognizability)
        
    return recognizability_scores

def calculate_medley_recognizability(pieces: list[Piece], target_ages: list[int]) -> list[float]:
    """
    Calculates the combined recognizability of an entire medley.
    """
    if not pieces:
        return [0.0] * len(target_ages)
        
    medley_scores = [0.0] * len(target_ages)
    
    for piece in pieces:
        song_scores = calculate_song_recognizability(piece.song, target_ages)
        # Sum the scores element-wise
        for i in range(len(target_ages)):
            medley_scores[i] += song_scores[i]
            
    return medley_scores

def calculate_audience_fit(medley_curve: list[float], audience_curve: list[float]) -> float:
    """
    Calculates the dot product of the medley's recognizability curve 
    and the audience's demographic age distribution.
    """
    if len(medley_curve) != len(audience_curve):
        raise ValueError("Curves must be the same length to calculate fit.")
        
    fit_score = sum(m * a for m, a in zip(medley_curve, audience_curve))
    return fit_score

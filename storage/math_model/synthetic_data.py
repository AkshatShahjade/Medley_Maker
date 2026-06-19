import math
import random
from typing import Dict
from storage.sql_schema import Song
from .song_data_interface import SongDataProvider

class SyntheticDataProvider(SongDataProvider):
    def get_popularity_timeseries(self, song: Song, year_range: list[int]) -> Dict[int, float]:
        """
        Generates a synthetic, data-driven-looking popularity curve.
        It centers a large spike at the song's release year and slowly decays,
        with random noise to simulate 'sleeper' hits or viral resurgences.
        """
        timeseries = {}
        
        # Use the song's ID to seed the random generator so the curve is deterministic
        # for a given song across multiple runs.
        random.seed(song.id)
        
        for year in year_range:
            if year < song.release_year:
                # Song didn't exist yet!
                timeseries[year] = 0.0
            else:
                years_since_release = year - song.release_year
                
                # Exponential decay from the initial release hype
                base_popularity = math.exp(-0.15 * years_since_release)
                
                # Random viral resurgences (e.g. TikTok, movies)
                # 5% chance of a random spike in any given year
                spike = random.uniform(0.1, 0.8) if random.random() < 0.05 else 0.0
                
                # Cap at 1.0
                timeseries[year] = min(1.0, base_popularity + spike)
                
        return timeseries

import math
from typing import Dict
from storage.sql_schema import Song
from .song_data_interface import SongDataProvider

class SyntheticDataProvider(SongDataProvider):
    def get_popularity_timeseries(self, song: Song, year_range: list[int]) -> Dict[int, float]:
        """
        Generates a synthetic, data-driven-looking popularity curve.
        It centers a large spike at the song's release year and slowly decays.
        """
        timeseries = {}
        
        for year in year_range:
            if year < song.release_year:
                # Song didn't exist yet!
                timeseries[year] = 0.0
            else:
                years_since_release = year - song.release_year
                
                # Exponential decay from the initial release hype
                base_popularity = math.exp(-0.15 * years_since_release)
                
                timeseries[year] = base_popularity
                
        return timeseries

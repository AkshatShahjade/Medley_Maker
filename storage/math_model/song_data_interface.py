from abc import ABC, abstractmethod
from typing import Dict
from storage.sql_schema import Song

class SongDataProvider(ABC):
    @abstractmethod
    def get_popularity_timeseries(self, song: Song, year_range: list[int]) -> Dict[int, float]:
        """
        Returns a dictionary mapping a specific year (e.g., 2005) to 
        the song's popularity score (0.0 to 1.0) in that year.
        
        Args:
            song (Song): The song to fetch data for.
            year_range (list[int]): The sequence of years to query.
            
        Returns:
            Dict[int, float]: A mapping of year to popularity score.
        """
        pass

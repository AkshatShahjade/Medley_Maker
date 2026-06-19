from typing import Dict
from storage.sql_schema import Song
from .song_data_interface import SongDataProvider
from .synthetic_data import SyntheticDataProvider

class GoogleTrendsProvider(SongDataProvider):
    def __init__(self):
        # Import inside the class so it doesn't crash the whole app if pytrends is missing
        from pytrends.request import TrendReq
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.synthetic_fallback = SyntheticDataProvider()
        
    def get_popularity_timeseries(self, song: Song, year_range: list[int]) -> Dict[int, float]:
        timeseries = {}
        
        # We search by exact song name. You could append " song" to be more specific.
        kw_list = [song.name]
        
        try:
            # Timeframe 'all' gets data from 2004 to present.
            # Using sleep to prevent aggressive rate limiting.
            self.pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='')
            df = self.pytrends.interest_over_time()
            
            if not df.empty and song.name in df.columns:
                # Group by year and take the mean popularity for that year
                df['year'] = df.index.year
                yearly_avg = df.groupby('year')[song.name].mean()
                
                # Google Trends returns 0-100. Scale it to 0.0-1.0
                max_val = yearly_avg.max()
                if max_val > 0:
                    yearly_avg = yearly_avg / max_val
                
                for year, val in yearly_avg.items():
                    timeseries[year] = float(val)
            else:
                raise ValueError("Empty DataFrame or song not found in results.")
                
        except Exception as e:
            # If Google rate limits us or throws an error, fallback entirely to synthetic
            print(f"  [Warning] PyTrends failed for '{song.name}' ({e}). Falling back to synthetic data.")
            return self.synthetic_fallback.get_popularity_timeseries(song, year_range)

        # ---------------------------------------------------------
        # HYBRID STITCHING (Option A)
        # ---------------------------------------------------------
        # For years prior to 2004, Google Trends has no data. We use the 
        # synthetic generator to fill in the pre-2004 history!
        synthetic_data = self.synthetic_fallback.get_popularity_timeseries(song, year_range)
        
        final_timeseries = {}
        for year in year_range:
            if year < 2004:
                final_timeseries[year] = synthetic_data.get(year, 0.0)
            else:
                final_timeseries[year] = timeseries.get(year, 0.0)
                
        return final_timeseries

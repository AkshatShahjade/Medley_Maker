from .song_data_interface import SongDataProvider
from .synthetic_data import SyntheticDataProvider

# Global configuration variable for the adapter
USE_SYNTHETIC = False

def get_provider() -> SongDataProvider:
    """
    Returns the active SongDataProvider based on the global configuration.
    """
    if USE_SYNTHETIC:
        return SyntheticDataProvider()
    else:
        from .pytrends_data import GoogleTrendsProvider
        return GoogleTrendsProvider()

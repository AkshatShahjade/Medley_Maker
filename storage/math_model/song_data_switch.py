from .song_data_interface import SongDataProvider
from .synthetic_data import SyntheticDataProvider

# Global configuration variable for the adapter
USE_SYNTHETIC = True

def get_provider() -> SongDataProvider:
    """
    Returns the active SongDataProvider based on the global configuration.
    """
    if USE_SYNTHETIC:
        return SyntheticDataProvider()
    else:
        # In the future, you can add real API providers like Google Trends here.
        # return SpotifyTrendsProvider()
        raise NotImplementedError("Real API provider is not yet implemented.")

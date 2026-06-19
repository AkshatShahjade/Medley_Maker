# Parking Document

## Future Enhancements
*   **Database Caching for Google Trends**: Implement a `popularity_cache` column in the `songs` table (using `String` type with JSON data). This will store the Google Trends API results locally in SQLite, dramatically speeding up `visualization.py` rendering and preventing Google API rate limits.s

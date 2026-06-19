# Mathematical Model Assumptions

The Medley Maker recommendation engine calculates the "Medley-Audience Fit" by convolving real-world cultural data with human cognitive psychology. To achieve this mathematically, the engine relies on the following core assumptions:

### 1. The Musical Reminiscence Bump (Cognitive Susceptibility)
We assume that the human brain's ability to form deep, nostalgic, and highly recognizable memories of a song is heavily tied to the listener's age at the time they heard it.
- Based on cognitive psychology research, this "Reminiscence Bump" peaks during coming-of-age years (typically ages 14–16).
- The drop-off is asymmetric: older adults (who are already fully grown when a new trend hits) are far less susceptible to forming long-term memories of new pop songs than young children (who might hear it as a "classic").
- **Mathematical Modeling:** This is modeled in `core_math.py` using a right-skewed **Skew-Normal Distribution** (`μ=12`, `σ=5`, `α=3`).

### 2. Dynamic Cultural Popularity (The Viral Factor)
We reject the assumption that a song's recognizability is statically tied to its `release_year`. 
- We assume that recognizability is tied to *actual cultural exposure*.
- For example, Kate Bush's *Running Up That Hill* (released in 1985) went globally viral in 2022 due to *Stranger Things*. Our model assumes that 15-year-olds in 2022 will have a strong cognitive memory of this song, which a static `release_year` model would incorrectly ignore.
- **Mathematical Modeling:** This is handled by fetching raw time-series search data (`0.0` to `1.0`) from the Google Trends API (`pytrends_data.py`).

### 3. The Convolution Principle (Recognizability)
We assume that an individual's total lifetime recognizability of a song is the mathematical integration (convolution) of the two factors above.
- For every year in history ($t$), we calculate: `Song Popularity at year t` × `Listener's Susceptibility at year t`.
- We assume that summing these yearly overlaps across the listener's entire lifespan accurately yields their total Recognizability Score for that song today.

### 4. Pre-Internet Data (The 2004 Limitation)
Because Google Trends only provides data going back to 2004, we must make an assumption about older music.
- For any song released prior to 2004 (e.g., *Ek Ladki Bheegi Bhaagi Si* in 1958), we assume its popularity followed a standard **exponential decay curve** starting from its `release_year`.
- **Mathematical Modeling:** Our Hybrid Architecture (`pytrends_data.py`) automatically stitches our theoretical exponential decay curve (for years `< 2004`) directly into the real-world Google Trends data (for years `≥ 2004`).
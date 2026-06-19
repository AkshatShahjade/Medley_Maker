from sqlalchemy.orm import Session
from .initialize_sql import get_engine
from .sql_schema import Song, Piece, Medley
import random

def seed_db():
    songs_data = [
        ("Ek Ladki Bheegi Bhaagi Si", 1958, "https://www.youtube.com/watch?v=kBKA3g8WTuE"),
        ("De De Pyaar De", 1984, "https://www.youtube.com/watch?v=ztLjAiErnFc"),
        ("Chahun Main Ya Naa", 2013, "https://www.youtube.com/watch?v=ww8htBCIqm8"),
        ("Disco Dancer - I Am A Disco Dancer", 1982, "https://www.youtube.com/watch?v=pKwNDsBxXRA"),
        ("Tum Se Hi", 2007, "https://www.youtube.com/watch?v=mt9xg0mmt28"),
        ("Lag Ja Gale", 1964, "https://www.youtube.com/watch?v=y2fgw1Oqz28"),
        ("Main Agar Kahoon", 2007, "https://www.youtube.com/watch?v=DAYszemgPxc"),
        ("Pal Pal Dil Ke Paas", 1973, "https://www.youtube.com/watch?v=AMuRRXCuy-4"),
        ("Gehra Hua", 2025, "https://www.youtube.com/watch?v=2kvtJL8Keog"),
        ("Phir Bhi Tumko Chaahunga", 2017, "https://www.youtube.com/watch?_iktURk0X-A"),
        ("Sapna Jahan", 2015, "https://www.youtube.com/watch?v=lHJp_3g2MAI"),
        ("Itni Si Baat Hain", 2016, "https://www.youtube.com/watch?v=jhPtPGKdQ-w"),
        ("Choo Lene Do Nazuk Hothon Ko", 1965, "https://www.youtube.com/watch?v=SZTBAdhBgTw"),
        ("Tere Mere Hothon Pe", 1989, "https://www.youtube.com/watch?v=h7Sf3v7qhmw"),
        ("Pankh Hote To Ud Aati", 1963, "https://www.youtube.com/watch?v=YEN9DoPNs4s"),
        ("Milne Hai Mujhse Aayi", 2013, "https://www.youtube.com/watch?v=GtPvCa3vvxA"),
        ("Kaise Mujhe", 2008, "https://www.youtube.com/watch?v=uC1iJcYOyeY"),
    ]

    with Session(get_engine()) as session:
        # Create Medleys
        medley1 = Medley(name="Retro Hits", nickname="retro")
        medley2 = Medley(name="Modern Mix", nickname="modern")
        session.add_all([medley1, medley2])
        
        # Create Songs and Pieces
        for idx, s_data in enumerate(songs_data):
            song = Song(name=s_data[0], release_year=s_data[1], url=s_data[2])
            session.add(song)
            
            # Create 2 pieces per song
            for p_idx in range(2):
                piece = Piece(
                    name=f"{song.name} - Part {p_idx + 1}",
                    emotion=round(random.uniform(0.0, 1.0), 2),
                    energy=round(random.uniform(0.0, 1.0), 2),
                    tempo=round(random.uniform(60.0, 180.0), 2),
                    st_time=round(random.uniform(0.0, 60.0), 2),
                    end_time=round(random.uniform(60.0, 180.0), 2),
                    song=song
                )
                session.add(piece)
                
                # Assign to medleys randomly or based on index
                if (idx + p_idx) % 5 == 0:
                    medley1.pieces.append(piece)
                elif (idx + p_idx) % 7 == 3:
                    medley2.pieces.append(piece)

        session.commit()

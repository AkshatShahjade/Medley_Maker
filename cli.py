import cmd
import sys
from storage.initialize_sql import initialize_db
from storage.seeding import seed_db
from storage.crud import search_songs, search_pieces, search_medleys, save, delete, get_all
from storage.sql_schema import Song, Piece, Medley
from visualization import visualize, visualize_human_susceptibility, visualize_song_popularity

class MedleyCLI(cmd.Cmd):
    intro = "Welcome to Medley Maker CLI.\nType 'help' or '?' to list commands."
    prompt = "(medley) "

    def do_initdb(self, arg):
        """Initialize the database and seed with data."""
        initialize_db()
        seed_db()
        print("Database initialized and seeded.")

    def do_list(self, arg):
        """List all records in a table. Usage: list <songs|pieces|medleys>"""
        if arg == "songs":
            for s in search_songs():
                print(f"[{s.id}] {s.name} ({s.release_year}) - {len(s.pieces)} pieces")
        elif arg == "pieces":
            for p in search_pieces():
                print(f"[{p.id}] {p.name} (Tempo: {p.tempo}) - from Song '{p.song.name}'")
        elif arg == "medleys":
            for m in search_medleys():
                print(f"[{m.id}] {m.name} ({m.nickname}) - {len(m.pieces)} pieces")
        else:
            print("Invalid table. Usage: list <songs|pieces|medleys>")

    def do_create(self, arg):
        """Interactive creation of a Medley or Song. Usage: create <song|medley>"""
        if arg == "song":
            name = input("Name: ")
            url = input("URL: ")
            try:
                year = int(input("Release Year: "))
                save(Song(name=name, url=url, release_year=year))
                print("Song created.")
            except ValueError:
                print("Invalid year.")
        elif arg == "medley":
            name = input("Name: ")
            nickname = input("Nickname: ")
            save(Medley(name=name, nickname=nickname))
            print("Medley created.")
        else:
            print("Interactive Piece creation is currently unsupported here. Try 'song' or 'medley'.")

    def do_delete(self, arg):
        """Delete a record by type and ID. Usage: delete <song|piece|medley> <id>"""
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: delete <type> <id>")
            return
        
        table, record_id = parts[0], parts[1]
        try:
            record_id = int(record_id)
        except ValueError:
            print("ID must be an integer.")
            return

        target = None
        if table == "song":
            records = [s for s in search_songs() if s.id == record_id]
            if records: target = records[0]
        elif table == "piece":
            records = [p for p in search_pieces() if p.id == record_id]
            if records: target = records[0]
        elif table == "medley":
            records = [m for m in search_medleys() if m.id == record_id]
            if records: target = records[0]
        else:
            print("Invalid type.")
            return

        if target:
            delete(target)
            print(f"Deleted {table} ID {record_id}.")
        else:
            print(f"No {table} found with ID {record_id}.")

    def do_visualize(self, arg):
        """Visualize a medley's demographic distribution. Usage: visualize <medley_name>"""
        if not arg:
            print("Please provide a medley name. Example: visualize Retro Hits")
            return
        
        print(f"Visualizing demographic distribution for '{arg}'...")
        try:
            visualize(arg)
        except Exception as e:
            print(f"Failed to visualize: {e}")

    def do_math(self, arg):
        """Visualize math models. Usage: math <"human" | song_id>"""
        arg = arg.strip().lower()
        if not arg:
            print("Usage: math human OR math <song_id>")
            return
            
        if arg == "human":
            print("Visualizing human memory susceptibility...")
            visualize_human_susceptibility()
        else:
            try:
                song_id = int(arg)
                records = [s for s in search_songs() if s.id == song_id]
                if records:
                    print(f"Visualizing historical popularity for Song '{records[0].name}'...")
                    visualize_song_popularity(records[0])
                else:
                    print(f"No song found with ID {song_id}.")
            except ValueError:
                print("Argument must be 'human' or a valid integer song ID.")
            except Exception as e:
                print(f"Failed to visualize: {e}")

    def do_EOF(self, arg):
        """Exit the CLI."""
        print()
        return True

    def do_exit(self, arg):
        """Exit the CLI."""
        print("Goodbye!")
        return True

if __name__ == '__main__':
    MedleyCLI().cmdloop()

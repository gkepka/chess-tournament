import psycopg2
from dao.ConnectionProvider import ConnectionProvider


class DatabaseInitializer:
    table_player = """
    CREATE TABLE IF NOT EXISTS chess_player (
        player_id SERIAL PRIMARY KEY,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20) NOT NULL,
        ranking INT NOT NULL,
        title VARCHAR(10),
        nationality VARCHAR(3) NOT NULL
        );
    """

    table_tournament = """
    CREATE TABLE IF NOT EXISTS tournament (
        tournament_id SERIAL PRIMARY KEY,
        max_places INT NOT NULL,
        max_rounds INT NOT NULL
        );
    """

    table_player_in_tournament = """
    CREATE TABLE IF NOT EXISTS player_in_tournament (
        player_id INT NOT NULL,
        tournament_id INT NOT NULL,
        current_score INT NOT NULL,
        current_buchholz INT NOT NULL,
        did_pause BOOL NOT NULL,
        FOREIGN KEY (player_id) REFERENCES chess_player(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id) ON UPDATE CASCADE ON DELETE CASCADE,
        PRIMARY KEY (player_id, tournament_id)
        );
    """

    table_match = """
    CREATE TABLE IF NOT EXISTS match (
        match_id SERIAL PRIMARY KEY,
        tournament_id INT NOT NULL,
        player_white_id INT NOT NULL,
        player_black_id INT NOT NULL,
        result INT NOT NULL,
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (player_white_id) REFERENCES chess_player(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (player_black_id) REFERENCES chess_player(player_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """

    def __init__(self):
        self.connection_provider = ConnectionProvider()

    def create_tables(self):
        conn = None
        try:
            conn = self.connection_provider.get_connection()
            cur = conn.cursor()

            for command in [self.table_player, self.table_tournament, self.table_player_in_tournament,
                            self.table_match]:
                cur.execute(command)

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.connection_provider.free_connection(conn)

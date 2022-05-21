import psycopg2

from dao.ConnectionProvider import get_connection_provider

from model.Match import Match
from model.Tournament import Tournament
from model.Player import Player
from model.PlayerParams import PlayerParams


class MatchDAO:

    def __init__(self):
        self.__connection_provider = get_connection_provider()

    def insert_match(self, match):
        """Inserts match into database, returns generated match_id"""
        conn = None
        match_id = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            INSERT INTO match(tournament_id, player_white_id, player_black_id, result)
            VALUES (%s, %s, %s, %s) RETURNING match_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [match.tournament.tournament_id, match.player_white.player_id, match.player_black.player_id,
                        match.get_result()])
            match_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return match_id

    def get_match_by_id(self, match_id):
        """Returns match with specified match_id"""
        conn = None
        match = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT tournament_id, player_white_id, player_black_id, result
            FROM match
            WHERE match_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [match_id])
            row = cur.fetchone()
            tournament_id = row[0]
            player_white_id = row[1]
            player_black_id = row[2]
            result = row[3]

            tournament_dao = TournamentDAO()
            tournament = tournament_dao.get_tournament_by_id(tournament_id)

            player_dao = PlayerDAO()
            player_white = player_dao.get_player_by_id(player_white_id)
            player_black = player_dao.get_player_by_id(player_black_id)

            match = Match(tournament, player_white, player_black, result, match_id)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return match

    def get_matches_for_tournament(self, tournament):
        """Returns list of matches associated with provided tournament"""
        conn = None
        matches = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT match_id FROM match
            WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.tournament_id])

            for row in cur:
                matches.append(self.get_match_by_id(row[0]))

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return matches

    def delete_match(self, match):
        """Deletes match from database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            DELETE FROM match
            WHERE match_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [match.match_id])
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def update_match(self, match):
        """Updates match in database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            UPDATE match SET (tournament_id, player_white_id, player_black_id, result) =
            (%s, %s, %s, %s) WHERE match_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [match.tournament.tournament_id, match.player_white.player_id, match.player_black.player_id,
                        match.result, match.match_id])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)


class PlayerDAO:
    def __init__(self):
        self.__connection_provider = get_connection_provider()

    def insert_player(self, player):
        """Inserts player into database, returns generated player_id"""
        conn = None
        player_id = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            INSERT INTO chess_player(first_name, last_name, ranking, title, nationality, chess_club)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING player_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.name, player.surname, player.rank, player.title, player.nationality, player.chess_club])
            player_id = cur.fetchone()[0]

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error: # zawęzić wyjątki
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return player_id

    def get_all_players(self):
        conn = None
        players = set()
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    SELECT first_name, last_name, ranking, title, nationality,chess_club, player_id FROM chess_player;
                    """
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur:
                name = row[0]
                surname = row[1]
                rank = row[2]
                title = row[3]
                nationality = row[4]
                chess_club = row[5]
                player_id = row[6]
                player = Player(name, surname, rank, title, nationality, chess_club, player_id)
                players.add(player)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return players

    def get_player_by_id(self, player_id):
        conn = None
        player = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT first_name, last_name, ranking, title, nationality, chess_club FROM chess_player
            WHERE player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_id])
            row = cur.fetchone()
            name = row[0]
            surname = row[1]
            rank = row[2]
            title = row[3]
            nationality = row[4]
            chess_club = row[5]

            player = Player(name, surname, rank, title, nationality, chess_club, player_id)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return player

    def delete_player(self, player):
        """Deletes player from database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            DELETE FROM chess_player
            WHERE player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.player_id])
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def update_player(self, player):
        """Updates player in database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            UPDATE chess_player SET (first_name, last_name, ranking, title, nationality, chess_club) =
            (%s, %s, %s, %s, %s, %s) WHERE player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.name, player.surname, player.rank, player.title, player.nationality, player.chess_club, player.player_id])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)


class PlayerParamsDAO:
    def __init__(self):
        self.__connection_provider = get_connection_provider()

    def insert_player_params(self, player_params):
        """Inserts player_params into database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            INSERT INTO player_in_tournament(player_id, tournament_id, current_score, current_buchholz, did_pause)
            VALUES (%s, %s, %s, %s, %s);
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.player.player_id, player_params.tournament.tournament_id,
                        player_params.get_points(), player_params.get_buchholz(), player_params.get_did_pause()])
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def insert_player_params_list(self, player_params_list):
        for player_params in player_params_list:
            self.insert_player_params(player_params)

    def get_player_params_for_player(self, player):
        """Returns list of player_params for player"""
        conn = None
        player_params_list = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT player_id, tournament_id, current_score, current_buchholz, did_pause
            FROM player_in_tournament
            WHERE player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.player_id])

            player_dao = PlayerDAO()
            tournament_dao = TournamentDAO()

            for row in cur:
                player = player_dao.get_player_by_id(row[0])
                tournament = tournament_dao.get_tournament_by_id(row[1])
                player_params = PlayerParams(player, tournament)
                player_params.get_points(row[2])
                player_params.set_buchholz(row[3])
                player_params.set_did_pause(row[4])
                player_params_list.append(player_params)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return player_params_list

    def get_player_params_for_tournament(self, tournament):
        """Returns list of player_params for tournament"""
        conn = None
        player_params_list = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT player_id, tournament_id, current_score, current_buchholz, did_pause
            FROM player_in_tournament
            WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.tournament_id])

            player_dao = PlayerDAO()
            tournament_dao = TournamentDAO()

            for row in cur:
                player = player_dao.get_player_by_id(row[0])
                tournament = tournament_dao.get_tournament_by_id(row[1])
                player_params = PlayerParams(player, tournament)
                player_params.set_points(row[2])
                player_params.set_buchholz(row[3])
                player_params.set_did_pause(row[4])
                player_params_list.append(player_params)

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return player_params_list

    def delete_player_params(self, player_params):
        """Deletes player_params from database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            DELETE FROM player_in_tournament
            WHERE player_id = %s AND tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.player.player_id, player_params.tournament.tournament_id])
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def update_player_params(self, player_params):
        """Updates player_params in database"""
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            UPDATE player_in_tournament SET (current_score, current_buchholz, did_pause) =
            (%s, %s, %s) WHERE player_id = %s AND tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.get_points(), player_params.get_buchholz(), player_params.get_did_pause(),
                        player_params.player.player_id, player_params.tournament.tournament_id])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)


class TournamentDAO:
    def __init__(self):
        self.__connection_provider = get_connection_provider()

    def insert_tournament(self, tournament):
        conn = None
        tournament_id = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            INSERT INTO tournament(name, tournament_date, rounds)
            VALUES (%s, %s, %s) RETURNING tournament_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.name, tournament.date, tournament.rounds])

            tournament_id = cur.fetchone()[0]

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return tournament_id

    def get_tournament_by_id(self, tournament_id):
        conn = None
        tournament = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT name, tournament_date, rounds
            FROM tournament WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament_id])
            row = cur.fetchone()
            tournament = Tournament(row[0], row[1], row[2], tournament_id)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return tournament

    def get_all_tournaments(self):
        conn = None
        tournaments = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT tournament_id, name, tournament_date, rounds
            FROM tournament;
            """
            cur = conn.cursor()
            cur.execute(sql)

            player_params_dao = PlayerParamsDAO()

            for row in cur:
                tournament = Tournament(row[1], row[2], row[3], row[0])
                player_params_list = player_params_dao.get_player_params_for_tournament(tournament)
                for player_params in player_params_list:
                    tournament.add_player_params(player_params)
                tournaments.append(tournament)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return tournaments

    def delete_tournament(self, tournament):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            DELETE FROM tournament
            WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.tournament_id])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def delete_tournament_by_id(self, tournament_id):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            DELETE FROM tournament
            WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament_id])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def update_tournament(self, tournament):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            UPDATE tournament SET (name, tournament_date, rounds) =
            (%s, %s, %s) WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.name, tournament.date, tournament.rounds])

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

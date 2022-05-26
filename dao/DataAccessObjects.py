import psycopg2
import threading

from dao.ConnectionProvider import get_connection_provider

from model.Match import Match
from model.Tournament import Tournament
from model.Player import Player
from model.PlayerParams import PlayerParams
from model.Round import Round


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
            INSERT INTO match(tournament_id, round_id, player_white_id, player_black_id, result)
            VALUES (%s, %s, %s, %s, %s) RETURNING match_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [match.tournament.tournament_id, match.round.round_id, match.player_white.player_id, match.player_black.player_id,
                        match.get_result()])
            match_id = cur.fetchone()[0]
            set_object(match, match_id)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return match_id

    def get_match_by_id(self, match_id):
        """Returns match with specified match_id"""
        conn = None
        match = get_object(match_id, Match)
        if match is not None:
            return match
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT tournament_id, round_id, player_white_id, player_black_id, result
            FROM match
            WHERE match_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [match_id])
            row = cur.fetchone()
            tournament_id = row[0]
            round_id = row[1]
            player_white_id = row[2]
            player_black_id = row[3]
            result = row[4]

            match = Match(None, None, None, None, result, match_id)
            set_object(match, match_id)

            tournament_dao = TournamentDAO()
            tournament = tournament_dao.get_tournament_by_id(tournament_id)

            round_dao = RoundDAO()
            round = round_dao.get_round_by_id(round_id)

            player_dao = PlayerDAO()
            player_white = player_dao.get_player_by_id(player_white_id)
            player_black = player_dao.get_player_by_id(player_black_id)

            match.tournament = tournament
            match.round = round
            match.player_white = player_white
            match.player_black = player_black

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return matches

    def get_matches_for_round_id(self, round_id):
        """Returns list of matches associated with provided round"""
        conn = None
        matches = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT match_id FROM match
            WHERE round_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [round_id])

            for row in cur:
                matches.append(self.get_match_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            set_object(None, match.match_id, Match)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            UPDATE match SET (tournament_id, round_id, player_white_id, player_black_id, result) =
            (%s, %s, %s, %s, %s) WHERE match_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [match.tournament.tournament_id, match.round.round_id, match.player_white.player_id,
                              match.player_black.player_id, match.result, match.match_id])

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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

            set_object(player, player_id)
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
                    SELECT player_id FROM chess_player;
                    """
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur:
                players.add(self.get_player_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return players

    def get_players_for_tournament(self, tournament_id):
        conn = None
        players = set()
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    SELECT chess_player.player_id 
                    FROM chess_player INNER JOIN player_in_tournament pit on chess_player.player_id = pit.player_id
                    INNER JOIN tournament t on t.tournament_id = pit.tournament_id
                    WHERE t.tournament_id = %s;
                    """
            cur = conn.cursor()
            cur.execute(sql, [tournament_id])
            for row in cur:
                players.add(self.get_player_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return players

    def get_player_by_id(self, player_id):
        conn = None
        player = get_object(player_id, Player)
        if player is not None:
            return player
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

            player = Player(name, surname, rank, nationality, title, chess_club, player_id)
            set_object(player, player_id)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            set_object(None, player.player_id, Player)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
        except psycopg2.DatabaseError as error:
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
            INSERT INTO player_in_tournament(player_id, tournament_id, current_score, current_buchholz, did_pause, eliminated)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING player_in_tournament_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.player.player_id, player_params.tournament.tournament_id,
                        player_params.get_points(), player_params.get_buchholz(), player_params.get_did_pause(), player_params.eliminated])

            player_params_id = cur.fetchone()[0]
            player_params.player_params_id = player_params_id
            set_object(player_params, player_params_id)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def insert_player_params_list(self, player_params_list):
        for player_params in player_params_list:
            self.insert_player_params(player_params)

    def get_player_params_by_id(self, player_params_id):
        conn = None
        player_params = get_object(player_params_id, PlayerParams)
        if player_params is not None:
            return player_params
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT player_id, tournament_id, current_score, current_buchholz, did_pause, eliminated
            FROM player_in_tournament
            WHERE player_in_tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params_id])

            player_params = PlayerParams(None, None)
            set_object(player_params, player_params_id)

            row = cur.fetchone()
            player_id = row[0]
            tournament_id = row[1]

            player_dao = PlayerDAO()
            player = player_dao.get_player_by_id(player_id)

            tournament_dao = TournamentDAO()
            tournament = tournament_dao.get_tournament_by_id(tournament_id)

            player_params.tournament = tournament
            player_params.player = player
            player_params.set_points(row[2])
            player_params.set_buchholz(row[3])
            player_params.set_did_pause(row[4])
            player_params.player_params_id = player_params_id
            player_params.eliminated = row[5]

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return player_params

    def get_player_params_for_player(self, player):
        """Returns list of player_params for player"""
        conn = None
        player_params_list = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT player_in_tournament_id
            FROM player_in_tournament
            WHERE player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.player_id])

            for row in cur:
                player_params_list.append(self.get_player_params_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            SELECT player_in_tournament_id
            FROM player_in_tournament
            WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.tournament_id])

            for row in cur:
                player_params_list.append(self.get_player_params_by_id(row[0]))

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
            WHERE player_id = %s AND tournament_id = %s RETURNING player_in_tournament_id;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.player.player_id, player_params.tournament.tournament_id])
            player_params_id = cur.fetchone()[0]
            set_object(None, player_params_id, PlayerParams)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            UPDATE player_in_tournament SET (current_score, current_buchholz, did_pause, eliminated) =
            (%s, %s, %s, %s) WHERE player_id = %s AND tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player_params.get_points(), player_params.get_buchholz(), player_params.get_did_pause(),
                        player_params.eliminated, player_params.player.player_id, player_params.tournament.tournament_id])

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            set_object(tournament, tournament_id)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return tournament_id

    def get_tournament_by_id(self, tournament_id):
        conn = None
        tournament = get_object(tournament_id, Tournament)
        if tournament is not None:
            return tournament
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
            set_object(tournament, tournament_id)

            player_params_dao = PlayerParamsDAO()
            player_params_list = player_params_dao.get_player_params_for_tournament(tournament)
            for player_params in player_params_list:
                tournament.add_player_params(player_params)

            round_dao = RoundDAO()
            rounds = round_dao.get_rounds_by_tournament_id(tournament_id)
            tournament.rounds_list.extend(rounds)

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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
            SELECT tournament_id
            FROM tournament;
            """
            cur = conn.cursor()
            cur.execute(sql)

            for row in cur:
                tournaments.append(self.get_tournament_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return tournaments

    def get_tournaments_for_player(self, player):
        conn = None
        tournaments = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            SELECT tournament.tournament_id
            FROM tournament INNER JOIN player_in_tournament pit on tournament.tournament_id = pit.tournament_id
            INNER JOIN chess_player cp on cp.player_id = pit.player_id
            WHERE cp.player_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [player.player_id])

            for row in cur:
                tournaments.append(self.get_tournament_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
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

            round_dao = RoundDAO()
            for round in tournament.rounds_list:
                round_dao.delete_round(round)

            params_dao = PlayerParamsDAO()
            for params in tournament.params_list:
                params_dao.delete_player_params(params)

            set_object(None, tournament.tournament_id, Tournament)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def delete_tournament_by_id(self, tournament_id):
        self.delete_tournament(self.get_tournament_by_id(tournament_id))

    def update_tournament(self, tournament):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
            UPDATE tournament SET (name, tournament_date, rounds) =
            (%s, %s, %s) WHERE tournament_id = %s;
            """
            cur = conn.cursor()
            cur.execute(sql, [tournament.name, tournament.date, tournament.rounds, tournament.tournament_id])

            round_dao = RoundDAO()
            current_rounds = round_dao.get_rounds_by_tournament_id(tournament.tournament_id)
            rounds_to_add = [round for round in tournament.rounds_list if round not in current_rounds]
            rounds_to_update = [round for round in current_rounds if round in tournament.rounds_list]

            for round in rounds_to_update:
                round_dao.update_round(round)

            for round in rounds_to_add:
                round.round_id = round_dao.insert_round(round)

            player_params_dao = PlayerParamsDAO()
            current_params = player_params_dao.get_player_params_for_tournament(tournament)

            params_to_delete = [params for params in current_params if params not in tournament.params_list]
            params_to_add = [params for params in tournament.params_list if params not in current_params]
            params_to_update = [params for params in tournament.params_list if params not in params_to_add and params not in params_to_delete]

            for player_params in params_to_delete:
                player_params_dao.delete_player_params(player_params)

            player_params_dao.insert_player_params_list(params_to_add)

            for params in params_to_update:
                player_params_dao.update_player_params(params)

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)


class RoundDAO:
    def __init__(self):
        self.__connection_provider = get_connection_provider()

    def insert_round(self, round):
        conn = None
        round_id = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    INSERT INTO round(tournament_id, round_no)
                    VALUES (%s, %s) RETURNING round_id;
                    """
            cur = conn.cursor()
            cur.execute(sql, [round.tournament.tournament_id, round.get_round_no()])
            row = cur.fetchone()
            round_id = row[0]
            round.round_id = round_id
            set_object(round, round_id)
            conn.commit()
            match_dao = MatchDAO()
            for match in round.matches:
                match_dao.insert_match(match)
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return round_id

    def get_round_by_id(self, round_id):
        conn = None
        round = get_object(round_id, Round)
        if round is not None:
            return round
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    SELECT tournament_id, round_no
                    FROM round where round_id = %s;
                    """
            cur = conn.cursor()
            cur.execute(sql, [round_id])

            row = cur.fetchone()
            tournament_id = row[0]
            round_no = row[1]

            round = Round(None, round_no, [], round_id)
            set_object(round, round_id)

            tournament_dao = TournamentDAO()
            tournament = tournament_dao.get_tournament_by_id(tournament_id)
            round.tournament = tournament

            match_dao = MatchDAO()
            matches = match_dao.get_matches_for_round_id(round_id)
            round.matches = matches

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return round

    def get_rounds_by_tournament_id(self, tournament_id):
        conn = None
        rounds = []
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    SELECT round_id
                    FROM round where tournament_id = %s;
                    """
            cur = conn.cursor()
            cur.execute(sql, [tournament_id])

            for row in cur:
                rounds.append(self.get_round_by_id(row[0]))

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)
        return rounds

    def delete_round(self, round):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    DELETE FROM round where round_id = %s;
                    """
            cur = conn.cursor()
            cur.execute(sql, [round.round_id])

            match_dao = MatchDAO()
            for match in round.matches:
                match_dao.delete_match(match)

            set_object(None, round.round_id, Round)
            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)

    def update_round(self, round):
        conn = None
        try:
            conn = self.__connection_provider.get_connection()
            sql = """
                    UPDATE round SET (tournament_id, round_no) = (%s, %s)
                    where round_id = %s;
                    """
            cur = conn.cursor()
            cur.execute(sql, [round.tournament.tournament_id, round.get_round_no(), round.round_id])
            match_dao = MatchDAO()
            for match in round.matches:
                match_dao.update_match(match)

            conn.commit()
            cur.close()
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                self.__connection_provider.free_connection(conn)


__identity_map = {}
__lock = threading.Lock()


def initialize_map():
    global __lock
    global __identity_map
    __lock.acquire()
    try:
        __identity_map[Match] = {}
        __identity_map[Player] = {}
        __identity_map[PlayerParams] = {}
        __identity_map[Round] = {}
        __identity_map[Tournament] = {}
    finally:
        __lock.release()


def get_object(id_, type_):
    global __lock
    global __identity_map
    __lock.acquire()
    try:
        obj =  __identity_map[type_][id_]
        return obj
    except KeyError:
        return None
    finally:
        __lock.release()


def set_object(obj, id_, type_=None):
    global __lock
    global __identity_map
    __lock.acquire()
    if type_ is None:
        type_ = type(obj)
    try:
        __identity_map[type_][id_] = obj
    finally:
        __lock.release()


initialize_map()

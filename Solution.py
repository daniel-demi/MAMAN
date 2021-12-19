from typing import List
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Match import Match
from Business.Player import Player
from Business.Stadium import Stadium
from psycopg2 import sql


def createTables() -> None:
    conn = None
    create_teams_table = 'CREATE TABLE Teams(' \
                         'id INTEGER PRIMARY KEY CHECK(id > 0)' \
                         ')'

    create_matches_table = 'CREATE TABLE Matches(' \
                           'id INTEGER PRIMARY KEY CHECK(id > 0),' \
                           'competition VARCHAR(15) NOT NULL '  \
                           "CHECK(competition = 'International' or competition = 'Domestic')," \
                           'home_team_id INTEGER NOT NULL CHECK(home_team_id > 0), ' \
                           'away_team_id INTEGER NOT NULL CHECK(away_team_id > 0)' \
                           'CHECK(home_team_id <> away_team_id), ' \
                           'FOREIGN KEY (home_team_id) REFERENCES Teams(id) ON DELETE CASCADE, ' \
                           'FOREIGN KEY (away_team_id) REFERENCES Teams(id) ON DELETE CASCADE' \
                           ')'

    create_players_table = 'CREATE TABLE Players(' \
                           'id INTEGER PRIMARY KEY CHECK(id > 0),' \
                           'team_id INTEGER NOT NULL CHECK(team_id > 0),' \
                           'age INTEGER NOT NULL CHECK(age > 0),' \
                           'height INTEGER NOT NULL CHECK(height > 0),' \
                           'preferred_foot VARCHAR(10) NOT NULL ' \
                           "CHECK(preferred_foot = 'Left' or preferred_foot = 'Right'), " \
                           'FOREIGN KEY (team_id) REFERENCES Teams(id) ON DELETE CASCADE' \
                           ')'

    create_stadium_table = 'CREATE TABLE Stadium(' \
                           'id INTEGER PRIMARY KEY CHECK(id > 0),' \
                           'capacity INTEGER NOT NULL CHECK(capacity > 0),' \
                           'belong_to INTEGER,' \
                           'FOREIGN KEY (belong_to) REFERENCES Teams(id) ON DELETE CASCADE, ' \
                           'UNIQUE(belong_to))'

    create_player_scored_match_table = 'CREATE TABLE player_scored(' \
                                       'match_id INTEGER NOT NULL CHECK(match_id > 0),' \
                                       'player_id INTEGER NOT NULL CHECK(player_id > 0),' \
                                       'amount INTEGER NOT NULL CHECK(amount > 0),' \
                                       'FOREIGN KEY (match_id) REFERENCES Matches(id) ON DELETE CASCADE, ' \
                                       'FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE, ' \
                                       'PRIMARY KEY (match_id, player_id)' \
                                       ')'

    create_match_in_stadium_table = 'CREATE TABLE match_in_stadium(' \
                                    'match_id INTEGER PRIMARY KEY CHECK(match_id > 0), ' \
                                    'stadium_id INTEGER NOT NULL CHECK(stadium_id > 0), ' \
                                    'attendance INTEGER NOT NULL CHECK(attendance >= 0), ' \
                                    'FOREIGN KEY (match_id) REFERENCES Matches(id) ON DELETE CASCADE, ' \
                                    'FOREIGN KEY (stadium_id) REFERENCES Stadium(id) ON DELETE CASCADE ' \
                                    ')'

    create_active_teams_view = 'CREATE VIEW active_teams_view AS ' \
                               'SELECT home_team_id team_id FROM Matches ' \
                               'UNION DISTINCT ' \
                               'SELECT away_team_id team_id FROM Matches'

    create_rich_teams_view = 'CREATE VIEW rich_teams_view AS ' \
                            'SELECT DISTINCT belong_to team_id ' \
                            'FROM Stadium ' \
                            'WHERE capacity > 55000 '
    try:
        conn = Connector.DBConnector()
        conn.execute(create_teams_table)
        conn.execute(create_matches_table)
        conn.execute(create_players_table)
        conn.execute(create_stadium_table)
        conn.execute(create_player_scored_match_table)
        conn.execute(create_match_in_stadium_table)
        conn.execute(create_active_teams_view)
        conn.execute(create_rich_teams_view)
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()


def clearTables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute('DELETE FROM player_scored;')
        conn.execute('DELETE FROM match_in_stadium;')
        conn.execute('DELETE FROM Matches;')
        conn.execute('DELETE FROM Players;')
        conn.execute('DELETE FROM Stadium;')
        conn.execute('DELETE FROM Teams;')
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()


def dropTables() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute('DROP TABLE player_scored;')
        conn.execute('DROP TABLE match_in_stadium;')
        conn.execute('DROP VIEW active_teams_view;')
        conn.execute('DROP VIEW rich_teams_view;')
        conn.execute('DROP TABLE Matches;')
        conn.execute('DROP TABLE Players;')
        conn.execute('DROP TABLE Stadium;')
        conn.execute('DROP TABLE Teams;')
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()


def addTeam(teamID: int) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Teams(id) VALUES({id});").format(id=sql.Literal(teamID))
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def addMatch(match: Match) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO Matches(id, competition, home_team_id, away_team_id) "
            "VALUES({id}, {competition}, {homeId}, {awayId});"
        ).format(id=sql.Literal(match.getMatchID()), competition=sql.Literal(match.getCompetition()),
                 homeId=sql.Literal(match.getHomeTeamID()), awayId=sql.Literal(match.getAwayTeamID()))
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def getMatchProfile(matchID: int) -> Match:
    ret = Match.badMatch()
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Matches WHERE id={matchID};").format(matchID=sql.Literal(matchID))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            ret = Match.resultSetToMatch(result)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret


def deleteMatch(match: Match) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Matches WHERE id={matchID};").format(matchID=sql.Literal(match.getMatchID()))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            ret = ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def addPlayer(player: Player) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO Players(id, team_id, age, height, preferred_foot) "
            "VALUES({id}, {teamID}, {age}, {height}, {foot});"
        ).format(
            id=sql.Literal(player.getPlayerID()), teamID=sql.Literal(player.getTeamID()),
            age=sql.Literal(player.getAge()), height=sql.Literal(player.getHeight()), foot=sql.Literal(player.getFoot())
        )
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def getPlayerProfile(playerID: int) -> Player:
    ret = Player.badPlayer()
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Players WHERE id={playerID};").format(playerID=sql.Literal(playerID))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            ret = Player.resultSetToPlayer(result)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret


def deletePlayer(player: Player) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Players WHERE id={playerID};").format(playerID=sql.Literal(player.getPlayerID()))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            ret = ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def addStadium(stadium: Stadium) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO Stadium(id, capacity, belong_to) VALUES({id}, {capacity}, {belongsTo});"
        ).format(id=sql.Literal(stadium.getStadiumID()), capacity=sql.Literal(stadium.getCapacity()),
                 belongsTo=sql.Literal(stadium.getBelongsTo()))
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def getStadiumProfile(stadiumID: int) -> Stadium:
    ret = Stadium.badStadium()
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Stadium WHERE id={stadiumID};").format(stadiumID=sql.Literal(stadiumID))
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            ret = Stadium.resultSetToStadium(result)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret


def deleteStadium(stadium: Stadium) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Stadium WHERE id={id};").format(id=sql.Literal(stadium.getStadiumID()))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            ret = ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def playerScoredInMatch(match: Match, player: Player, amount: int) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO player_scored(match_id, player_id, amount) "
            "VALUES({match_id}, {player_id}, {amount});"
        ).format(
            match_id=sql.Literal(match.getMatchID()), player_id=sql.Literal(player.getPlayerID()),
            amount=sql.Literal(amount)
        )
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.NOT_EXISTS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def playerDidntScoreInMatch(match: Match, player: Player) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM player_scored WHERE match_id = {matchId} And player_id = {playerId};"
        ).format(
            matchId=sql.Literal(match.getMatchID()), playerId=sql.Literal(player.getPlayerID())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            ret = ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.NOT_EXISTS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def matchInStadium(match: Match, stadium: Stadium, attendance: int) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO match_in_stadium(match_id, stadium_id, attendance) "
            "VALUES({matchId}, {stadiumId}, {attendance});"
        ).format(
            matchId=sql.Literal(match.getMatchID()), stadiumId=sql.Literal(stadium.getStadiumID()),
            attendance=sql.Literal(attendance)
        )
        rows_effected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.NOT_EXISTS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def matchNotInStadium(match: Match, stadium: Stadium) -> ReturnValue:
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM match_in_stadium WHERE match_id = {matchId} And stadium_id = {stadiumId};"
        ).format(
            matchId=sql.Literal(match.getMatchID()), stadiumId=sql.Literal(stadium.getStadiumID())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            ret = ReturnValue.NOT_EXISTS

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = ReturnValue.NOT_EXISTS
    except Exception as e:
        #print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def averageAttendanceInStadium(stadiumID: int) -> float:
    ret = 0
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT AVG(attendance) FROM match_in_stadium WHERE stadium_id = {stadiumID}"
        ).format(stadiumID=sql.Literal(stadiumID))
        rows_effected, result = conn.execute(query)
        if result.rows[0][0]:
            ret = result.rows[0][0]
        else:
            ret = 0
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = -1
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = -1
    except Exception as e:
        #print(e)
        ret = -1
    finally:
        conn.close()
        return ret


def stadiumTotalGoals(stadiumID: int) -> int:
    ret = 0
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT SUM(amount) "
            "FROM match_in_stadium "
            "LEFT JOIN player_scored ON match_in_stadium.match_id = player_scored.match_id "
            "WHERE match_in_stadium.stadium_id = {stadiumID}"
        ).format(stadiumID=sql.Literal(stadiumID))
        rows_effected, result = conn.execute(query)
        if result.rows[0][0]:
            ret = result.rows[0][0]
        else:
            ret = 0
    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = -1
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = -1
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = -1
    except Exception as e:
        #print(e)
        ret = -1
    finally:
        conn.close()
        return ret


def playerIsWinner(playerID: int, matchID: int) -> bool:
    ret = False
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT SUM(amount) >=  "
            "(cast((SELECT SUM(amount) FROM player_scored WHERE match_id = {matchID}) as decimal) / 2)"
            "FROM player_scored "
            "WHERE match_id = {matchID} AND player_id = {playerID}"
        ).format(playerID=sql.Literal(playerID), matchID=sql.Literal(matchID))
        rows_effected, result = conn.execute(query)
        if result.rows[0][0]:
            ret = result.rows[0][0]

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = False
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = False
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = False
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = False
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = False
    except Exception as e:
        #print(e)
        ret = False
    finally:
        conn.close()
        return ret


def getActiveTallTeams() -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT team_id "
            "FROM Players "
            "WHERE height >= 190 AND team_id IN (SELECT * FROM active_teams_view) "
            "GROUP BY team_id "
            "HAVING COUNT(height) >= 2 "
            "ORDER BY team_id DESC "
            "LIMIT 5"
        )
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = []
    except Exception as e:
        #print(e)
        ret = []
    finally:
        conn.close()
        return ret


def getActiveTallRichTeams() -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT team_id "
            "FROM Players "
            "WHERE height >= 190 AND team_id IN (SELECT * FROM active_teams_view) "
            "AND team_id IN (SELECT * FROM rich_teams_view)"
            "GROUP BY team_id "
            "HAVING COUNT(height) >= 2 "
            "ORDER BY team_id "
            "LIMIT 5"
        )
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = []
    except Exception as e:
        #print(e)
        ret = []
    finally:
        conn.close()
        return ret


def popularTeams() -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            'SELECT home_team_id id '
            'FROM Matches M '
            'LEFT JOIN match_in_stadium ON match_in_stadium.match_id = M.id '
            'WHERE  40000 < ALL('
                'SELECT attendance '
                'FROM Matches M2 '
                'LEFT JOIN match_in_stadium ON match_in_stadium.match_id = M2.id '
                'WHERE M.home_team_id = M2.home_team_id'
            ') '
            'AND stadium_id IS NOT NULL '
            'UNION DISTINCT '
            'SELECT id '
            'FROM Teams '
            'WHERE id NOT IN ('
                'SELECT team_id '
                'FROM active_teams_view'
            ') '
            'UNION DISTINCT '
            'SELECT id '
            'FROM Teams T '
            'WHERE id IN ('
                'SELECT team_id '
                'FROM active_teams_view'
            ') '
            'AND ('
                'SELECT COUNT(home_team_id) '
                'FROM Matches '
                'WHERE home_team_id = T.id '
            ') = 0 '
            'ORDER BY id DESC '
            'LIMIT 10'
        )
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        #print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        #print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        #print(e)
        ret = []
    except Exception as e:
        #print(e)
        ret = []
    finally:
        conn.close()
        return ret


def getMostAttractiveStadiums() -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            'SELECT x.s_id '
            'FROM ('
                'SELECT id s_id, SUM(COALESCE (amount, 0)) total '
                'FROM Stadium '
                'LEFT JOIN match_in_stadium ON match_in_stadium.stadium_id = Stadium.id '
                'LEFT JOIN player_scored ON match_in_stadium.match_id = player_scored.match_id '
                'GROUP BY stadium_id, id '
                'ORDER BY total DESC, stadium_id, s_id'
            ') x'
        )
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        # print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        # print(e)
        ret = []
    except Exception as e:
        # print(e)
        ret = []
    finally:
        conn.close()
        return ret


def mostGoalsForTeam(teamID: int) -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            'SELECT x.p_id '
            'FROM ('
                'SELECT id p_id, SUM(COALESCE (amount, 0)) total '
                'FROM players '
                'LEFT JOIN player_scored ON players.id = player_scored.player_id '
                'WHERE team_id = {teamID} '
                'GROUP BY player_id, id '
                'ORDER BY total DESC , player_id DESC, id DESC '
                'LIMIT 5'
            ') x'
        ).format(teamID=sql.Literal(teamID))
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        # print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        # print(e)
        ret = []
    except Exception as e:
        # print(e)
        ret = []
    finally:
        conn.close()
        return ret


def getClosePlayers(playerID: int) -> List[int]:
    ret = []
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            'SELECT id '
            'FROM ( '
                'SELECT COUNT(*) num , x.id id '
                'FROM ( '
                    'SELECT id, COALESCE(match_id,-1) match_id, COALESCE (amount,0) amount '
                    'FROM players P '
                    'LEFT JOIN player_scored ps ON P.id = ps.player_id'
                ') as x , ('
                    'SELECT id, COALESCE(match_id,-1) match_id, COALESCE (amount,0) amount '
                    'FROM players P '
                    'LEFT JOIN player_scored ps ON P.id = ps.player_id'
                ') as y '
            'WHERE (x.match_id = y.match_id OR  y.match_id = -1) '
                'AND x.id != y.id AND x.id != {playerID} AND y.id = {playerID} '
            'GROUP BY x.id '
            ') z '
            'WHERE z.num >= (SELECT COUNT(*) FROM player_scored WHERE player_id = {playerID})/2 '
            'ORDER BY id '
            'LIMIT 10'
            ).format(playerID=sql.Literal(playerID))
        rows_effected, result = conn.execute(query)
        if len(result.rows):
            for i in range(0, len(result.rows)):
                ret.append(result.rows[i][0])

    except DatabaseException.ConnectionInvalid as e:
        # print(e)
        ret = []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.CHECK_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.UNIQUE_VIOLATION as e:
        # print(e)
        ret = []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        # print(e)
        ret = []
    except Exception as e:
        # print(e)
        ret = []
    finally:
        conn.close()
        return ret

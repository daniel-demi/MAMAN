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
    try:
        conn = Connector.DBConnector()
        conn.execute(create_teams_table)
        conn.execute(create_matches_table)
        conn.execute(create_players_table)
        conn.execute(create_stadium_table)
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
        conn.execute('DELETE FROM Teams;')
        conn.execute('DELETE FROM Matches;')
        conn.execute('DELETE FROM Players;')
        conn.execute('DELETE FROM Stadium;')
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
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
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
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
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
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
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
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def getPlayerProfile(playerID: int) -> Player:
    ret = Match.badMatch()
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
    pass


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
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except Exception as e:
        print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def getStadiumProfile(stadiumID: int) -> Stadium:
    pass


def deleteStadium(stadium: Stadium) -> ReturnValue:
    pass


def playerScoredInMatch(match: Match, player: Player, amount: int) -> ReturnValue:
    pass


def playerDidntScoreInMatch(match: Match, player: Player) -> ReturnValue:
    pass


def matchInStadium(match: Match, stadium: Stadium, attendance: int) -> ReturnValue:
    pass


def matchNotInStadium(match: Match, stadium: Stadium) -> ReturnValue:
    pass


def averageAttendanceInStadium(stadiumID: int) -> float:
    pass


def stadiumTotalGoals(stadiumID: int) -> int:
    pass


def playerIsWinner(playerID: int, matchID: int) -> bool:
    pass


def getActiveTallTeams() -> List[int]:
    pass


def getActiveTallRichTeams() -> List[int]:
    pass


def popularTeams() -> List[int]:
    pass


def getMostAttractiveStadiums() -> List[int]:
    pass


def mostGoalsForTeam(teamID: int) -> List[int]:
    pass


def getClosePlayers(playerID: int) -> List[int]:
    pass

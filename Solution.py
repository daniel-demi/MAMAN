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
                         'id INTEGER PRIMARY KEY' \
                         ')'
    create_matches_table = 'CREATE TABLE Matches(' \
                           'id INTEGER PRIMARY KEY,' \
                           'competition TEXT VARCHAR(15) NOT NULL,' \
                           'home_team_id INTEGER NOT NULL, ' \
                           'away_team_id INTEGER NOT NULL, ' \
                           'UNIQUE(home_team_id, away_team_id)' \
                           ')'
    create_players_table = 'CREATE TABLE Players(' \
                           'id INTEGER PRIMARY KEY,' \
                           'team_id INTEGER NOT NULL,' \
                           'age INTEGER NOT NULL,' \
                           'height INTEGER NOT NULL,' \
                           'preferred_foot VARCHAR(10) NOT NULL' \
                           ')'
    create_stadium_table = 'CREATE TABLE Stadium(' \
                           'id INTEGER PRIMARY KEY,' \
                           'capacity INTEGER NOT NULL,' \
                           'belong_to INTEGER,' \
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
    if teamID <= 0:
        return ReturnValue.BAD_PARAMS
    ret = ReturnValue.OK
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(f"INSERT INTO Teams(id) VALUES({sql.Literal(teamID)});")
        rows_affected, _ = conn.execute(query)
    except DatabaseException.ConnectionInvalid as e:
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
        ret = ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
        ret = ReturnValue.ERROR
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
        ret = ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
        ret = ReturnValue.ERROR
    except Exception as e:
        print(e)
        ret = ReturnValue.ERROR
    finally:
        conn.close()
        return ret


def addMatch(match: Match) -> ReturnValue:
    pass


def getMatchProfile(matchID: int) -> Match:
    pass


def deleteMatch(match: Match) -> ReturnValue:
    pass


def addPlayer(player: Player) -> ReturnValue:
    pass


def getPlayerProfile(playerID: int) -> Player:
    pass


def deletePlayer(player: Player) -> ReturnValue:
    pass


def addStadium(stadium: Stadium) -> ReturnValue:
    pass


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

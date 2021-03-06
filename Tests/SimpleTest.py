import unittest
import Solution
from Utility.ReturnValue import ReturnValue
from Tests.abstractTest import AbstractTest
from Business.Match import Match
from Business.Stadium import Stadium
from Business.Player import Player

'''
    Simple test, create one of your own
    make sure the tests' names start with test_
'''


class Test(AbstractTest):
    def test_Team(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addTeam(1), "ID 1 already exists")
        # my tests
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addTeam(0), "Id Should be positive")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addTeam(None), "Id Should be positive")

    def test_Match(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(5), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(1, "Domestic", 1, 2)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(2, "Domestic", 1, 3)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(3, "Domestic", 1, 4)), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addMatch(Match(1, "Domestic", 1, 5)), "ID 1 already exists")
        # my tests
        self.assertEqual(ReturnValue.OK, Solution.addTeam(6), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(4, "Domesti", 1, 6)), "bad Competition")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(0, "Domestic", 1, 6)), "bad ID")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(5, "Domestic", 6, 6)), "home and away can not be the same id")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(None, "Domestic", 1, 6)), "All attributes are not optional")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(5, None, 1, 6)), "All attributes are not optional")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(5, "Domestic", None, 6)), "All attributes are not optional")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMatch(Match(5, "Domestic", 1, None)), "All attributes are not optional")

    def test_Player(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(Player(1, 1, 20, 185, "Left")), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(Player(2, 1, 20, 185, "Left")), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(Player(3, 1, 20, 185, "Left")), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addPlayer(Player(1, 1, 20, 185, "Left")), "ID 1 already exists")
        # my tests
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPlayer(Player(4, 2, 20, 185, "Left")), "Team don't exists")

    def test_Stadium(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(1, "Domestic", 1, 2)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(Stadium(1, 55000, 1)), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addStadium(Stadium(1, 5000, 1)), "ID 1 already exists")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addStadium(Stadium(2, 5000, 3)), "teamID 3 not exists")
        # my tests
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addStadium(Stadium(2, 5000, 1)), "Team 1 already owns a stadium")

    def test_getMatchProfile(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(1, "Domestic", 1, 2)), "Should work")
        s = Solution.getMatchProfile(1)
        self.assertIsInstance(s, Match)
        self.assertEqual(1, s.getMatchID(), "Should work")

    def test_deleteMatch(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        m = Match(1, "Domestic", 1, 2)
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteMatch(m), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteMatch(m), "Match should not exist")

    def test_getStadiumProfile(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(Stadium(1, 500, 1)), "Should work")
        s = Solution.getStadiumProfile(1)
        self.assertIsInstance(s, Stadium)
        self.assertEqual(1, s.getStadiumID(), "Should work")

    def test_getPlayerProfile(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(Player(1, 1, 20, 185, "Left")), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPlayer(Player(100, 1, 10, 150, "Both")), "Should work")
        s = Solution.getPlayerProfile(1)
        s2 = Solution.getPlayerProfile(100)
        self.assertIsInstance(s, Player)
        self.assertEqual(1, s.getPlayerID(), "Should work")

    def test_deletePlayer(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        p = Player(1, 1, 20, 185, "Left")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePlayer(p), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deletePlayer(p), "Player should not exist")

    def test_deleteStadium(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        s = Stadium(1, 55000, 1)
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteStadium(s), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteStadium(s), "Stadium should not exist")

    def test_playerScoredInMatch(self) -> None:
        m = Match(1, "Domestic", 1, 2)
        p = Player(1, 1, 20, 185, "Left")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.playerScoredInMatch(m, p, 1), "player/match does not exist")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.playerScoredInMatch(m, p, 0), "amount is not positive")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.playerScoredInMatch(m, p, 2), "player already scored in this match")

    def test_playerDidntScoreInMatch(self) -> None:
        m = Match(1, "Domestic", 1, 2)
        p = Player(1, 1, 20, 185, "Left")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.playerDidntScoreInMatch(m, p), "player/match does not exist")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.playerDidntScoreInMatch(m, p), "match does not exist")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.playerDidntScoreInMatch(m, p), "player did not already score in match")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerDidntScoreInMatch(m, p), "Should work")

    def test_matchInStadium(self) -> None:
        m = Match(1, "Domestic", 1, 2)
        s = Stadium(1, 55000, 1)
        s2 = Stadium(2, 55000, 2)
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.matchInStadium(m, s, 500), "Stadium/match does not exist")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.matchInStadium(m, s, -500), "amount is negative")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 500), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.matchInStadium(m, s2, 500), "match already taking place in any stadium")

    def test_matchNotInStadium(self) -> None:
        m = Match(1, "Domestic", 1, 2)
        s = Stadium(1, 55000, 1)
        s2 = Stadium(2, 55000, 2)
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 500), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.matchNotInStadium(m, s2), "match not in s2")
        self.assertEqual(ReturnValue.OK, Solution.matchNotInStadium(m, s), "Should work")

    def test_averageAttendanceInStadium(self) -> None:
        self.assertEqual(0, Solution.averageAttendanceInStadium(1), "stadiumID does not exist")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "International", 2, 1)
        s = Stadium(1, 55000, 1)
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 100), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m2, s, 100), "Should work")
        self.assertEqual(100, Solution.averageAttendanceInStadium(1), "Should work")

    def test_stadiumTotalGoals(self) -> None:
        self.assertEqual(0, Solution.stadiumTotalGoals(1), "stadiumID does not exist")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "International", 2, 1)
        s = Stadium(1, 55000, 1)
        p = Player(1, 1, 20, 185, "Left")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p, 3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 500), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m2, s, 500), "Should work")
        self.assertEqual(5, Solution.stadiumTotalGoals(1), "Should work")

    def test_playerIsWinner(self) -> None:
        self.assertEqual(0, Solution.playerIsWinner(1, 1), "player does not exist")
        p = Player(1, 1, 20, 185, "Left")
        p2 = Player(2, 2, 20, 185, "Left")
        m = Match(1, "Domestic", 1, 2)
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 3), "Should work")
        self.assertEqual(False, Solution.playerIsWinner(1, 1), "Should work")
        self.assertEqual(True, Solution.playerIsWinner(2, 1), "Should work")

    def test_getActiveTallTeams(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(4), "Should work")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 2, 3)
        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 2, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 2, 20, 190, "Left")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual([2, 1], Solution.getActiveTallTeams(), "Should work")

    def test_getActiveTallRichTeams(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(4), "Should work")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 2, 3)
        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 2, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 2, 20, 190, "Left")
        s = Stadium(1, 65000, 1)
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual([1], Solution.getActiveTallRichTeams(), "Should work")

    def test_popularTeams(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(4), "Should work")

        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 2, 3)
        m3 = Match(3, "Domestic", 2, 1)
        s = Stadium(1, 65000, 1)
        s2 = Stadium(2, 65000, 2)

        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m2, s2, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m3, s2, 35000), "Should work")
        self.assertEqual([4, 3, 1], Solution.popularTeams(), "Should work")

    def test_getMostAttractiveStadiums(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")

        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 2, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 3, 20, 190, "Left")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 3, 2)
        m3 = Match(3, "Domestic", 2, 1)
        s = Stadium(1, 65000, 1)
        s2 = Stadium(2, 65000, 2)
        s3 = Stadium(3, 65000, 3)

        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m3), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p2, 4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p2, 3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p3, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p3, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p3, 1), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s3), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m2, s3, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m3, s2, 35000), "Should work")
        self.assertEqual([2, 1, 3], Solution.getMostAttractiveStadiums(), "Should work")

    def test_getMostAttractiveStadiums2(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(4), "Should work")

        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 2, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 3, 20, 190, "Left")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 3, 2)
        m3 = Match(3, "Domestic", 2, 1)
        s = Stadium(1, 65000, 1)
        s2 = Stadium(2, 65000, 2)
        s3 = Stadium(3, 65000, 3)
        s4 = Stadium(4, 65000, 4)

        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m3), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p2, 4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p2, 3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p3, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p3, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p3, 1), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.addStadium(s), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addStadium(s4), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m, s, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m2, s3, 45000), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.matchInStadium(m3, s2, 35000), "Should work")
        self.assertEqual([2, 1, 3, 4], Solution.getMostAttractiveStadiums(), "Should work")

    def test_mostGoalsForTeam(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")

        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 1, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 1, 20, 190, "Left")
        p5 = Player(5, 1, 20, 190, "Left")
        p6 = Player(6, 1, 20, 190, "Left")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(3, "Domestic", 2, 1)
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p5), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p6), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p3, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p4, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p5, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p6, 3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p2, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p3, 1), "Should work")
        self.assertEqual([2, 6, 1, 3, 5], Solution.mostGoalsForTeam(1), "Should work")

    def test_mostGoalsForTeam2(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")

        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 1, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 1, 20, 190, "Left")
        p5 = Player(5, 1, 20, 190, "Left")
        p6 = Player(6, 1, 20, 190, "Left")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(3, "Domestic", 2, 1)
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p5), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p6), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p3, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p2, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p3, 1), "Should work")
        self.assertEqual([2, 1, 3, 6, 5], Solution.mostGoalsForTeam(1), "Should work")

    def test_getClosePlayers(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addTeam(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addTeam(3), "Should work")

        p = Player(1, 1, 20, 195, "Left")
        p2 = Player(2, 2, 20, 190, "Left")
        p3 = Player(3, 1, 20, 190, "Left")
        p4 = Player(4, 3, 20, 190, "Left")
        m = Match(1, "Domestic", 1, 2)
        m2 = Match(2, "Domestic", 3, 2)
        m3 = Match(3, "Domestic", 2, 1)

        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPlayer(p4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addMatch(m3), "Should work")

        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p2, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p2, 4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p2, 3), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m, p3, 2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m3, p3, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.playerScoredInMatch(m2, p3, 1), "Should work")
        self.assertEqual([2, 3], Solution.getClosePlayers(1), "should work")


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)

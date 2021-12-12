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
        self.assertEqual(ReturnValue.OK, Solution.addMatch(Match(1, "Domestic", 1, 2)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteMatch(Match(1, "Domestic", 1, 2)), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteMatch(Match(1, "Domestic", 1, 2)), "Match should not exist")


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
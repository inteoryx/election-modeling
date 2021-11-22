from election import Election
import unittest

from voter import Voter

class TestElection(unittest.TestCase):

    def test_constructor(self):
        e = Election(10, 100)
        self.assertEqual(len(e.candidates), 10)
        self.assertEqual(len(e.voters), 100)

    def test_vote(self):
        e = Election(1, 100)
        num_issues = len(e.candidates[0].preferences)
        candidates = [
            Voter(preferences=[[0, 0] for i in range(num_issues)]),
            Voter(preferences=[[-5000, 0] for i in range(num_issues)]),
        ]

        e.set_candidates(candidates)

        self.assertEqual(e.vote(), candidates[0])
        candidates.append(candidates.pop(0))
        self.assertEqual(e.vote(), candidates[1])

    def test_rank(self):
        e = Election(1, 100)
        num_issues = len(e.candidates[0].preferences)
        candidates = [
            Voter(preferences=[[0, 0] for i in range(num_issues)]),
            Voter(preferences=[[-5000, 0] for i in range(num_issues)]),
        ]

        e.set_candidates(candidates)

        self.assertEqual(e.ranked_choice(), candidates[0])
        candidates.append(candidates.pop(0))
        self.assertEqual(e.ranked_choice(), candidates[1])

    def test_approval(self):
        e = Election(1, 100)
        num_issues = len(e.candidates[0].preferences)
        candidates = [
            Voter(preferences=[[i, 0] for i in range(num_issues)]),
            Voter(preferences=[[-5 - i * 10000, 0] for i in range(num_issues)]),
        ]

        voters = [Voter(preferences=[[i, 1] for i in range(num_issues)]) for _ in range(100)]

        e.set_candidates(candidates)
        e.set_voters(voters)

        self.assertEqual(e.approval(), candidates[0])
        candidates.append(candidates.pop(0))
        self.assertEqual(e.approval(), candidates[1])

if __name__ == '__main__':
    unittest.main()
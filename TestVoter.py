import unittest
from voter import Voter

class TestVoter(unittest.TestCase):

    # Test the constructor
    def test_constructor(self):
        v = Voter(number_of_issues=10)
        self.assertEqual(len(v.preferences), 10)


    # Test the candidate_distance function
    def test_candidate_distance(self):
        v = Voter(number_of_issues=10)

        same_candidate = Voter(preferences=v.preferences)
        self.assertEqual(v.candidate_distance(same_candidate), 0)

        different_candidate = Voter(preferences=v.preferences)
        different_candidate.preferences[0][0] += 1

        # Candidate distance should be the magnitude of the first preference.
        self.assertAlmostEquals(v.candidate_distance(different_candidate), different_candidate.preferences[0][1])

    def test_vote(self):
        v = Voter()
        same_candidate = Voter(preferences=v.preferences)

        candidates = [Voter() for i in range(10)] + [same_candidate]
        self.assertEqual(v.vote(candidates), len(candidates) - 1)

        different_candidate = Voter(preferences=v.preferences)
        different_candidate.preferences[0][0] += 1
        candidates = [Voter() for i in range(10)] + [different_candidate]
        self.assertEqual(v.vote(candidates), len(candidates) - 1)

    def test_rank(self):
        v = Voter(preferences=[[1,1] for i in range(10)])
        candidates = [Voter(preferences=v.preferences) for i in range(10)]
        
        for i, candidate in enumerate(candidates):
            candidate.preferences[0][0] += i

        # Test that the candidates are ranked in index order
        self.assertEqual(v.rank(candidates), list(candidates))

        # Enumerate over the candidates in reverse
        for i, candidate in enumerate(candidates[::-1]):
            candidate.preferences[0][0] += i * 5

        # Test that the candidates are now in reverse index order
        self.assertEqual(v.rank(candidates), list(reversed((candidates))))

    def test_approval(self):
        v = Voter(approval_threshold=1000)

        self.assertEqual(v.approval_threshold, 1000)

        candidates = [Voter(preferences=v.preferences) for i in range(10)]
        self.assertEqual(len(v.approval(candidates)), len(candidates))

        candidates[0].preferences[0][0] += 1001
        v.preferences[0][1] = 1
        v.preferences[0][0] = 0
        self.assertEqual(len(v.approval(candidates)), len(candidates) - 1)

if __name__ == '__main__':
    unittest.main()
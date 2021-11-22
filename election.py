from voter import Voter
import random

class Election:
    def __init__(self, candidates, voters):
        self.candidates = [Voter() for _ in range(candidates)]
        self.voters = [Voter() for _ in range(voters)]

    def set_candidates(self, candidates):
        self.candidates = candidates

    def set_voters(self, voters):
        self.voters = voters

    def election_quality(self, winner):
        return sum([v.candidate_distance(winner) for v in self.voters])

    def vote(self):
        tally = {i: 0 for i in range(len(self.candidates))}

        for v in self.voters:
            tally[v.vote(self.candidates)] += 1

        tally_items = list(tally.items())
        tally_items.sort(key=lambda x: x[1], reverse=True)
        return self.candidates[tally_items[0][0]]

    def approval(self):
        tally = {candidate: 0 for candidate in self.candidates}

        for v in self.voters:
            for c in v.approval(self.candidates):
                tally[c] += 1

        tally_items = list(tally.items())
        tally_items.sort(key=lambda x: x[1], reverse=True)
        return tally_items[0][0]

    def ranked_choice(self):
        remaining = set(self.candidates)

        while len(remaining) > 1:
            votes = {r: 0 for r in remaining}

            for v in self.voters:
                votes[v.rank(remaining)[0]] += 1

            min_val, min_key = max(votes.values()), None
            for k, v in votes.items():
                if v <= min_val:
                    min_val, min_key = v, k

            remaining.remove(min_key)

        return remaining.pop()

    def random(self):
        return random.choice(self.candidates)

def test(trials, candidates, voters):
    """
    Create an election with the given number of candidates and voters.
    Run the election for the given number of trials.
    Return the average election quality of vote, approval, ranked choice, and random vote
    """

    e = Election(candidates, voters)

    results = {
        e.vote: 0,
        e.approval: 0,
        e.ranked_choice: 0,
        e.random: 0,
    }

    for _ in range(trials):
        run = normalize([e.election_quality(m()) for m in results.keys()])
        for i, m in enumerate(results):
            results[m] += run[i]
        
        
    return list(sorted({k.__name__: v / trials for k, v in results.items()}.items(), key=lambda x: x[1]))


def normalize(values):
    smallest = min(values)
    largest = max(values)
    if smallest == largest:
        return [1] * len(values)
    return [((v - smallest) / (largest - smallest)) for v in values]

if __name__ == '__main__':
    print(test(100, 25, 1000))
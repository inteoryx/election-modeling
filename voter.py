import numpy as np
import matplotlib.pyplot as plt
from uuid import uuid4

class Voter:
    """
    This class is intended to represent a voter in an election.

    A voter has a list of preferences.  Each preference has a location and a magnitude.  The location
    is a number that represents the voter's "position" on some issue while the magnitude is a number
    representing how much this voter cares about that issue.  For example, if we imagine that one 
    issue was 'how tough should police be on crime' a voter with a 0 might be an anarchist who doesn't 
    want police to stop criminals at all while 100 might be a fascist who wants the police to shoot
    dead literers and jaywalkers.

    """


    def __init__(self, number_of_issues=100, preferences=None, approval_threshold=None) -> None:
        if preferences is None:
            self.preferences = list(list(x) for x in np.random.normal(50, scale=50, size=[number_of_issues, 2]))
        else:
            self.preferences = list(list(x) for x in preferences)

        # Normalize the preferences
        prefs = [p[0] for p in self.preferences]
        mags  = [p[1] for p in self.preferences]

        max_p = max(prefs)
        min_p = min(prefs)
        max_m = max(mags)
        min_m = min(mags)
        
        for i in range(len(prefs)):

            # Some tests use identical preferences - this is a hack to prevent division by zero
            if max_p != min_p and max_m != min_m:
                prefs[i] = (prefs[i] - min_p) / (max_p - min_p)
                mags[i] = (mags[i] - min_m) / (max_m - min_m)

        self.preferences = list([p, m] for p, m in zip(prefs, mags))
        
        if approval_threshold is None:
            # Set approval threshold to a random number between 0 and 100
            self.approval_threshold = np.random.randint(0, len(self.preferences))
        else:
            self.approval_threshold = approval_threshold

        self.id = str(uuid4())

    def __hash__(self) -> int:
        return hash(self.id)


    def __eq__(self, __o: object) -> bool:
        """
        This function will return True if the given object is a Voter and has the same preferences as this voter.
        """
        if type(__o) is Voter:
            if len(self.preferences) != len(__o.preferences):
                return False

            for p in range(len(self.preferences)):
                if self.preferences[p] != __o.preferences[p]:
                    return False

            return True
        else:
            return False

    def __str__(self) -> str:
        """
        This function will return a string representation of the voter.
        """
        return "Voter: " + str(self.preferences) + " Approval Threshold: " + str(self.approval_threshold)
        return False
        

    def graph_prefs(self, fname):
        """
        This function will create a bar graph of the voter's preferences and save to a file.
        """

        plt.figure(figsize=(10,10))
        plt.title('Voter Preferences')
        plt.legend(['Location', 'Magnitude'])

        plt.bar([2 * x - 0.25 for x in range(len(self.preferences))], [x[0] for x in self.preferences], width=0.5, color='b', align='center')
        plt.bar([2 * x + 0.25 for x in range(len(self.preferences))], [x[1] for x in self.preferences], width=0.5, color='r', align='center')
        plt.savefig(fname)
        plt.close()


    def candidate_distance(self, candidate):
        """
        This function will return the distance between the voter and a candidate.  The distance
        is the sum of the absolute differences between the voter's preference location and the candidate's
        multiplied by the voter's preference magnitude.
        """
        result = 0

        for i in range(len(self.preferences)):
            result += abs(self.preferences[i][0] - candidate.preferences[i][0]) * self.preferences[i][1]

        return result


    def vote(self, candidates):
        """
        This function will return the index of the candidate with the lowest distance from the voter.
        """
        distances = [self.candidate_distance(candidate) for candidate in candidates]
        return distances.index(min(distances))
        
    
    def rank(self, candidates):
        """
        Return a list of candidate indicies sorted by their distance from the voter.
        """
        distances = [(candidate, self.candidate_distance(candidate)) for i, candidate in enumerate(candidates)]
        distances.sort(key=lambda x: x[1])
        return [x[0] for x in distances]


    def approval(self, candidates):
        """
        Return a list of candidate indicies for all candidates that have a distance less than the approval threshold.
        """
        result = []
        for candidate in candidates:
            distance = self.candidate_distance(candidate)
            if distance <= self.approval_threshold:
                result.append(candidate)

        return result

    def modify(self, index, location=None, magnitude=None):
        """
        This function will modify the voter's preference at the given index to have the given location and magnitude.
        """
        self.preferences[index] = [
            location if location else self.preferences[index][0], 
            magnitude if magnitude else self.preferences[index][1]
        ]


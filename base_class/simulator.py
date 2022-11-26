import numpy as np
from numpy.random import choice

from configs import DEFAULT_PROBA

class MatchMaker:
    @classmethod
    def set_random_state(cls, seed=1212):
        np.random.seed(seed)

    @classmethod
    def predict_one_result(cls, match_prob):
        return cls.predict_one_result_by_dict_dist(match_prob.p1_score_dist, match_prob.p2_score_dist)

    @classmethod
    def predict_one_result_by_dict_dist(cls, dict_score1, dict_score2):
        p1_score = choice(np.array(dict_score1.keys()), 1, np.array(dict_score1.values()))
        p2_score = choice(dict_score2.keys(), 1, dict_score2.values())
        return p1_score, p2_score

class MatchProbability:

    def __init__(self, p1, p2, p1_score_prob_dist, p2_score_prob_dist):
        self.p1 = p1
        self.p2 = p2
        self.p1_score_dist = p1_score_prob_dist
        self.p2_score_dist = p2_score_prob_dist


class WorldCupSimulator:

    def __init__(self, participants, default_proba=DEFAULT_PROBA):
        matches = dict()
        for i, p1 in enumerate(participants):
            for j, p2 in enumerate(participants):
                if j >= i:
                    break

                matches[f"{p1}__{p2}"] = MatchProbability(p1, p2, default_proba, default_proba)
        self.matches = matches

    def update_prob(self, p1, p2, proba1, proba2):
        self.matches[f"{p1}__{p2}"] = MatchProbability(p1, p2, proba1, proba2)


if __name__ == "__main__":
    for i in range(10):
        print(i, MatchMaker.predict_one_result_by_dict_dist(DEFAULT_PROBA, DEFAULT_PROBA))
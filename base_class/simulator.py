import numpy as np
from numpy.random import choice

from configs import DEFAULT_PROBA
from participant import WorldCupParticipants
from match import WorldCupMatchManager


class MatchPredictor:
    @classmethod
    def set_random_state(cls, seed=1212):
        np.random.seed(seed)

    @classmethod
    def predict_one_result(cls, match_prob):
        return cls.predict_one_result_by_dict_dist(match_prob.p1_score_dist, match_prob.p2_score_dist)

    @classmethod
    def predict_one_result_by_dict_dist(cls, dict_score1, dict_score2):
        p1_score = choice(list(dict_score1.keys()), 1, p=list(dict_score1.values()))
        p2_score = choice(list(dict_score2.keys()), 1, p=list(dict_score2.values()))
        return p1_score[0], p2_score[0]


class MatchProbability:

    def __init__(self, p1_score_prob_dist, p2_score_prob_dist):
        self.p1_score_dist = p1_score_prob_dist
        self.p2_score_dist = p2_score_prob_dist


class WorldCupSimulator:
    """ 시뮬레이터는 참가팀의 풀 리그를 가정하고, 골 확률표를 이용해서 최종 순위테이블을 리턴합니다."""

    def __init__(self, participants, default_proba=DEFAULT_PROBA):
        self.participants = {x: WorldCupParticipants(x) for x in participants}
        matches = dict()
        for i, p1 in enumerate(self.participants):
            for j, p2 in enumerate(self.participants):
                if j >= i:
                    break

                matches[f"{p1}__{p2}"] = MatchProbability(default_proba, default_proba)
        self.matches = matches

    def update_prob(self, p1, p2, proba1, proba2):
        self.matches[f"{p1}__{p2}"] = MatchProbability(proba1, proba2)

    def run_single(self):

        for p in self.participants.values():
            p.reset()

        history = []
        for match_name, match_prob in self.matches.items():
            result = MatchPredictor.predict_one_result(match_prob)
            history.append({match_name: result})

            p1_name, p2_name = match_name.split("__")
            p1 = self.participants[p1_name]
            p2 = self.participants[p2_name]
            p1_score, p2_score = result
            WorldCupMatchManager.apply_result(p1=p1, p2=p2, p1_score=p1_score, p2_score=p2_score)

        return self.participants


if __name__ == "__main__":
    sample_answer = choice([0, 1, 2, 3], 1, p=[0.4, 0.6, 0.0, 0.0])
    print("sample answer:", sample_answer)

    for i in range(10):
        print(i, MatchPredictor.predict_one_result_by_dict_dist(DEFAULT_PROBA, DEFAULT_PROBA))

    teams = ['Korea', 'Portugal', 'Uruguay', 'Ghana',]
    simulator = WorldCupSimulator(teams)

    team_results = simulator.run_single()
    print(team_results)
    assert len(team_results) == len(teams)
    assert type(team_results['Korea']) == WorldCupParticipants
    assert sum([x.win for x in team_results.values()]) == sum([x.lose for x in team_results.values()])
    assert sum([x.tie for x in team_results.values()]) % 2 == 0
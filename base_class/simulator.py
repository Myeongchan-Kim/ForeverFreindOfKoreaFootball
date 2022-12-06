from collections import Counter

import numpy as np
from numpy.random import choice

from configs import DEFAULT_PROBA
from participant import WorldCupParticipants
from match import WorldCupMatchManager
from leaderboard import WordCupGroupStageLeaderBoard


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

    def __repr__(self):
        return f"p1:{self.p1_score_dist}, p2:{self.p2_score_dist}"


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

        assert self.matches.get(f"{p1}__{p2}", False) or self.matches.get(f"{p2}__{p1}",
                                                                          False), "No match information found"

        if self.matches.get(f"{p1}__{p2}", False):
            self.matches[f"{p1}__{p2}"] = MatchProbability(proba1, proba2)
        else:
            self.matches[f"{p2}__{p1}"] = MatchProbability(proba2, proba1)

    def simulate_single(self):

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

        return self.participants, history

    def simulate(self, group_name, n=1000):
        result = SimulationResult()
        for i in range(n):
            team_results, history = self.simulate_single()

            # 마지막 리더보드 추가
            leaderboard = WordCupGroupStageLeaderBoard(group_name, 2)
            leaderboard.add_participants(team_results.values())

            # 진출팀
            winners = leaderboard.get_passed_participants()
            winner_names = [x.name for x in winners[:2]]

            single_result = SimulationSingleResult(leaderboard.stats(), history, winner_names)
            result.append(single_result)

        return result


class SimulationResult:
    """시뮬레이션 결과를 담는 구조체입니다."""

    def __init__(self):
        self.win_counter = Counter()
        self.simulation_detail = []

    def append(self, single_result):
        self.simulation_detail.append(single_result)
        self.win_counter.update(single_result.winners)

    def __repr__(self):
        return str(self.win_counter)


class SimulationSingleResult:
    """시뮬레이션 한번 결과를 담는 구조체입니다."""

    def __init__(self, leaderboard_stats, match_history, winners):
        self.leaderboard = leaderboard_stats
        self.match_history = match_history
        self.winners = winners

    def __repr__(self):
        return str(self.leaderboard)


if __name__ == "__main__":
    sample_answer = choice([0, 1, 2, 3], 1, p=[0.4, 0.6, 0.0, 0.0])
    print("sample answer:", sample_answer)

    for i in range(10):
        print(i, MatchPredictor.predict_one_result_by_dict_dist(DEFAULT_PROBA, DEFAULT_PROBA))

    teams = ['Korea', 'Portugal', 'Uruguay', 'Ghana', ]
    simulator = WorldCupSimulator(teams)

    team_results, history = simulator.simulate_single()
    for name, p in team_results.items():
        print(p.stats())

    assert len(team_results) == len(teams)
    assert type(team_results['Korea']) == WorldCupParticipants
    assert sum([x.win for x in team_results.values()]) == sum([x.lose for x in team_results.values()])
    assert sum([x.tie for x in team_results.values()]) % 2 == 0

    print(history)
    assert len(history) == 6

    leaderboard = WordCupGroupStageLeaderBoard('Group H', 2)
    leaderboard.add_participants(team_results.values())
    passed = leaderboard.get_passed_participants()
    print(passed)

    mt_result = simulator.simulate("Goup H", 100)
    print("Round0 :", mt_result)

    simulator.update_prob("Korea", "Uruguay", {0: 1}, {0: 1})
    simulator.update_prob("Ghana", "Portugal", {2: 1}, {3: 1})
    mt_result = simulator.simulate("Goup H", 100)
    print("After Round1 :", mt_result)

    simulator.update_prob("Korea", "Ghana", {2: 1}, {3: 1})
    simulator.update_prob("Uruguay", "Portugal", {0: 1}, {2: 1})
    mt_result = simulator.simulate("Goup H", 1000)
    print("After Round2 :", mt_result)

    simulator.update_prob("Korea", "Portugal", {2: 1}, {1: 1})
    simulator.update_prob("Uruguay", "Ghana", {2: 1}, {0: 1})
    mt_result = simulator.simulate("Goup H", 100)
    print("After Round3 :", mt_result)

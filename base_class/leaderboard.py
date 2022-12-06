

class Leaderboard:
    def __init__(self, name, n_cutoff, key_func_for_sorting=None):
        """리그 순위를 관리하는 클래스 입니다.
        rule 은 순위를 정할때 사용하는 함수입니다. sorted 의 key 함수와 사용법이 같습니다.
        """
        self.name = name
        self.n_cutoff = n_cutoff
        self.key_func = key_func_for_sorting
        self.participants = []

    def add_participants(self, participants):
        """리스트로 된 참가팀들을 추가합니다. """
        self.participants += participants

    def append_participant(self, p):
        """단일 참가팀을 추가합니다."""
        self.participants.append(p)

    def get_sorted_list(self):
        return sorted(self.participants, key=self.key_func, reverse=True)

    def get_passed_participants(self):
        assert self.participants, "No participants added yet!"
        return self.get_sorted_list()[:self.n_cutoff]


class WordCupGroupStageLeaderBoard(Leaderboard):

    def get_sorted_list(self):
        score_func = lambda x: [x.win_score, x.goal_diff, x.gain_goal]
        participants = sorted(self.participants, key=score_func, reverse=True)
        if score_func(participants[2]) == score_func(participants[1]):  # 2위와 3위가 같은 경우에는 타이브레이크 룰 적용
            participants = self.__apply_tie_breaker(participants)
        return participants

    def stats(self):
        return {x.name: x.stats() for x in self.participants}

    @classmethod
    def __apply_tie_breaker(cls, participants):
        return participants


if __name__ == "__main__":

    ld = Leaderboard("숫자 리더보드", 2)
    ld.append_participant(1)
    ld.append_participant(2)
    ld.append_participant(9)
    ld.append_participant(10)
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [10, 9]

    ld.key_func = lambda x: -x
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [1, 2]

    ld.add_participants([-1, -2])
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [-2, -1]

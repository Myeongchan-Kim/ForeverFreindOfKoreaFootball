

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
        self.participants += participants

    def append_participant(self, p):
        self.participants.append(p)

    def get_sorted_list(self):
        return sorted(self.participants, key=self.key_func)

    def get_passed_participants(self):
        return self.get_sorted_list()[-self.n_cutoff:]


class TypeCheckingLeaderboard(Leaderboard):
    def __init__(self, name, n_cutoff, key_func_for_sorting, participants_class):
        super().__init__(name, n_cutoff, key_func_for_sorting)
        self.participants_class = participants_class

    def _is_valid_participants(self, p):
        return type(p) == self.participants_class


if __name__ == "__main__":

    ld = Leaderboard("숫자 리더보드", 2)
    ld.append_participant(1)
    ld.append_participant(2)
    ld.append_participant(9)
    ld.append_participant(10)
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [9, 10]

    ld.key_func = lambda x: -x
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [2, 1]

    ld.add_participants([-1, -2])
    print("passed: ", ld.get_passed_participants())
    assert ld.get_passed_participants() == [-1, -2]


class Participant:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class WorldCupParticipants(Participant):

    def __init__(self, name):
        super().__init__(name)
        self.win = None
        self.lose = None
        self.tie = None

        self.gain_goal = None
        self.lost_goal = None
        self.win_others = None
        self.reset()

    def reset(self):
        self.win = 0
        self.lose = 0
        self.tie = 0

        self.gain_goal = 0
        self.lost_goal = 0
        self.win_others = []

    @property
    def win_score(self):
        return self.win * 3 + self.tie * 1

    @property
    def goal_diff(self):
        return self.gain_goal - self.lost_goal

    def stats(self):
        return f"{self.name} {self.win}-{self.tie}-{self.lose} goaldiff:{self.goal_diff} {self.gain_goal}-{self.lost_goal}"

    def __gt__(self, other):
        return [self.win_score, self.goal_diff, self.gain_goal, True if other in self.win_others else False]

    def __repr__(self):
        return " ".join(self.stats().split(" ")[:2])


if __name__ == "__main__":
    mc_team = WorldCupParticipants("MC")
    kt_team = WorldCupParticipants('KT')
    mc_team.win = 1
    kt_team.win = 0
    assert mc_team > kt_team

    mc_team.win = 1
    kt_team.win = 1
    mc_team.gain_goal = 2
    kt_team.gain_goal = 1
    assert mc_team.goal_diff == 2
    assert kt_team.goal_diff == 1
    assert mc_team > kt_team

    mc_team.win = 0
    kt_team.win = 1
    assert mc_team < kt_team

    mc_team.win = 1
    kt_team.win = 1
    mc_team.lost_goal = 3
    kt_team.lost_goal = 2
    assert mc_team.goal_diff == -1
    assert kt_team.goal_diff == -1
    assert mc_team > kt_team

    mc_team.win = 1
    mc_team.win_others.append(kt_team)
    kt_team.win = 1
    assert kt_team in mc_team.win_others
    assert mc_team > kt_team

    kt_team.reset()
    assert kt_team.win == 0
    assert mc_team > kt_team

    assert mc_team.stats() == "MC 1-0-0 goaldiff:-1 2-3", mc_team.stats() + " looks wrong"
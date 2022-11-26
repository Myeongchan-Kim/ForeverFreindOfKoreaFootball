
class Participant:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class WorldCupParticipants(Participant):

    def __init__(self, name):
        super().__init__(name)

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

    def __gt__(self, other):
        return [self.win_score, self.goal_diff, self.gain_goal, True if other in self.win_others else False]


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


    mc_team.win = 1
    kt_team.win = 1
    mc_team.lost_goal = 2
    kt_team.lost_goal = 1
    assert mc_team.goal_diff == 0
    assert kt_team.goal_diff == 0
    assert mc_team > kt_team

    mc_team.win = 1
    mc_team.win_others.append(kt_team)
    kt_team.win = 1
    assert kt_team in mc_team.win_others
    assert mc_team > kt_team
from participant import WorldCupParticipants


class WorldCupMatchManager:

    @classmethod
    def apply_result(cls, p1: WorldCupParticipants, p2: WorldCupParticipants, p1_score, p2_score):
        p1.gain_goal += p1_score
        p2.gain_goal += p2_score

        p1.lost_goal += p2_score
        p2.lost_goal += p1_score

        if p1_score > p2_score:
            p1.win += 1
            p2.lose += 1
            p1.win_others.append(p2)
        elif p2_score > p1_score:
            p2.win += 1
            p1.lose += 1
            p2.win_others.append(p1)
        elif p1_score == p2_score:
            p1.tie += 1
            p2.tie += 1

        
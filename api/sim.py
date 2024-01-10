import numpy as np

def weighted_choice(options, proba):
    cumsum = np.cumsum(proba)
    rand = np.random.random_sample()
    index = int((cumsum < rand).sum())
    index = min(index, len(options) - 1)

    return options[index]

class Batsman:
    def __init__(self):
        self.runs = 0
        self.balls = 0

    def scored(self, runs):
        self.runs += runs
        self.balls += 1

    def as_str(self):
        return f"{self.runs} ({self.balls})"
    
    def json(self):
        return {
            "runs": self.runs,
            "balls": self.balls
        }

class Bowler:
    def __init__(self):
        self.runs = 0
        self.balls = 0
        self.wickets = 0

    def scored(self, runs):
        self.runs += runs
        self.balls += 1

    def wicket_taken(self):
        self.wickets += 1
        self.balls += 1

    def as_str(self):
        return f"{self.wickets}/{self.runs} ({self.balls / 6})"
    
    def json(self):
        return {
            "runs": self.runs,
            "balls": self.balls,
            "wickets": self.wickets
        }

class Innings:
    def __init__(self, model):
        self.model = model
        self.batsmen = [Batsman() for _ in range(11)]
        self.bowlers = [Bowler() for _ in range(5)]
        self.total = 0
        self.wickets = 0
        self.ball = 1
        self.striker = self.batsmen[0]
        self.nonstriker = self.batsmen[1]

    def scored(self, runs):
        self.total += runs
        self.ball += 1

    def wicket_taken(self):
        self.wickets += 1
        self.ball += 1

    def scorecard(self):
        s = "== SCORECARD ==\n\n"
        s += f"{self.total} - {self.wickets}\n\n"
        s += "== BATTING ==\n\n"
        for batsman in self.batsmen:
            s += batsman.as_str() + "\n"

        s += "\n== BOWLING ==\n\n"
        for bowler in self.bowlers:
            s += bowler.as_str() + "\n"

        return s

    def sim(self, chasing = 0):
        bowler_idx = 0
        self.chasing = chasing

        while self.ball < 120 and self.wickets < 10:
            self.bowler = self.bowlers[bowler_idx]
            self.sim_over()
            bowler_idx += 1
            bowler_idx = bowler_idx % 5

            if self.total >= self.chasing and self.chasing != 0:
                break

    def sim_over(self):
        for _ in range(6):
            outcome = self.sim_ball()

            if outcome != 7:
                self.striker.scored(outcome)
                self.bowler.scored(outcome)
                self.scored(outcome)

                if outcome % 2 == 1:
                    self.striker, self.nonstriker = self.nonstriker, self.striker
            else:
                self.bowler.wicket_taken()
                self.wicket_taken()
                if self.wickets == 10:
                    break

                self.striker = self.batsmen[self.wickets + 1]

            if self.total >= self.chasing and self.chasing != 0:
                break

        self.striker, self.nonstriker = self.nonstriker, self.striker

    def sim_ball(self):
        proba = self.model.predict_proba([[
            self.total,
            self.wickets,
            self.ball // 6,
            self.striker.runs,
            self.striker.balls,
            self.bowler.runs,
            self.bowler.balls,
            self.bowler.wickets,
            self.chasing
        ]])

        outcome = weighted_choice([0,1,2,3,4,6,7], proba[0])

        return outcome
    
    def json(self):
        return {
            "total": self.total,
            "wickets": self.wickets,
            "balls": self.ball,
            "batting": [batsman.json() for batsman in self.batsmen],
            "bowling": [bowling.json() for bowling in self.bowlers]
        }
    

class Match:
    def __init__(self, model):
        self.first_innings = Innings(model)
        self.second_innings = Innings(model)

    def sim(self):
        self.first_innings.sim()
        self.second_innings.sim(self.first_innings.total + 1)

    def json(self):
        return {
            "innings": [self.first_innings.json(), self.second_innings.json()]
        }
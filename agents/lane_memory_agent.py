class LaneMemoryAgent:

    def __init__(self):

        self.memory = {}

    def update(
        self,
        track_id,
        in_lane
    ):

        if in_lane:

            self.memory[track_id] = 10

            return True

        if track_id in self.memory:

            if self.memory[track_id] > 0:

                self.memory[track_id] -= 1

                return True

        return False
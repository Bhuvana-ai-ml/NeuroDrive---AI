class LaneChangeAgent:

    def decide(self, driving_state):

        lane_objects = driving_state["lane_objects"]

        left_free = driving_state.get("left_lane_free", True)
        right_free = driving_state.get("right_lane_free", True)

        # No obstacle ahead
        if len(lane_objects) == 0:

            return {
                "decision": "MAINTAIN_LANE",
                "reason": "No obstacle ahead."
            }

        nearest = min(
            lane_objects,
            key=lambda x: x["distance"]
        )

        # Critical collision
        if nearest["risk"] == "critical":

            if left_free:

                return {
                    "decision": "CHANGE_LEFT",
                    "reason": "Critical obstacle. Left lane is free."
                }

            if right_free:

                return {
                    "decision": "CHANGE_RIGHT",
                    "reason": "Critical obstacle. Right lane is free."
                }

            return {
                "decision": "BRAKE",
                "reason": "No escape lane available."
            }

        return {
            "decision": "MAINTAIN_LANE",
            "reason": "Lane is safe."
        }
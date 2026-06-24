class TrafficRuleGraphAgent:

    def retrieve(self, signs):

        rules = []

        for sign in signs:

            cls = sign["class"]

            if cls == "stop sign":

                rules.append({
                    "action":"STOP",
                    "reason":"Stop sign ahead"
                })

            if cls == "traffic light":

                state = sign.get(
                    "light_state",
                    "UNKNOWN"
                )

                if state == "RED":

                    rules.append({
                        "action":"STOP",
                        "reason":"Red traffic light"
                    })

                elif state == "YELLOW":

                    rules.append({
                        "action":"SLOW_DOWN",
                        "reason":"Yellow traffic light"
                    })

                elif state == "GREEN":

                    rules.append({
                        "action":"MAINTAIN_SPEED",
                        "reason":"Green traffic light"
                    })

        return rules
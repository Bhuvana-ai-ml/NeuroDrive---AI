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

            elif cls == "traffic light":

                rules.append({
                    "action":"MONITOR_LIGHT",
                    "reason":"Traffic signal detected"
                })

        return rules
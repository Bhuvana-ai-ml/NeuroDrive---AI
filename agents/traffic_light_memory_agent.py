class TrafficLightMemoryAgent:

    def __init__(self):

        self.counter = 0

    def update(self, traffic_lights):

        if len(traffic_lights) > 0:

            self.counter = 15

            return True

        if self.counter > 0:

            self.counter -= 1

            return True

        return False
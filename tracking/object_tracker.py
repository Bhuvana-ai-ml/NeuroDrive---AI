class ObjectTracker:

    def __init__(self):

        self.previous_positions = {}

    def update(
        self,
        object_id,
        center_x,
        center_y
    ):

        speed = 0

        if object_id in self.previous_positions:

            prev_x, prev_y = self.previous_positions[
                object_id
            ]

            dx = center_x - prev_x

            dy = center_y - prev_y

            speed = (dx**2 + dy**2)**0.5

        self.previous_positions[object_id] = (
            center_x,
            center_y
        )

        return round(speed, 2)
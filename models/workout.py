class Workout:
    def __init__(self, user_id, workout_type, duration, difficulty):
        self.user_id = user_id
        self.workout_type = workout_type
        self.duration = duration
        self.difficulty = difficulty

    def get_info(self):
        return f"Workout: {self.workout_type}, Duration: {self.duration} min, Difficulty: {self.difficulty}"


class CardioWorkout(Workout):
    def __init__(self, user_id, duration, difficulty, distance):
        super().__init__(user_id, "Cardio", duration, difficulty)
        self.distance = distance

    def get_info(self):
        return super().get_info() + f", Distance: {self.distance} km"

class StrengthWorkout(Workout):
    def __init__(self, user_id, duration, difficulty, muscle_group):
        super().__init__(user_id, "Strength", duration, difficulty)
        self.muscle_group = muscle_group

    def get_info(self):
        return super().get_info() + f", Target Muscle Group: {self.muscle_group}"

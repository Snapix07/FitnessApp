from models.user import User
from controllers.workout_controller import add_workout, list_workouts
from database import initialize_db


initialize_db()

print("Welcome to FitnessApp!")

user = None
while not user:
    choice = input("Do you want to [1] Register or [2] Login? ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if choice == "1":
        User.register(username, password)
    elif choice == "2":
        user = User.login(username, password)


while True:
    print("\nMenu:")
    print("1. Add Workout")
    print("2. View Workouts")
    print("3. Exit")

    option = input("Choose an option: ")

    if option == "1":
        workout_type = input("Enter workout type (Cardio/Strength): ")
        duration = int(input("Enter duration (minutes): "))
        difficulty = input("Enter difficulty (Easy/Medium/Hard): ")
        extra_data = input("Enter extra data (Distance for Cardio / Muscle Group for Strength): ")

        add_workout(user.username, workout_type, duration, difficulty, extra_data)

    elif option == "2":
        list_workouts(user.username)

    elif option == "3":
        print("Goodbye!")
        break

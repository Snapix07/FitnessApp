import tkinter as tk
from tkinter import messagebox
from controllers.workout_controller import add_workout, list_workouts, mark_workout_done


class MainWindow:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("FitnessApp")
        self.root.geometry("500x400")

        tk.Label(self.root, text=f"Welcome, {self.user.username}!", font=("Arial", 14)).pack()

        tk.Button(self.root, text="Add Workout", command=self.add_workout_window).pack()

        self.show_done_var = tk.BooleanVar()
        self.show_done_checkbox = tk.Checkbutton(self.root, text="Show only completed workouts",
                                                 variable=self.show_done_var, command=self.view_workouts)
        self.show_done_checkbox.pack()

        self.workout_listbox = tk.Listbox(self.root)
        self.workout_listbox.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.root, text="Mark as Done", command=self.mark_selected_done).pack()
        tk.Button(self.root, text="Exit", command=self.root.quit).pack()

        self.view_workouts()
        self.root.mainloop()

    def add_workout_window(self):
        workout_window = tk.Toplevel(self.root)
        workout_window.title("Add Workout")
        workout_window.geometry("300x250")

        tk.Label(workout_window, text="Workout Type (Cardio/Strength)").pack()
        workout_type_entry = tk.Entry(workout_window)
        workout_type_entry.pack()

        tk.Label(workout_window, text="Duration (minutes)").pack()
        duration_entry = tk.Entry(workout_window)
        duration_entry.pack()

        tk.Label(workout_window, text="Difficulty (Easy/Medium/Hard)").pack()
        difficulty_entry = tk.Entry(workout_window)
        difficulty_entry.pack()

        def save_workout():
            workout_type = workout_type_entry.get()
            duration = int(duration_entry.get())
            difficulty = difficulty_entry.get()
            add_workout(self.user.user_id, workout_type, duration, difficulty)
            messagebox.showinfo("Success", "Workout added successfully!")
            self.view_workouts()

        tk.Button(workout_window, text="Save Workout", command=save_workout).pack()

    def view_workouts(self):

        self.workout_listbox.delete(0, tk.END)
        only_done = self.show_done_var.get()
        workouts = list_workouts(self.user.user_id, only_done)

        for workout in workouts:
            workout_text = f"{workout[0]}: {workout[1]}, {workout[2]} min, {workout[3]}, {workout[4]}"
            self.workout_listbox.insert(tk.END, workout_text)

    def mark_selected_done(self):

        try:
            selected = self.workout_listbox.get(self.workout_listbox.curselection())  # Получаем выбранную строку
            workout_id = int(selected.split(":")[0])
            mark_workout_done(workout_id)
            messagebox.showinfo("Success", "Workout marked as completed!")
            self.view_workouts()
        except:
            messagebox.showwarning("Warning", "Please select a workout!")

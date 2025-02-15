import datetime
import os
import re

import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog, Image

from PIL import Image

from models.user import get_avatar


from controllers.workout_controller import list_workouts, mark_workout_done, mark_workout_pending, delete_workout, \
    add_workout, update_workout
from tkcalendar import Calendar
import schedule
import threading
import time
import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


class MainWindow:
    def __init__(self, user):
        self.user = user
        self.last_ai_response = ""
        self.selected_workout_id = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("FitnessApp")
        self.root.geometry("800x600")

        self.create_navigation_panel()
        self.create_workout_page()

        self.check_reminders()
        self.root.mainloop()

    def create_navigation_panel(self):
        self.nav_frame = ctk.CTkFrame(self.root, width=180, corner_radius=0)
        self.nav_frame.pack(side="left", fill="y")

        self.workouts_button = ctk.CTkButton(self.nav_frame, text="Workouts", command=self.create_workout_page,
                                             width=160)
        self.workouts_button.pack(pady=10)

        self.ai_button = ctk.CTkButton(self.nav_frame, text="AI Assistant", command=self.create_ai_assistant, width=160)
        self.ai_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self.nav_frame, text="Settings", command=self.create_settings_page,
                                             width=160)
        self.settings_button.pack(pady=10)

    def create_workout_page(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.root, text="Your Workouts", font=("Arial", 18)).pack(pady=10)

        self.workout_combobox = ctk.CTkComboBox(self.root, width=400, state="readonly", command=self.select_workout)
        self.workout_combobox.pack(pady=10)

        ctk.CTkLabel(self.root, text="Workout Type:").pack()
        self.workout_type_entry = ctk.CTkEntry(self.root, width=400)
        self.workout_type_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Duration (min):").pack()
        self.workout_duration_entry = ctk.CTkEntry(self.root, width=400)
        self.workout_duration_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Difficulty:").pack()
        self.workout_difficulty_entry = ctk.CTkEntry(self.root, width=400)
        self.workout_difficulty_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Add Workout", command=self.add_workout).pack(pady=5)
        ctk.CTkButton(self.root, text="Update Workout", command=self.update_selected_workout, hover_color="blue").pack(
            pady=5)
        ctk.CTkButton(self.root, text="Mark as Done", command=self.mark_selected_done, hover_color="green").pack(pady=5)
        ctk.CTkButton(self.root, text="Mark as Pending", command=self.mark_selected_pending, hover_color="orange").pack(
            pady=5)
        ctk.CTkButton(self.root, text="Delete Workout", command=self.delete_selected_workout, hover_color="red").pack(
            pady=5)
        ctk.CTkButton(self.root, text="Filter by Date", command=self.open_calendar, hover_color="blue").pack(pady=5)

        self.view_workouts()

    def select_workout(self, event=None):
        selected_text = self.workout_combobox.get()
        if not selected_text:
            return

        self.selected_workout_id = int(selected_text.split(":")[0])

    def add_workout(self):
        workout_type = self.workout_type_entry.get()
        duration = self.workout_duration_entry.get()
        difficulty = self.workout_difficulty_entry.get()

        if not workout_type or not duration or not difficulty:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            duration = int(duration)
        except ValueError:
            messagebox.showwarning("Warning", "Duration must be a number!")
            return

        add_workout(self.user.user_id, workout_type, duration, difficulty, datetime.date.today().strftime("%Y-%m-%d"))
        messagebox.showinfo("Success", "Workout added successfully!")
        self.view_workouts()

    def update_selected_workout(self):
        if not self.selected_workout_id:
            messagebox.showwarning("Warning", "Please select a workout to update!")
            return

        workout_type = self.workout_type_entry.get()
        duration = self.workout_duration_entry.get()
        difficulty = self.workout_difficulty_entry.get()

        if not workout_type or not duration or not difficulty:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            duration = int(duration)
        except ValueError:
            messagebox.showwarning("Warning", "Duration must be a number!")
            return

        update_workout(self.selected_workout_id, workout_type, duration, difficulty)
        messagebox.showinfo("Success", "Workout updated successfully!")
        self.view_workouts()

    def view_workouts(self, date_filter=None):
        workouts = list_workouts(self.user.user_id, False, date_filter)
        workout_options = [f"{workout[0]}: {workout[1].replace('*', '')}, {workout[2]} min, {workout[3]}, {workout[4]}"
                           for workout in workouts]
        self.workout_combobox.configure(values=workout_options)

        if workout_options:
            self.workout_combobox.set(workout_options[0])
            self.select_workout()

    def mark_selected_done(self):
        if not self.selected_workout_id:
            messagebox.showwarning("Warning", "Please select a workout!")
            return

        mark_workout_done(self.selected_workout_id)
        messagebox.showinfo("Success", "Workout marked as completed!")
        self.view_workouts()

    def mark_selected_pending(self):
        if not self.selected_workout_id:
            messagebox.showwarning("Warning", "Please select a workout!")
            return

        mark_workout_pending(self.selected_workout_id)
        messagebox.showinfo("Success", "Workout marked as pending!")
        self.view_workouts()

    def delete_selected_workout(self):
        if not self.selected_workout_id:
            messagebox.showwarning("Warning", "Please select a workout!")
            return

        delete_workout(self.selected_workout_id)
        messagebox.showinfo("Success", "Workout deleted successfully!")
        self.view_workouts()

    def open_calendar(self):
        self.calendar_window = ctk.CTkToplevel(self.root)
        self.calendar_window.title("Select Date")
        self.calendar_window.geometry("300x300")

        self.calendar = Calendar(self.calendar_window, selectmode='day', year=2024, month=2, day=16)
        self.calendar.pack(pady=20)

        ctk.CTkButton(self.calendar_window, text="Apply Filter", command=self.apply_date_filter).pack()

    def apply_date_filter(self):
        selected_date = self.calendar.get_date()
        self.view_workouts(date_filter=selected_date)
        self.calendar_window.destroy()

    def create_ai_assistant(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.root, text="AI Workout Assistant", font=("Arial", 18)).pack(pady=10)

        self.chatbox = ctk.CTkTextbox(self.root, width=600, height=300)
        self.chatbox.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self.root, width=500)
        self.input_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Send", command=self.ask_ai).pack(pady=5)

    def ask_ai(self):
        question = self.input_entry.get()
        response = self.generate_ai_response(question)

        clean_response = re.sub(r"[*_`]", "", response)
        self.last_ai_response = clean_response
        self.chatbox.insert("end", f"You: {question}\n\nAI: {response}\n\n")

    def generate_ai_response(self, question):
        prompt = f"Answer only about training and fitness. Ignore other topics. Question: {question}"

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text


    def create_settings_page(self):
        self.clear_main_frame()
        ctk.CTkLabel(self.root, text="Settings", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self.root, text="Profile", command=self.create_profile_page).pack(pady=5)
        ctk.CTkButton(self.root, text="Set Workout Reminder", command=self.set_reminder).pack(pady=5)
        ctk.CTkButton(self.root, text="Log Out", command=self.logout).pack(pady=5)
        ctk.CTkButton(self.root, text="Delete Account", command=self.delete_account).pack(pady=5)

    def set_reminder(self):
        reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder time (HH:MM format):")
        if reminder_time:
            try:
                schedule.every().day.at(reminder_time).do(self.show_reminder)
                messagebox.showinfo("Reminder Set", f"Workout reminder set for {reminder_time}")
            except:
                messagebox.showerror("Error", "Invalid time format! Use HH:MM (e.g., 10:30)")

    def show_reminder(self):
        messagebox.showinfo("Workout Reminder", "Time to work out!")

    def logout(self):
        self.root.destroy()
        from ui.start_window import StartWindow
        StartWindow()

    def delete_account(self):
        from models.user import User
        confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if confirmation:
            User.delete(self.user.user_id)
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            self.root.destroy()
            from ui.login_window import LoginWindow
            LoginWindow()

    def clear_main_frame(self):
        for widget in self.root.winfo_children():
            if widget not in [self.nav_frame]:
                widget.destroy()

    def check_reminders(self):

        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=run_schedule, daemon=True)
        thread.start()

    def create_profile_page(self):
        self.clear_main_frame()

        self.avatar_display = ctk.CTkLabel(self.root, text="")
        self.avatar_display.pack(pady=5)
        ctk.CTkLabel(self.root, text="My Profile", font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(self.root, text="Username:").pack()
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.insert(0, self.user.username)
        self.username_entry.pack(pady=5)

        self.avatar_label = ctk.CTkLabel(self.root, text="No Avatar Selected", font=("Arial", 12))
        self.avatar_label.pack(pady=5)
        ctk.CTkButton(self.root, text="Choose Avatar", command=self.choose_avatar).pack(pady=5)

        saved_avatar = get_avatar(self.user.user_id)
        if saved_avatar and os.path.exists(saved_avatar):
            img = Image.open(saved_avatar)
            img = img.resize((100, 100))
            self.avatar_img = ctk.CTkImage(light_image=img, size=(100, 100))

            self.avatar_display = ctk.CTkLabel(self.root, image=self.avatar_img, text="")
            self.avatar_display.pack(pady=5)


        ctk.CTkLabel(self.root, text="Fitness Goal:").pack()
        self.goal_combobox = ctk.CTkComboBox(self.root, values=["Lose Weight", "Gain Muscle", "Stay Fit"])
        self.goal_combobox.set("Stay Fit")
        self.goal_combobox.pack(pady=5)

        ctk.CTkButton(self.root, text="Save Changes", command=self.save_profile).pack(pady=10)

    def choose_avatar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.avatar_label.configure(text="")

            img = Image.open(file_path)
            img = img.resize((100, 100))

            self.avatar_img = ctk.CTkImage(light_image=img, size=(100, 100))

            if hasattr(self, 'avatar_display'):
                self.avatar_display.configure(image=self.avatar_img)
            else:
                self.avatar_display = ctk.CTkLabel(self.root, image=self.avatar_img, text="")
                self.avatar_display.pack(pady=5)


    def save_profile(self):
        new_username = self.username_entry.get()
        new_goal = self.goal_combobox.get()

        messagebox.showinfo("Profile Updated", f"Username: {new_username}\nGoal: {new_goal}")

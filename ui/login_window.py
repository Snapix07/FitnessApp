import customtkinter as ctk
from tkinter import messagebox
from models.user import User
from ui.main_window import MainWindow

class LoginWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Login - FitnessApp")
        self.root.geometry("400x300")

        ctk.CTkLabel(self.root, text="Login", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(self.root, text="Username:").pack()
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Password:").pack()
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self.root, text="Back", command=self.go_back).pack(pady=5)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User.login(username, password)

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.root.destroy()
            MainWindow(user)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def go_back(self):
        self.root.destroy()
        from ui.start_window import StartWindow
        StartWindow()

if __name__ == "__main__":
    LoginWindow()

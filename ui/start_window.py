import customtkinter as ctk
from login_window import LoginWindow
from register_window import RegisterWindow

class StartWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Welcome - FitnessApp")
        self.root.geometry("400x300")

        ctk.CTkLabel(self.root, text="Welcome to FitnessApp!", font=("Arial", 20)).pack(pady=20)

        ctk.CTkButton(self.root, text="Login", command=self.open_login).pack(pady=10)
        ctk.CTkButton(self.root, text="Register", command=self.open_register).pack(pady=10)

        self.root.mainloop()

    def open_login(self):
        self.root.destroy()
        LoginWindow()

    def open_register(self):
        self.root.destroy()
        RegisterWindow()

if __name__ == "__main__":
    StartWindow()

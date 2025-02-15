import customtkinter as ctk
from tkinter import messagebox
from models.user import User



class RegisterWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Register - FitnessApp")
        self.root.geometry("400x350")

        ctk.CTkLabel(self.root, text="Register", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(self.root, text="Username:").pack()
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Password:").pack()
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Confirm Password:").pack()
        self.confirm_password_entry = ctk.CTkEntry(self.root, show="*")
        self.confirm_password_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Register", command=self.register).pack(pady=10)
        ctk.CTkButton(self.root, text="Back", command=self.go_back).pack(pady=5)

        self.root.mainloop()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        result = User.register(username, password)
        if result == "Username already taken":
            messagebox.showerror("Error", "This username is already in use. Choose another one.")
        else:
            messagebox.showinfo("Registration", "Account created successfully!")
            self.root.destroy()
            from ui.login_window import LoginWindow
            LoginWindow()

    def go_back(self):
        self.root.destroy()
        from ui.start_window import StartWindow
        StartWindow()

if __name__ == "__main__":
    RegisterWindow()

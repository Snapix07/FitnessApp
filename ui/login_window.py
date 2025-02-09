import tkinter as tk
from tkinter import messagebox
from models.user import User
from ui.main_window import MainWindow
from database import initialize_db
initialize_db()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - FitnessApp")
        self.root.geometry("300x250")

        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack()
        tk.Button(root, text="Register", command=self.register).pack()

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

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = User.register(username, password)
        messagebox.showinfo("Registration", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

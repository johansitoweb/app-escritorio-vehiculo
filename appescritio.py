import tkinter as tk  
from tkinter import messagebox, simpledialog  
import sqlite3  
from PIL import Image, ImageTk  


class CarWashApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Car Wash App")  
        self.root.geometry("400x300")  
        self.create_db()  

        # Cargar imagen de fondo  
        self.bg_image = Image.open("login_bg.png")  
        self.bg_image = self.bg_image.resize((400, 300))  
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  

        self.bg_label = tk.Label(self.root, image=self.bg_photo)  
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  

        self.create_login_widgets()  

    def create_login_widgets(self):  
        self.label_username = tk.Label(self.root, text="Username", bg='white')  
        self.label_username.pack(pady=10)  
        self.entry_username = tk.Entry(self.root)  
        self.entry_username.pack(pady=5)  

        self.label_password = tk.Label(self.root, text="Password", bg='white')  
        self.label_password.pack(pady=10)  
        self.entry_password = tk.Entry(self.root, show="*")  
        self.entry_password.pack(pady=5)  

        self.button_login = tk.Button(self.root, text="Login", command=self.login)  
        self.button_login.pack(pady=20)  

        self.button_register = tk.Button(self.root, text="Register", command=self.open_register)  
        self.button_register.pack(pady=5)  

    def create_db(self):  
        conn = sqlite3.connect('car_wash.db')  
        c = conn.cursor()  
        c.execute('''  
            CREATE TABLE IF NOT EXISTS users (  
                username TEXT PRIMARY KEY,  
                password TEXT NOT NULL  
            )  
        ''')  
        c.execute('''  
            CREATE TABLE IF NOT EXISTS services (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                service_name TEXT NOT NULL,  
                price REAL NOT NULL  
            )  
        ''')  
        conn.commit()  
        conn.close()  

    def login(self):  
        username = self.entry_username.get()  
        password = self.entry_password.get()  

        conn = sqlite3.connect('car_wash.db')  
        c = conn.cursor()  

        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))  
        user = c.fetchone()  

        conn.close()  

        if user:  
            messagebox.showinfo("Login", "Login successful!")  
            self.open_main_menu()  
        else:  
            messagebox.showerror("Login", "Invalid username or password")  

    def open_register(self):  
        username = simpledialog.askstring("Register", "Enter username:")  
        password = simpledialog.askstring("Register", "Enter password:", show="*")  

        if username and password:  
            self.register_user(username, password)  

    def register_user(self, username, password):  
        conn = sqlite3.connect('car_wash.db')  
        c = conn.cursor()  

        try:  
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))  
            conn.commit()  
            messagebox.showinfo("Register", "User registered successfully!")  
        except sqlite3.IntegrityError:  
            messagebox.showerror("Register", "Username already exists.")  
        finally:  
            conn.close()  

    def open_main_menu(self):  
        self.clear_widgets()  
        self.label_title = tk.Label(self.root, text="Main Menu", font=("Arial", 16))  
        self.label_title.pack(pady=10)  

        self.button_add_service = tk.Button(self.root, text="Add Service", command=self.add_service)  
        self.button_add_service.pack(pady=10)  

        self.button_view_services = tk.Button(self.root, text="View Services", command=self.view_services)  
        self.button_view_services.pack(pady=10)  

        self.button_logout = tk.Button(self.root, text="Logout", command=self.logout)  
        self.button_logout.pack(pady=10)  

    def clear_widgets(self):  
        for widget in self.root.winfo_children():  
            widget.destroy()  

    def add_service(self):  
        service_name = simpledialog.askstring("Add Service", "Enter service name:")  
        price = simpledialog.askfloat("Add Service", "Enter service price:")  

        if service_name and price is not None:  
            self.save_service(service_name, price)  

    def save_service(self, service_name, price):  
        conn = sqlite3.connect('car_wash.db')  
        c = conn.cursor()  
        c.execute("INSERT INTO services (service_name, price) VALUES (?, ?)", (service_name, price))  
        conn.commit()  
        conn.close()  
        messagebox.showinfo("Add Service", "Service added successfully!")  

    def view_services(self):  
        conn = sqlite3.connect('car_wash.db')  
        c = conn.cursor()  
        c.execute("SELECT * FROM services")  
        services = c.fetchall()  
        conn.close()  

        services_list = "Available Services:\n"  
        for service in services:  
            services_list += f"{service[1]} - ${service[2]:.2f}\n"  

        messagebox.showinfo("Services", services_list)  

    def logout(self):  
        self.clear_widgets()  
        self.create_login_widgets()  

if __name__ == "__main__":  
    root = tk.Tk()  
    app = CarWashApp(root)  
    root.mainloop()
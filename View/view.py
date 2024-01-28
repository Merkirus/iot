import tkinter as tk
from enum import Enum
from tkinter.constants import DISABLED

WIDTH = 450
HEIGHT = 300
PADDING = 15

class State(Enum):
    LOGIN = 0
    MAIN = 1
    INSERT = 2
    REGISTER_CLIENT = 3
    REGISTER_WORKER = 4
    MANAGER = 5

class Gui(tk.Tk,):
    def __init__(self) -> None:
        super().__init__()

        self.my_state = State.LOGIN
        self.my_prev_state = State.LOGIN

        self.title("Book manager system")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2

        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        self.resizable(False, False)

        self.login_view = LoginView(self, WIDTH, HEIGHT)
        self.main_view = MainView(self, WIDTH, HEIGHT)
        self.book_inster_view = BookInsertView(self, WIDTH, HEIGHT)
        self.register_client_view = RegisterView(self, WIDTH, HEIGHT, "client")
        self.register_worker_view = RegisterView(self, WIDTH, HEIGHT, "worker")
        self.rent_return_view = BookManagerView(self, WIDTH, HEIGHT)

        self.login_view.pack(fill='both', expand=True)

    def update_card(self, message):
        match self.my_state:
            case State.LOGIN:
                self.login_view.update_user(message)
            case State.REGISTER_CLIENT:
                self.register_client_view.update_user(message)
            case State.REGISTER_WORKER:
                self.register_worker_view.update_user(message)
            case _:
                self.rent_return_view.update_user(message)
                self.switch_view("manager")

    def switch_view(self, view):
        for displayed_frame in self.winfo_children():
            displayed_frame.pack_forget()

        self.my_prev_state = self.my_state

        match view:
            case "main":
                self.main_view.pack(fill='both', expand=True)   
                self.my_state = State.MAIN
            case "manager":
                self.rent_return_view.pack(fill='both', expand=True)
                self.my_state = State.MANAGER
            case "register_worker":
                self.register_worker_view.pack(fill='both', expand=True)
                self.my_state = State.REGISTER_WORKER
            case "register_client":
                self.register_client_view.pack(fill='both', expand=True)
                self.my_state = State.REGISTER_CLIENT
            case "insert":
                self.book_inster_view.pack(fill='both', expand=True)
                self.my_state = State.INSERT
            case "login":
                self.login_view.pack(fill='both', expand=True)
                self.my_state = State.LOGIN
            case _:
                self.main_view.pack(fill='both', expand=True)
                self.my_state = State.MAIN

    def rent_book_listener(self, fun):
        self.rent_return_view.configure_rent_book(fun)

    def return_book_listener(self, fun):
        self.rent_return_view.configure_return_book(fun)

    def login_listener(self, fun):
        self.login_view.configure_login(fun)

    def register_listener(self, fun):
        self.register_client_view.configure_register(fun)
        self.register_worker_view.configure_register(fun)

    def insert_listener(self, fun):
        self.book_inster_view.configure_insert(fun)

    def run(self):
        self.mainloop()

class LoginView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.login_var = tk.StringVar(self)
        self.password_var = tk.StringVar(self)

        self.login_label = tk.Label(self, text="Login")
        self.password_label = tk.Label(self, text="Password")

        self.login_entry = tk.Entry(self, textvariable=self.login_var, relief=tk.SUNKEN, state=DISABLED)
        self.password_entry = tk.Entry(self, textvariable=self.password_var, relief=tk.SUNKEN)

        self.login_button = tk.Button(self, text="Login")
        self.register_button = tk.Button(self, text="Register", command=lambda: self.master.switch_view("register_worker"))

        self.login_label.grid(column=0, row=0)
        self.login_entry.grid(column=1, row=0)

        self.password_label.grid(column=0, row=1)
        self.password_entry.grid(column=1, row=1)

        self.login_button.grid(column=0, row=2)
        self.register_button.grid(column=1, row=2)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)
        
    def configure_login(self, fun):
        def login():
            response = fun(self.login_var.get(), self.password_var.get())
            popup_window(self, response)
            if response == "OK":
                self.master.switch_view("main")
            self.password_var.set("")

        self.login_button.config(command=login)

    def update_user(self, user):
        self.login_var.set(user)

class MainView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.book_insert_button = tk.Button(self, command=lambda: self.master.switch_view("insert"), text="Insert book")
        self.register_client_button = tk.Button(self, command=lambda: self.master.switch_view("register_client"), text="Register client")
        self.book_manager_button = tk.Button(self, command=lambda: self.master.switch_view("manager"), text="Book manager")

        self.waiting_label = tk.Label(self, text="Loading...")

        self.book_insert_button.grid(column=0, row=0)
        self.register_client_button.grid(column=1, row=0)
        self.book_manager_button.grid(column=2, row=0)

        self.waiting_label.grid(column=0, row=1, columnspan=3)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

class RegisterView(tk.Frame):
    def __init__(self, master, width, height, role):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.role = role

        self.name_var = tk.StringVar(self)
        self.surname_var = tk.StringVar(self)
        self.phone_var = tk.StringVar(self)
        self.email_var = tk.StringVar(self)
        self.password_var = tk.StringVar(self)
        self.checkbox_var = tk.IntVar(self)
        self.checkbox_var.set(0)
        self.uuid_var = tk.StringVar(self)

        self.name_label = tk.Label(self, text="Name")
        self.surname_label = tk.Label(self, text="Surname")
        self.phone_label = tk.Label(self, text="Phone")
        self.email_label = tk.Label(self, text="Email")
        self.password_label = tk.Label(self, text="Password")

        self.name_entry = tk.Entry(self, textvariable=self.name_var, relief=tk.SUNKEN)
        self.surname_entry = tk.Entry(self, textvariable=self.surname_var, relief=tk.SUNKEN)
        self.phone_entry = tk.Entry(self, textvariable=self.phone_var, relief=tk.SUNKEN)
        self.email_entry = tk.Entry(self, textvariable=self.email_var, relief=tk.SUNKEN)
        self.password_entry = tk.Entry(self, textvariable=self.password_var, relief=tk.SUNKEN)
        self.uuid_checkbox = tk.Checkbutton(self, text="Card", variable=self.checkbox_var, state=DISABLED)

        def back():
            self.uuid_var.set("")
            self.checkbox_var.set(0)
            self.name_var.set("")
            self.surname_var.set("")
            self.phone_var.set("")
            self.email_var.set("")
            self.password_var.set("")
            if self.master.my_prev_state == State.LOGIN:
                self.master.switch_view("login")
            else:
                self.master.switch_view("main")

        self.register_button = tk.Button(self, text="Register")
        self.back_button = tk.Button(self, text="Back", command=back)

        self.name_label.grid(column=0, row=0)
        self.surname_label.grid(column=0, row=1)
        self.phone_label.grid(column=0, row=2)
        self.email_label.grid(column=0, row=3)
        self.password_label.grid(column=0, row=4)

        self.name_entry.grid(column=1, row=0)
        self.surname_entry.grid(column=1, row=1)
        self.phone_entry.grid(column=1, row=2)
        self.email_entry.grid(column=1, row=3)
        self.password_entry.grid(column=1, row=4)
        self.uuid_checkbox.grid(column=2, row=2)

        self.register_button.grid(column=2, row=0)
        self.back_button.grid(column=2, row=1)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def configure_register(self, fun):
        def register():
            response = fun(
                self.uuid_var.get(),
                self.name_var.get(),
                self.surname_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                self.password_var.get(),
                self.role)
            popup_window(self, response)
            self.uuid_var.set("")
            self.checkbox_var.set(0)
            self.name_var.set("")
            self.surname_var.set("")
            self.phone_var.set("")
            self.email_var.set("")
            self.password_var.set("")
            self.master.switch_view("login")

        self.register_button.config(command=register)
    
    def update_user(self, user):
        self.checkbox_var.set(1)
        self.uuid_var.set(user)

class BookInsertView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.author_var = tk.StringVar(self)
        self.title_var = tk.StringVar(self)
        self.isbn_var = tk.StringVar(self)
        self.id_var = tk.StringVar(self)

        self.author_label = tk.Label(self, text="Author")
        self.title_label = tk.Label(self, text="Title")
        self.isbn_label = tk.Label(self, text="ISBN")
        self.book_id_label = tk.Label(self, text="ID")

        self.author_entry = tk.Entry(self, textvariable=self.author_var, relief=tk.SUNKEN)
        self.title_entry = tk.Entry(self, textvariable=self.title_var, relief=tk.SUNKEN)
        self.isbn_entry = tk.Entry(self, textvariable=self.isbn_var, relief=tk.SUNKEN)
        self.id_entry = tk.Entry(self, textvariable=self.id_var, relief=tk.SUNKEN)

        def back():
            self.author_var.set("")
            self.title_var.set("")
            self.isbn_var.set("")
            self.id_var.set("")
            self.master.switch_view("main")

        self.insert_button = tk.Button(self, text="Register")
        self.back_button = tk.Button(self, text="Back", command=back)

        self.author_label.grid(column=0, row=0)
        self.title_label.grid(column=0, row=1)
        self.isbn_label.grid(column=0, row=2)
        self.book_id_label.grid(column=0, row=3)

        self.author_entry.grid(column=1, row=0)
        self.title_entry.grid(column=1, row=1)
        self.isbn_entry.grid(column=1, row=2)
        self.id_entry.grid(column=1, row=3)

        self.insert_button.grid(column=2, row=0)
        self.back_button.grid(column=2, row=1)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def configure_insert(self, fun):
        def insert():
            response = fun(self.author_var.get(), self.title_var.get(), self.isbn_var.get(),self.id_var.get())
            popup_window(self, response)
            self.author_var.set("")
            self.title_var.set("")
            self.isbn_var.set("")
            self.id_var.set("")
            self.master.switch_view("main")

        self.insert_button.config(command=insert)

class BookManagerView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.user_var = tk.StringVar(self)
        self.book_var = tk.StringVar(self)

        self.user_label = tk.Label(self, text="User UUID")
        self.book_label = tk.Label(self, text="Book ID")

        self.user_entry = tk.Entry(self, textvariable=self.user_var, relief=tk.SUNKEN, state=DISABLED)
        self.book_entry = tk.Entry(self, textvariable=self.book_var, relief=tk.SUNKEN)

        self.return_button = tk.Button(self, text="Return")
        self.rent_button = tk.Button(self, text="Rent")
        self.back_button = tk.Button(self, text="Back", command=lambda: self.master.switch_view("main"))

        self.user_label.grid(column=0, row=0, sticky=tk.W)
        self.user_entry.grid(column=1, row=0, sticky=tk.E)

        self.book_label.grid(column=0, row=1, sticky=tk.W)
        self.book_entry.grid(column=1, row=1, sticky=tk.E)

        self.return_button.grid(column=2, row=0)
        self.rent_button.grid(column=2, row=1)

        self.back_button.grid(column=2, row=2)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def configure_return_book(self, fun):
        def return_book_request():
            if (self.book_var.get() != "" and self.user_var.get() != ""):
                response = fun(self.user_var.get(), self.book_var.get())
                popup_window(self, response)
                self.book_var.set("")
                self.user_var.set("")
                self.master.switch_view("main")

        self.return_button.config(command=return_book_request)

    def configure_rent_book(self, fun):
        def rent_book_request():
            if (self.book_var.get() != "" and self.user_var.get() != ""):
                response = fun(self.user_var.get(), self.book_var.get())
                popup_window(self, response)
                self.book_var.set("")
                self.user_var.set("")
                self.master.switch_view("main")

        self.rent_button.config(command=rent_book_request)

    def update_user(self, user):
        self.user_var.set(user)


def popup_window(root, response):
    popup = tk.Toplevel(root)
    popup.title("Response")

    x = root.master.winfo_x() + (root.master.winfo_width() - popup.winfo_reqwidth()) // 2
    y = root.master.winfo_y() + (root.master.winfo_height() - popup.winfo_reqheight()) // 2

    popup.geometry(f"{WIDTH // 2}x{HEIGHT // 2}+{x}+{y}")
    popup.resizable(False, False)

    popup_label = tk.Label(popup, text=response)
    close_button = tk.Button(popup, text="Close", command=popup.destroy)

    popup_label.pack(padx=PADDING, pady=PADDING)
    close_button.pack(padx=PADDING, pady=PADDING)

if __name__ == "__main__":
    gui = Gui()

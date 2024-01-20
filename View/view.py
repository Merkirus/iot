import tkinter as tk
from tkinter.constants import DISABLED

WIDTH = 450
HEIGHT = 200
PADDING = 15

class Gui(tk.Tk,):
    def __init__(self) -> None:
        super().__init__()
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
        self.register_client_view = RegisterClientView(self, WIDTH, HEIGHT)
        self.rent_return_view = BookManagerView(self, WIDTH, HEIGHT)

        #TODO Login first, for now main first
        self.main_view.pack(fill='both', expand=True)

    def update_manager(self, message):
        self.rent_return_view.update_user(message)
        self.switch_view("manager")

    def switch_view(self, view):
        for displayed_frame in self.winfo_children():
            displayed_frame.pack_forget()

        match view:
            case "main":
                self.main_view.pack(fill='both', expand=True)
            case "manager":
                self.rent_return_view.pack(fill='both', expand=True)

    def rent_book_listener(self, fun):
        self.rent_return_view.configure_rent_book(fun)

    def return_book_listener(self, fun):
        self.rent_return_view.configure_return_book(fun)

    def run(self):
        self.mainloop()

class LoginView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)

class MainView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.book_insert_button = tk.Button(self, command=lambda: self.master.switch_view("insert"), text="Insert book")
        self.register_client_button = tk.Button(self, command=lambda: self.master.switch_view("register"), text="Register client")
        self.book_manager_button = tk.Button(self, command=lambda: self.master.switch_view("manager"), text="Book manager")

        self.waiting_label = tk.Label(self, text="Loading...")

        self.book_insert_button.grid(column=0, row=0)
        self.register_client_button.grid(column=1, row=0)
        self.book_manager_button.grid(column=2, row=0)

        self.waiting_label.grid(column=0, row=1, columnspan=3)

        for elem in self.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

class BookInsertView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

class RegisterClientView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

class BookManagerView(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master=master, width=width, height=height)
        self.master: Gui = master

        self.user_var = tk.StringVar(self)
        self.book_var = tk.StringVar(self)

        self.user_label = tk.Label(self, text="User UUID")
        self.book_label = tk.Label(self, text="Book ISBN")

        self.user_entry = tk.Entry(self, textvariable=self.user_var, relief=tk.SUNKEN, state=DISABLED)
        self.book_entry = tk.Entry(self, textvariable=self.book_var, relief=tk.SUNKEN)

        self.return_button = tk.Button(self, text="Return")
        self.rent_button = tk.Button(self, text="Rent")
        self.back_button = tk.Button(self, text="Back", command=lambda: self.master.switch_view("main"))

        self.user_label.grid(column=0, row=0, sticky=tk.W)
        self.user_entry.grid(column=1, row=0, sticky=tk.E)

        self.book_label.grid(column=0, row=1, sticky=tk.W)
        self.book_entry.grid(column=1, row=1, sticky=tk.E)

        self.return_button.grid(column=1, row=2, sticky=tk.W)
        self.rent_button.grid(column=1, row=2, sticky=tk.E)

        self.back_button.grid(column=0, row=2)

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

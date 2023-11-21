import tkinter as tk
from tkinter import ttk
from controllers.tasks import Tasks as tasks_controller
from services.auth import Authentication as auth

auth = auth()

class TaskCard(tk.Toplevel):
    def __init__(self, root, task, status_change_callback, delete_task_callback):
        super().__init__(root)
        self.title("Kanban Board")
        self.geometry("300x500")

        self.task = task
        self.status_change_callback = status_change_callback
        self.delete_task_callback = delete_task_callback

        label = ttk.Label(self, text=f"Task: {task['title']}")
        label.pack(pady=5)

        status_label = ttk.Label(self, text="Status:")
        status_label.pack(pady=5)

        self.status_var = tk.StringVar()
        self.status_var.set(task['status'])

        status_options = ttk.Combobox(self, values=['backlog', 'toDo', 'inProgress', 'done'], textvariable=self.status_var)
        status_options.pack(pady=5)

        details_label = ttk.Label(self, text="Details:")
        details_label.pack(pady=5)

        self.details_text = tk.Text(self, height=4, width=30)
        self.details_text.insert(tk.INSERT, task['description'])
        self.details_text.pack(pady=5)

        cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.pack(pady=5)

        save_details_button = ttk.Button(self, text="Save Details", command=self.save_details)
        save_details_button.pack(pady=5)

        delete_button = ttk.Button(self, text="Delete", command=self.delete_task)
        delete_button.pack(pady=5)

    def save_details(self):
        details = self.details_text.get("1.0", tk.END).strip()
        new_status = self.status_var.get()
        updated_task = self.task
        updated_task['description'] = details
        updated_task['status'] = new_status
        self.status_change_callback(self.task, updated_task)
        self.destroy()
    
    def delete_task(self):
        self.delete_task_callback(self.task['_id'])
        self.destroy()


class KanbanBoard:
    def __init__(self, root):

        self.username = None

        # Initialize the frame
        self.root = root
        self.root.title("Task Details")
        self.root.geometry("1500x500")

        self.columns = [
            'backlog',
            'toDo',
            'inProgress',
            'done'
        ]
        self.column_index_hashmap = {
            'backlog': 0, 
            'toDo': 1,
            'inProgress': 2,
            'done': 3
        }

        self.validate_login()
 
    def validate_login(self):
        self.alert_window = tk.Toplevel(self.root)
        self.alert_window.title("Login")

        self.login_status_label = ttk.Label(self.alert_window, text="")
        self.login_status_label.grid(row=0, column=0, padx=(0, 5), sticky=tk.W)

        username_label = ttk.Label(self.alert_window, text="Enter username:")
        username_label.grid(row=1, column=0, padx=(0, 5), sticky=tk.W)

        password_label = ttk.Label(self.alert_window, text="Enter Password:")
        password_label.grid(row=2, column=0, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        self.username_entry = ttk.Entry(self.alert_window, width=30)
        self.username_entry.grid(row=1, column=1, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        self.password_entry = ttk.Entry(self.alert_window, width=30)
        self.password_entry.grid(row=2, column=1, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        login_button = ttk.Button(self.alert_window, text="Login", command=self.post_login_attempt)
        login_button.grid(row=3, column=1, pady=(5, 0), sticky=tk.W)

        signup_button = ttk.Button(self.alert_window, text="Signup", command=self.post_signup_attempt)
        signup_button.grid(row=4, column=1, pady=(5, 0), sticky=tk.W)
        
    def post_login_attempt(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if auth.login(username, password):
            print("Login Sucessful")
            self.alert_window.destroy()

            # get all tasks of user
            self.username = username
            self.tasks = tasks_controller.get_all_tasks(self.username)

            # Create the table
            self.create_board()
            self.create_task_entry()
        else:
            self.login_status_label.configure(text="Incorrect Details. \nUsername: admin \npassword: admin for testing")

    def post_signup_attempt(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if auth.signup(username, password):
            print("Signup Sucessful")
            self.alert_window.destroy()

            # get all tasks of user
            self.username = username
            self.tasks = tasks_controller.get_all_tasks(self.username)

            # Create the table
            self.create_board()
            self.create_task_entry()
        else:
            self.login_status_label.configure(text="Incorrect Details. Username: admin, password: admin for testing")

    def show_alert(self, message):
        alert_window = tk.Toplevel(self.root)
        alert_window.title("Alert")

        label = ttk.Label(alert_window, text=message, font=('Helvetica', 12))
        label.pack(padx=30, pady=30)

        ok_button = ttk.Button(alert_window, text="OK", command=alert_window.destroy)
        ok_button.pack(pady=10)

    def create_board(self):
        columns = ['Backlog', 'Todo', 'In Progress', 'Done']
        column_display_to_key = {
            'Backlog': 'backlog',
            'Todo': 'toDo',
            'In Progress': 'inProgress',
            'Done': 'done'
        }
        scrollable_frame = self.create_scrollable_frame(self.root, 0)

        frames={0: None, 1: None, 2:None, 3:None}
        for col_index, col_name in enumerate(columns):
            frame = ttk.Frame(scrollable_frame, relief="ridge", borderwidth=2)
            frame.grid(row=0, column=col_index, padx=10, pady=10, sticky="nsew")
            frames[col_index] = frame
            task_count = len([i for i in self.tasks if i['status'] == f'{column_display_to_key[col_name]}'])
            tk.Label(frame, text=f'{col_name} ({task_count})', font=('Helvetica', 12, 'bold'), width=30).grid(row=0, column=col_index, padx=10, pady=5)

        for row_index, task in enumerate(self.tasks):
            label_text = task['title'] if 'title' in task.keys() else ""
            col_index = self.column_index_hashmap[task['status']]
            label = tk.Label(frames[col_index], text=label_text, borderwidth=1, relief="solid", width=30, height=2)
            label.grid(row=row_index + 1, column=col_index, padx=10, pady=5)
            label.bind('<Button-1>', lambda event, task_object=task: self.open_card(task_object))

    def update_state(self,):
        self.tasks = tasks_controller.get_all_tasks(self.username)        
        self.create_board()

    def open_card(self, task_object):
        selected_task = task_object
        try:
            task_card = TaskCard(
                self.root,
                selected_task,
                lambda task, status: self.update_task_status(task, status),
                lambda task_id: self.delete_task(task_id),
            )
            task_card.grab_set()
            self.root.wait_window(task_card)
        except tk.TclError:
            pass  # Ignore if no task is selected

    def update_task_status(self, task, update):
        tasks_controller.update_task(task['_id'], update)
        self.update_state()

    def create_task_entry(self):
        entry_frame = ttk.Frame(self.root)
        entry_frame.grid(row=len(self.tasks) + 1, column=0, columnspan=len(self.columns), pady=10, padx=10)

        welcome_label = ttk.Label(entry_frame, text=f'Welcome {self.username}')
        welcome_label.grid(row=0, column=0, padx=(0, 5), sticky=tk.W)

        title_label = ttk.Label(entry_frame, text="New Task:")
        title_label.grid(row=1, column=0, padx=(0, 5), sticky=tk.W)

        description_label = ttk.Label(entry_frame, text="Description:")
        description_label.grid(row=2, column=0, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        self.title_entry = ttk.Entry(entry_frame, width=30)
        self.title_entry.grid(row=1, column=1, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        self.description_entry = ttk.Entry(entry_frame, width=30)
        self.description_entry.grid(row=2, column=1, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        add_button = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=3, column=1, pady=(5, 0), sticky=tk.W)

        self.create_status_box(entry_frame, tasks_controller.get_db_status(), 4, 1)

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            # Add the task to the "Backlog" column by default
            tasks_controller.create_task(self.username, {
                "title": title,
                "description": description,
                "status": "backlog"
            })
            self.update_state()

            # Clear the entry field
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        else:
            self.show_alert("Add both title and description to create task!")

    def delete_task(self, task_id):
        tasks_controller.delete_task(task_id)
        self.update_state()

    def create_status_box(self, root, flag, row, col):
        label = ttk.Label(root, text=f'Database Connection: {"on" if flag else "off"}', font=('Helvetica', 12, 'bold'), width=25)
        
        if flag:
            label.configure(background="green", foreground="white")
        else:
            label.configure(background="red", foreground="white")

        label.grid(row=row, column=col, pady=10)

    def create_scrollable_frame(self, root, row):
        frame = ttk.Frame(root)
        frame.grid(row=row, column=0, pady=10)

        canvas = tk.Canvas(frame, width=1300, borderwidth=2, relief="solid")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar_x.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        return scrollable_frame

class Main:
    def __init__(self):
        self.root = tk.Tk()
        KanbanBoard(self.root)
        self.root.mainloop()

Main()
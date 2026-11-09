
import os
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import Screen
from functions.loader import load_dataset


class LoadInterface(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.build_content()

    def build_content(self):
        button_frame = ttk.Frame(self.top_frame)
        button_frame.grid(row=0, column=0, pady=20)

        self.load_button = ttk.Button(button_frame, text="Browse File", width=30,
            command=self.browse_file)
        self.load_button.pack(side="left", padx=20)

        self.profile_button = ttk.Button(button_frame, text="Create Profile", width=30,
            command=lambda: self.controller.show_frame("ProfileInterface"))
        self.profile_button.pack(side="left", padx=20)

        self.dashboard_button = ttk.Button(button_frame, text="Intelligence Dashboard", width=30,
            command=lambda: self.controller.show_frame("DashboardInterface"))
        self.dashboard_button.pack(side="left", padx=20)

        navigation_frame = ttk.Frame(self.bottom_frame)
        navigation_frame.grid(row=1, column=0, pady=10)

        ttk.Button(navigation_frame, text="Exit Application", width=30,
            command=self.controller.exit_app).pack()

        self.apply_cursor(self)

    def on_enter(self):
        self.update_states()

    def update_states(self):
        is_loaded = self.controller.dataset is not None

        self.profile_button.config(state="normal" if is_loaded else "disabled")
        self.dashboard_button.config(state="normal" if is_loaded else "disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if file_path:
            try:
                dataset = load_dataset(file_path)

            except (FileNotFoundError, ValueError, RuntimeError) as error:
                messagebox.showerror("Dataset Loading Failed", str(error))
                return
            
            self.controller.set_dataset(dataset)

            file_name = os.path.basename(file_path)
            self.controller.set_title(file_name)

            self.update_states()
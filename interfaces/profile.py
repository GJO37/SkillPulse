import tkinter as tk
from tkinter import ttk
from interfaces.screen import Screen


class ProfileInterface(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.candidate_name = tk.StringVar()
        self.candidate_id = tk.StringVar()

        self.build_content()
        self.setup_traces()
        
    def build_content(self):
        button_frame = ttk.Frame(self.top_frame)
        button_frame.grid(row=0, column=0, pady=10)

        self.create_button = ttk.Button(button_frame, text="Create Profile", width=25)
        self.create_button.pack(side="left", padx=20)

        self.export_button = ttk.Button(button_frame, text="Export Profile", width=25)
        self.export_button.pack(side="left", padx=20)

        self.clear_button = ttk.Button(button_frame, text="Clear Profile", width=25, command=self.clear_profile)
        self.clear_button.pack(side="left", padx=20)

        self.profile_frame = ttk.Frame(self.bottom_frame, borderwidth=2, relief="groove")
        self.profile_frame.grid(row=0, column=0, sticky="nsew", padx=120, pady=10)
        self.profile_frame.columnconfigure(0, weight=1)
        self.profile_frame.rowconfigure(0, weight=1)

        navigation_frame = ttk.Frame(self.bottom_frame)
        navigation_frame.grid(row=1, column=0, pady=10)

        ttk.Button(navigation_frame, text="Return to Home", width=30,
            command=lambda: self.controller.show_frame("HomeInterface")).pack()

        self.candidate_page()

        self.apply_cursor(self)

    def candidate_page(self):
        self.candidate_frame = ttk.Frame(self.profile_frame)

        candidate_frame = self.candidate_frame
        candidate_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        candidate_frame.columnconfigure(0, weight=1)
        candidate_frame.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(candidate_frame)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Candidate Profile").grid(row=0, column=0, sticky="w")
        ttk.Label(header_frame, text="Page 1 of 3").grid(row=0, column=1, sticky="e")

        content_frame = ttk.Frame(candidate_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", pady=30)
        content_frame.columnconfigure(1, weight=1)

        ttk.Label(content_frame, text="Candidate Name").grid(row=0, column=0, sticky="w", padx=20, pady=15)
        self.name_entry = ttk.Entry(content_frame, textvariable=self.candidate_name)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=20, pady=15)

        ttk.Label(content_frame, text="Candidate ID").grid(row=1, column=0, sticky="w", padx=20, pady=15)
        self.id_entry = ttk.Entry(content_frame, textvariable=self.candidate_id)
        self.id_entry.grid(row=1, column=1, sticky="ew", padx=20, pady=15)

        navigation_frame = ttk.Frame(candidate_frame)
        navigation_frame.grid(row=2, column=0, sticky="e")
        navigation_frame.columnconfigure(0, weight=1)

        self.candidate_next = ttk.Button(navigation_frame, text="Next", width=20)
        self.candidate_next.pack()

    def on_enter(self):
        self.update_states()

    def on_exit(self):
        self.clear_profile()

    def setup_traces(self):
        self.candidate_name.trace_add("write", self.update_states)
        self.candidate_id.trace_add("write", self.update_states)
     
    def update_states(self, *args):
        has_name = bool(self.name_entry.get().strip())
        has_id = bool(self.id_entry.get().strip())

        has_details = has_name and has_id
        has_anything = has_name or has_id

        self.create_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.clear_button.config(state="normal" if has_anything else "disabled")
        self.candidate_next.config(state="normal" if has_details else "disabled")

    def clear_profile(self):
        self.candidate_name.set("")
        self.candidate_id.set("")

        self.candidate_frame.tkraise()
        self.update_states()
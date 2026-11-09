
import os
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import Screen
from functions.loader import load_dataset


class HomeInterface(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.build_content()
        self.update_states()

    def build_content(self):
        button_frame = ttk.Frame(self.top_frame)
        button_frame.grid(row=0, column=0, pady=10)

        self.browse_button = ttk.Button(button_frame, text="Browse Dataset", width=25,
            command=self.browse_file)
        self.browse_button.pack(side="left", padx=20)

        self.profile_button = ttk.Button(button_frame, text="Create Profile", width=25,
            command=lambda: self.controller.show_frame("ProfileInterface"))
        self.profile_button.pack(side="left", padx=20)

        self.dashboard_button = ttk.Button(button_frame, text="Intelligence Dashboard", width=25,
            command=lambda: self.controller.show_frame("DashboardInterface"))
        self.dashboard_button.pack(side="left", padx=20)

        preview_frame = ttk.Frame(self.bottom_frame, borderwidth=2, relief="groove")
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=120, pady=10)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(preview_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=20)
        header_frame.columnconfigure(0, weight=1)

        ttk.Label(header_frame, text="Dataset Preview").grid(row=0, column=0, sticky="w")
        self.header_label = ttk.Label(header_frame, text="No dataset loaded")
        self.header_label.grid(row=0, column=1, sticky="e")

        table_frame = ttk.Frame(preview_frame, borderwidth=2, relief="solid")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=(10, 40))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.table_preview = ttk.Treeview(table_frame, columns=("job_title", "skillset"),
            show="headings", selectmode="none")

        self.table_preview.heading("job_title", text="Job Title")
        self.table_preview.heading("skillset", text="Skillset")
        self.table_preview.grid(row=0, column=0, sticky="nsew")        

        self.table_preview.bind("<Button-1>", lambda event: "break"
            if self.table_preview.identify_region(event.x, event.y)
            in ("separator", "heading", "cell", "tree") else None)
        
        scrollbar = ttk.Scrollbar(table_frame, command=self.table_preview.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table_preview.configure(yscrollcommand=scrollbar.set)

        navigation_frame = ttk.Frame(self.bottom_frame)
        navigation_frame.grid(row=1, column=0, pady=10)
        navigation_frame.columnconfigure(0, weight=1)

        ttk.Button(navigation_frame, text="Exit Application", width=30,
            command=self.controller.exit_app).pack()

        self.apply_cursor(self)

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

            self.display_preview()
            self.update_states()

    def display_preview(self):
        dataset = self.controller.dataset

        unique_skills = {
            skill 
            for role_skills in dataset.values() 
            for skill in role_skills
        }

        self.header_label.config(
            text=f"{len(dataset)} job titles & {len(unique_skills)} unique skills")
        
        self.table_preview.delete(*self.table_preview.get_children())

        for role, skills in dataset.items():
            self.table_preview.insert("", "end",
                values=(role, ", ".join(skills)))
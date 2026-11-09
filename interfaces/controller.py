
import tkinter as tk
from tkinter import ttk


class Controller(tk.Tk):

    def __init__(self, title="SkillPulse", size="1024x768"):
        super().__init__()

        self.current_frame = None

        self.dataset = None
        self.presets = {}

        self.base_title = title
        self.title(self.base_title)

        self.geometry(size)
        self.minsize(1024, 768)

        self.set_style()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.container = container
        self.frames = {}

    def set_dataset(self, dataset):
        self.dataset = dataset
        self.presets.clear()

    def set_title(self, dataset_name=None):
        if dataset_name:
            self.title(f"{self.base_title} | {dataset_name}")
        else:
            self.title(self.base_title)

    def set_style(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=5)
        style.configure("TLabel", font=("Segoe UI", 10))

    def add_frame(self, name, frame_class):
        frame = frame_class(self.container, self)
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        new_frame = self.frames.get(name)

        if not new_frame:
            raise ValueError(f"Frame '{name}' not found")

        if self.current_frame and hasattr(self.current_frame, "on_exit"):
            self.current_frame.on_exit()

        if hasattr(new_frame, "on_enter"):
            new_frame.on_enter()

        new_frame.tkraise()
        self.current_frame = new_frame

    def exit_app(self):
        self.destroy()
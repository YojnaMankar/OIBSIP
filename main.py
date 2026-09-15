"""
BMI Calculator (Advanced) - OASIS INFOBYTE SIP Internship Task 2
Main Graphical User Interface application built with Tkinter, SQLite3, and Matplotlib.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
from datetime import datetime

# Local application modules
from bmi_logic import (
    calculate_bmi,
    get_bmi_category,
    calculate_healthy_weight_range,
    validate_inputs
)
from database import (
    init_db,
    insert_record,
    get_records,
    get_all_users,
    delete_record,
    clear_user_history
)

# Enable high-DPI awareness on Windows if possible
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class BMICalculatorApp(tk.Tk):
    """
    Main Application Window for the Advanced BMI Calculator.
    Provides calculation, SQLite persistence, history viewing, and Matplotlib trend visualization.
    """

    def __init__(self):
        super().__init__()

        self.title("BMI Calculator - OASIS INFOBYTE Task 2")
        self.geometry("960x740")
        self.minsize(860, 640)

        # Apply application-level theme and colors
        self.configure(bg="#f8fafc")

        # Initialize SQLite database
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("Database Initialization Error", f"Failed to initialize SQLite database:\n{str(e)}")

        self._init_styles()
        self._build_header()
        self._build_notebook()
        self._refresh_user_dropdowns()

    def _init_styles(self):
        """Configure modern ttk styles and colors."""
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        font_family = "Segoe UI" if sys.platform == "win32" else "Helvetica"

        style.configure("TNotebook", background="#f8fafc", tabmargins=[10, 10, 10, 0])
        style.configure(
            "TNotebook.Tab",
            font=(font_family, 11, "bold"),
            padding=[16, 8],
            background="#e2e8f0",
            foreground="#334155"
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff"), ("active", "#cbd5e1")],
            foreground=[("selected", "#0f172a"), ("active", "#0f172a")]
        )

        style.configure(
            "Primary.TButton",
            font=(font_family, 10, "bold"),
            background="#2563eb",
            foreground="#ffffff",
            padding=[14, 8],
            borderwidth=0
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1d4ed8"), ("disabled", "#94a3b8")],
            foreground=[("disabled", "#ffffff")]
        )

        style.configure(
            "Secondary.TButton",
            font=(font_family, 10),
            background="#e2e8f0",
            foreground="#1e293b",
            padding=[12, 7],
            borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#cbd5e1")]
        )

        style.configure(
            "Danger.TButton",
            font=(font_family, 10),
            background="#ef4444",
            foreground="#ffffff",
            padding=[12, 7],
            borderwidth=0
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#dc2626")]
        )

        style.configure(
            "Treeview",
            font=(font_family, 10),
            rowheight=28,
            background="#ffffff",
            fieldbackground="#ffffff"
        )
        style.configure(
            "Treeview.Heading",
            font=(font_family, 10, "bold"),
            background="#e2e8f0",
            foreground="#1e293b"
        )

    def _build_header(self):
        """Construct a professional title header banner."""
        header_frame = tk.Frame(self, bg="#0f172a", height=75)
        header_frame.pack(fill="x", side="top")

        content_box = tk.Frame(header_frame, bg="#0f172a")
        content_box.pack(fill="both", expand=True, padx=25, pady=12)

        title_label = tk.Label(
            content_box,
            text="⚖ BMI Calculator",
            font=("Segoe UI", 18, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        title_label.pack(side="left")

        subtitle_label = tk.Label(
            content_box,
            text="OASIS INFOBYTE SIP Internship | Task 2 (Advanced)",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )
        subtitle_label.pack(side="right")

    def _build_notebook(self):
        """Create tabbed navigation for Calculator, History, and Trend Analytics."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab 1: Calculator
        self.tab_calc = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_calc, text="  📊 Calculator  ")
        self._build_calculator_tab(self.tab_calc)

        # Tab 2: History
        self.tab_history = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_history, text="  📋 History  ")
        self._build_history_tab(self.tab_history)

        # Tab 3: Trend Analytics
        self.tab_trend = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.tab_trend, text="  📈 Trend Graph  ")
        self._build_trend_tab(self.tab_trend)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    # -------------------------------------------------------------
    # TAB 1: CALCULATOR
    # -------------------------------------------------------------
    def _build_calculator_tab(self, parent):
        """Build the calculation form and dynamic result cards."""
        container = tk.Frame(parent, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=20, pady=15)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # LEFT CARD: Input Form
        form_card = tk.LabelFrame(
            container,
            text=" User & Body Measurements ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=20,
            pady=15
        )
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        # User Name selection / entry
        tk.Label(
            form_card,
            text="User Name:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(anchor="w", pady=(5, 2))

        user_input_frame = tk.Frame(form_card, bg="#ffffff")
        user_input_frame.pack(fill="x", pady=(0, 12))

        self.user_combo = ttk.Combobox(user_input_frame, font=("Segoe UI", 10))
        self.user_combo.pack(fill="x", side="left", expand=True)
        self.user_combo.set("Yojna")

        # Weight (kg) input
        tk.Label(
            form_card,
            text="Weight (kg):",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(anchor="w", pady=(5, 2))

        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(form_card, textvariable=self.weight_var, font=("Segoe UI", 11))
        weight_entry.pack(fill="x", pady=(0, 3))
        tk.Label(
            form_card,
            text="Example: 68.5  (numeric value in kilograms)",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 12))

        # Height (m) input
        tk.Label(
            form_card,
            text="Height (meters):",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(anchor="w", pady=(5, 2))

        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(form_card, textvariable=self.height_var, font=("Segoe UI", 11))
        height_entry.pack(fill="x", pady=(0, 3))
        tk.Label(
            form_card,
            text="Example: 1.75  (numeric value in meters; 175 cm = 1.75 m)",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 15))

        # Action Buttons
        btn_frame = tk.Frame(form_card, bg="#ffffff")
        btn_frame.pack(fill="x", pady=10)

        calc_btn = ttk.Button(
            btn_frame,
            text="Calculate & Save BMI",
            style="Primary.TButton",
            command=self.handle_calculate
        )
        calc_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        reset_btn = ttk.Button(
            btn_frame,
            text="Reset / Clear",
            style="Secondary.TButton",
            command=self.handle_clear_inputs
        )
        reset_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Standard Reference Categories legend
        ref_frame = tk.LabelFrame(
            form_card,
            text=" WHO BMI Reference Categories ",
            font=("Segoe UI", 9, "bold"),
            bg="#f8fafc",
            fg="#475569",
            padx=10,
            pady=8
        )
        ref_frame.pack(fill="x", pady=(15, 0))

        legend_items = [
            ("Underweight", "< 18.5", "#0284c7"),
            ("Normal Weight", "18.5 – 24.9", "#16a34a"),
            ("Overweight", "25.0 – 29.9", "#d97706"),
            ("Obese", "≥ 30.0", "#dc2626")
        ]
        for name, rng, color in legend_items:
            row = tk.Frame(ref_frame, bg="#f8fafc")
            row.pack(fill="x", pady=2)
            tk.Label(row, text="●", fg=color, font=("Segoe UI", 11, "bold"), bg="#f8fafc").pack(side="left", padx=(0, 4))
            tk.Label(row, text=f"{name}:", font=("Segoe UI", 9, "bold"), fg="#334155", bg="#f8fafc").pack(side="left")
            tk.Label(row, text=f" {rng}", font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").pack(side="left")

        # RIGHT CARD: Result Display Card
        self.result_card = tk.LabelFrame(
            container,
            text=" BMI Result & Health Insights ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=25,
            pady=20
        )
        self.result_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        # Empty initial state prompt
        self.empty_prompt = tk.Label(
            self.result_card,
            text="Enter your name, weight, and height\nthen click 'Calculate & Save BMI'\nto view your result.",
            font=("Segoe UI", 12),
            fg="#94a3b8",
            bg="#ffffff",
            justify="center"
        )
        self.empty_prompt.pack(expand=True, pady=40)

        # Actual result content container (hidden initially)
        self.result_content = tk.Frame(self.result_card, bg="#ffffff")

        self.res_user_lbl = tk.Label(
            self.result_content,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg="#0f172a",
            bg="#ffffff"
        )
        self.res_user_lbl.pack(pady=(0, 5))

        tk.Label(
            self.result_content,
            text="YOUR BODY MASS INDEX",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#ffffff"
        ).pack()

        self.res_bmi_val = tk.Label(
            self.result_content,
            text="--",
            font=("Segoe UI", 36, "bold"),
            fg="#2563eb",
            bg="#ffffff"
        )
        self.res_bmi_val.pack(pady=2)

        self.res_category_badge = tk.Label(
            self.result_content,
            text="Normal",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#16a34a",
            padx=16,
            pady=4
        )
        self.res_category_badge.pack(pady=8)

        # Healthy weight range calculation
        self.res_healthy_range = tk.Label(
            self.result_content,
            text="",
            font=("Segoe UI", 10),
            fg="#334155",
            bg="#ffffff"
        )
        self.res_healthy_range.pack(pady=(5, 10))

        # Advice message box
        self.res_advice = tk.Label(
            self.result_content,
            text="",
            font=("Segoe UI", 10, "italic"),
            fg="#475569",
            bg="#f1f5f9",
            wraplength=340,
            justify="center",
            padx=12,
            pady=12,
            relief="groove"
        )
        self.res_advice.pack(fill="x", pady=10)

        # Quick navigation link buttons
        nav_btns = tk.Frame(self.result_content, bg="#ffffff")
        nav_btns.pack(fill="x", pady=(15, 0))

        view_hist_btn = ttk.Button(
            nav_btns,
            text="View History 📋",
            style="Secondary.TButton",
            command=lambda: self.notebook.select(1)
        )
        view_hist_btn.pack(side="left", expand=True, fill="x", padx=(0, 4))

        view_trend_btn = ttk.Button(
            nav_btns,
            text="View Trend 📈",
            style="Secondary.TButton",
            command=lambda: self.notebook.select(2)
        )
        view_trend_btn.pack(side="left", expand=True, fill="x", padx=(4, 0))

    def handle_calculate(self):
        """Validate inputs, calculate BMI, save to SQLite, and update GUI display."""
        user = self.user_combo.get()
        weight_str = self.weight_var.get()
        height_str = self.height_var.get()

        is_valid, err_msg, parsed = validate_inputs(user, weight_str, height_str)
        if not is_valid:
            messagebox.showerror("Validation Error", err_msg)
            return

        try:
            bmi = calculate_bmi(parsed["weight"], parsed["height"])
            cat_name, cat_color, advice = get_bmi_category(bmi)
            min_w, max_w = calculate_healthy_weight_range(parsed["height"])

            # Persist record in SQLite
            insert_record(
                user_name=parsed["user_name"],
                weight=parsed["weight"],
                height=parsed["height"],
                bmi=bmi,
                category=cat_name
            )

            # Update GUI Result Card
            self.empty_prompt.pack_forget()
            self.result_content.pack(fill="both", expand=True, pady=10)

            self.res_user_lbl.config(text=f"Report for: {parsed['user_name']}")
            self.res_bmi_val.config(text=f"{bmi:.2f}", fg=cat_color)
            self.res_category_badge.config(text=cat_name.upper(), bg=cat_color)
            self.res_healthy_range.config(
                text=f"Healthy Weight Range for {parsed['height']}m: {min_w} kg – {max_w} kg"
            )
            self.res_advice.config(text=f"💡 {advice}")

            # Refresh dropdowns and notify
            self._refresh_user_dropdowns()
            messagebox.showinfo("Success", f"BMI calculated ({bmi:.2f} - {cat_name}) and saved to database successfully!")

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An unexpected error occurred during calculation:\n{str(e)}")

    def handle_clear_inputs(self):
        """Clear calculation inputs and restore empty state."""
        self.weight_var.set("")
        self.height_var.set("")
        self.result_content.pack_forget()
        self.empty_prompt.pack(expand=True, pady=40)

    # -------------------------------------------------------------
    # TAB 2: HISTORY
    # -------------------------------------------------------------
    def _build_history_tab(self, parent):
        """Build historical table view with filtering and record deletion."""
        container = tk.Frame(parent, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # Filter and Control Bar
        toolbar = tk.Frame(container, bg="#ffffff", relief="solid", bd=1, padx=12, pady=10)
        toolbar.pack(fill="x", pady=(0, 10))

        tk.Label(
            toolbar,
            text="Filter by User:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(side="left", padx=(0, 6))

        self.history_user_combo = ttk.Combobox(toolbar, state="readonly", font=("Segoe UI", 10), width=18)
        self.history_user_combo.pack(side="left", padx=(0, 12))
        self.history_user_combo.bind("<<ComboboxSelected>>", lambda e: self.load_history())

        refresh_btn = ttk.Button(toolbar, text="🔄 Refresh", style="Secondary.TButton", command=self.load_history)
        refresh_btn.pack(side="left", padx=(0, 6))

        delete_btn = ttk.Button(toolbar, text="🗑 Delete Selected", style="Danger.TButton", command=self.handle_delete_record)
        delete_btn.pack(side="left", padx=(0, 6))

        clear_all_btn = ttk.Button(toolbar, text="Clear User Records", style="Secondary.TButton", command=self.handle_clear_user_history)
        clear_all_btn.pack(side="left")

        self.history_count_lbl = tk.Label(
            toolbar,
            text="0 records found",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg="#64748b"
        )
        self.history_count_lbl.pack(side="right", padx=6)

        # Table Frame with Scrollbars
        table_frame = tk.Frame(container, bg="#ffffff", relief="solid", bd=1)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "user_name", "weight", "height", "bmi", "category", "date_time")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("user_name", text="User Name")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("height", text="Height (m)")
        self.tree.heading("bmi", text="BMI")
        self.tree.heading("category", text="Category")
        self.tree.heading("date_time", text="Date / Time")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("user_name", width=140, anchor="w")
        self.tree.column("weight", width=100, anchor="center")
        self.tree.column("height", width=100, anchor="center")
        self.tree.column("bmi", width=90, anchor="center")
        self.tree.column("category", width=130, anchor="center")
        self.tree.column("date_time", width=180, anchor="center")

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Row styling tags
        self.tree.tag_configure("Underweight", background="#f0f9ff")
        self.tree.tag_configure("Normal", background="#f0fdf4")
        self.tree.tag_configure("Overweight", background="#fffbeb")
        self.tree.tag_configure("Obese", background="#fef2f2")

    def load_history(self):
        """Fetch records from SQLite and populate the Treeview table."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_user = self.history_user_combo.get()
        filter_user = None if (not selected_user or selected_user == "All Users") else selected_user

        try:
            records = get_records(user_name=filter_user)
            for rec in records:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        rec["id"],
                        rec["user_name"],
                        f"{rec['weight']:.2f}",
                        f"{rec['height']:.2f}",
                        f"{rec['bmi']:.2f}",
                        rec["category"],
                        rec["date_time"]
                    ),
                    tags=(rec["category"],)
                )

            count = len(records)
            user_suffix = f" for '{selected_user}'" if filter_user else ""
            self.history_count_lbl.config(text=f"{count} record{'s' if count != 1 else ''} found{user_suffix}")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to retrieve history records:\n{str(e)}")

    def handle_delete_record(self):
        """Delete selected row from database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a record from the table to delete.")
            return

        values = self.tree.item(selected_item[0], "values")
        record_id = int(values[0])
        user_name = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete record #{record_id} for user '{user_name}'?"
        )
        if confirm:
            try:
                success = delete_record(record_id)
                if success:
                    messagebox.showinfo("Deleted", f"Record #{record_id} deleted successfully.")
                    self.load_history()
                    self._refresh_user_dropdowns()
                else:
                    messagebox.showwarning("Not Found", "Record could not be found or was already deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record:\n{str(e)}")

    def handle_clear_user_history(self):
        """Clear all records for the currently selected user."""
        selected_user = self.history_user_combo.get()
        if not selected_user or selected_user == "All Users":
            messagebox.showwarning("User Selection Required", "Please select a specific user from the filter dropdown first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Clear History",
            f"Are you sure you want to permanently delete ALL records for user '{selected_user}'?"
        )
        if confirm:
            try:
                count = clear_user_history(selected_user)
                messagebox.showinfo("History Cleared", f"Deleted {count} record(s) for user '{selected_user}'.")
                self.load_history()
                self._refresh_user_dropdowns()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history:\n{str(e)}")

    # -------------------------------------------------------------
    # TAB 3: TREND GRAPH (MATPLOTLIB)
    # -------------------------------------------------------------
    def _build_trend_tab(self, parent):
        """Construct the Matplotlib interactive BMI trend visualization tab."""
        container = tk.Frame(parent, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # Top control bar
        control_bar = tk.Frame(container, bg="#ffffff", relief="solid", bd=1, padx=12, pady=10)
        control_bar.pack(fill="x", pady=(0, 10))

        tk.Label(
            control_bar,
            text="Select User for Trend Analytics:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(side="left", padx=(0, 8))

        self.trend_user_combo = ttk.Combobox(control_bar, state="readonly", font=("Segoe UI", 10), width=20)
        self.trend_user_combo.pack(side="left", padx=(0, 12))
        self.trend_user_combo.bind("<<ComboboxSelected>>", lambda e: self.plot_trend_graph())

        plot_btn = ttk.Button(
            control_bar,
            text="📈 Render Trend Graph",
            style="Primary.TButton",
            command=self.plot_trend_graph
        )
        plot_btn.pack(side="left")

        # Graph Container
        self.graph_frame = tk.Frame(container, bg="#ffffff", relief="solid", bd=1)
        self.graph_frame.pack(fill="both", expand=True)

        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor="#ffffff")
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()

    def plot_trend_graph(self):
        """Fetch user BMI history and render Matplotlib line plot with category zones."""
        user = self.trend_user_combo.get()
        self.ax.clear()

        if not user or user == "All Users":
            self.ax.text(
                0.5, 0.5,
                "Please select a specific user from the dropdown\nto view their BMI trend over time.",
                horizontalalignment="center",
                verticalalignment="center",
                transform=self.ax.transAxes,
                fontsize=12,
                color="#64748b"
            )
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.canvas.draw()
            return

        try:
            records = get_records(user_name=user)
            records = sorted(records, key=lambda r: r["date_time"])

            if not records:
                self.ax.text(
                    0.5, 0.5,
                    f"No BMI records found for '{user}'.\nCalculate and save a BMI measurement first!",
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=self.ax.transAxes,
                    fontsize=12,
                    color="#64748b"
                )
                self.ax.set_xticks([])
                self.ax.set_yticks([])
                self.canvas.draw()
                return

            dates = []
            bmis = []
            for r in records:
                try:
                    dt = datetime.strptime(r["date_time"], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    dt = datetime.now()
                dates.append(dt)
                bmis.append(float(r["bmi"]))

            y_min = max(10, min(min(bmis) - 3, 14))
            y_max = max(max(bmis) + 4, 35)

            self.ax.axhspan(0, 18.5, facecolor="#bae6fd", alpha=0.35, label="Underweight (<18.5)")
            self.ax.axhspan(18.5, 24.9, facecolor="#bbf7d0", alpha=0.4, label="Normal (18.5–24.9)")
            self.ax.axhspan(24.9, 29.9, facecolor="#fef08a", alpha=0.4, label="Overweight (25–29.9)")
            self.ax.axhspan(29.9, 100, facecolor="#fecaca", alpha=0.35, label="Obese (≥30.0)")

            self.ax.axhline(18.5, color="#0284c7", linestyle="--", linewidth=0.8)
            self.ax.axhline(24.9, color="#16a34a", linestyle="--", linewidth=0.8)
            self.ax.axhline(30.0, color="#dc2626", linestyle="--", linewidth=0.8)

            if len(dates) == 1:
                self.ax.plot(
                    dates, bmis,
                    marker="o",
                    markersize=10,
                    color="#2563eb",
                    linewidth=2.5,
                    label=f"{user}'s BMI Entry"
                )
                self.ax.annotate(
                    f"{bmis[0]:.2f}",
                    xy=(dates[0], bmis[0]),
                    xytext=(0, 12),
                    textcoords="offset points",
                    ha="center",
                    fontweight="bold",
                    color="#1e293b",
                    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#2563eb", lw=1)
                )
            else:
                self.ax.plot(
                    dates, bmis,
                    marker="o",
                    markersize=7,
                    color="#2563eb",
                    linewidth=2.2,
                    label=f"{user}'s BMI Trend"
                )
                for idx in (0, -1):
                    self.ax.annotate(
                        f"{bmis[idx]:.2f}",
                        xy=(dates[idx], bmis[idx]),
                        xytext=(0, 10),
                        textcoords="offset points",
                        ha="center",
                        fontsize=9,
                        fontweight="bold",
                        color="#1e293b",
                        bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#94a3b8", lw=0.8)
                    )

            self.ax.set_title(f"BMI History Trend for {user}", fontsize=13, fontweight="bold", color="#0f172a", pad=12)
            self.ax.set_xlabel("Date & Time", fontsize=10, fontweight="bold", color="#334155")
            self.ax.set_ylabel("BMI Value (kg/m²)", fontsize=10, fontweight="bold", color="#334155")
            self.ax.set_ylim(y_min, y_max)
            self.ax.grid(True, linestyle=":", alpha=0.6)

            self.fig.autofmt_xdate(rotation=25)
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))

            self.ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Graph Error", f"Failed to plot BMI trend graph:\n{str(e)}")

    # -------------------------------------------------------------
    # HELPERS & SYNC
    # -------------------------------------------------------------
    def _refresh_user_dropdowns(self):
        """Update all user comboboxes across tabs with distinct users from SQLite."""
        try:
            users = get_all_users()
            current_calc_user = self.user_combo.get()
            self.user_combo["values"] = users if users else ["Yojna"]
            if current_calc_user:
                self.user_combo.set(current_calc_user)
            elif users:
                self.user_combo.set(users[0])
            else:
                self.user_combo.set("Yojna")

            history_options = ["All Users"] + users
            prev_hist_sel = self.history_user_combo.get()
            self.history_user_combo["values"] = history_options
            if prev_hist_sel in history_options:
                self.history_user_combo.set(prev_hist_sel)
            else:
                self.history_user_combo.set("All Users")

            self.trend_user_combo["values"] = users
            prev_trend_sel = self.trend_user_combo.get()
            if prev_trend_sel in users:
                self.trend_user_combo.set(prev_trend_sel)
            elif users:
                self.trend_user_combo.set(users[0])
            else:
                self.trend_user_combo.set("")

        except Exception as e:
            print(f"User dropdown sync warning: {e}", file=sys.stderr)

    def _on_tab_changed(self, event):
        """Trigger view reloads when switching tabs."""
        current_tab_idx = self.notebook.index(self.notebook.select())
        if current_tab_idx == 1:
            self.load_history()
        elif current_tab_idx == 2:
            self._refresh_user_dropdowns()
            self.plot_trend_graph()


def main():
    """Application entry point."""
    app = BMICalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()

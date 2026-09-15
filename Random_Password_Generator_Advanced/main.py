"""
Secure Password Generator (Advanced) - OASIS INFOBYTE SIP Internship Task 3
Main Graphical User Interface built with Tkinter, TTK, and Python's `secrets` module (CSPRNG).
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Local generator logic module (strictly uses secrets module)
from password_generator import (
    generate_secure_password,
    evaluate_password_strength,
    CHAR_SETS
)

# Clipboard support with graceful fallback
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# Enable high-DPI awareness on Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class PasswordGeneratorApp(tk.Tk):
    """
    Main Application Window for the Advanced Secure Password Generator.
    Features cryptographic password generation, dynamic strength evaluation,
    and an in-memory session-only history.
    """

    def __init__(self):
        super().__init__()

        self.title("Secure Password Generator - OASIS INFOBYTE Task 3")
        self.geometry("900x720")
        self.minsize(820, 620)
        self.configure(bg="#f8fafc")

        # In-memory session history (strictly ephemeral, never persisted to disk or DB)
        self.session_history = []  # List of tuples: (password, timestamp, strength)

        self._init_styles()
        self._build_header()
        self._build_main_layout()

        # Generate an initial strong password on launch
        self.handle_generate()

    def _init_styles(self):
        """Configure clean TTK styling and fonts."""
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        font_family = "Segoe UI" if sys.platform == "win32" else "Helvetica"

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
            "Success.TButton",
            font=(font_family, 10, "bold"),
            background="#16a34a",
            foreground="#ffffff",
            padding=[14, 8],
            borderwidth=0
        )
        style.map(
            "Success.TButton",
            background=[("active", "#15803d"), ("disabled", "#94a3b8")]
        )

        style.configure(
            "Secondary.TButton",
            font=(font_family, 9),
            background="#e2e8f0",
            foreground="#1e293b",
            padding=[10, 5],
            borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#cbd5e1")]
        )

        style.configure(
            "TCheckbutton",
            font=(font_family, 10),
            background="#ffffff",
            foreground="#1e293b"
        )

    def _build_header(self):
        """Construct a modern header banner."""
        header_frame = tk.Frame(self, bg="#0f172a", height=75)
        header_frame.pack(fill="x", side="top")

        content_box = tk.Frame(header_frame, bg="#0f172a")
        content_box.pack(fill="both", expand=True, padx=25, pady=12)

        title_label = tk.Label(
            content_box,
            text="🔒 Secure Password Generator",
            font=("Segoe UI", 18, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        title_label.pack(side="left")

        subtitle_label = tk.Label(
            content_box,
            text="OASIS INFOBYTE SIP Internship | Task 3 (Advanced)",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )
        subtitle_label.pack(side="right")

    def _build_main_layout(self):
        """Create the responsive split-card layout."""
        main_container = tk.Frame(self, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        main_container.columnconfigure(0, weight=5)
        main_container.columnconfigure(1, weight=6)
        main_container.rowconfigure(0, weight=1)

        # Left Column: Configuration Controls
        left_col = tk.Frame(main_container, bg="#f8fafc")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self._build_options_card(left_col)

        # Right Column: Output, Strength, and Session History
        right_col = tk.Frame(main_container, bg="#f8fafc")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self._build_display_card(right_col)
        self._build_strength_card(right_col)
        self._build_history_card(right_col)

    def _build_options_card(self, parent):
        """Construct the configuration controls card."""
        options_card = tk.LabelFrame(
            parent,
            text=" Password Configuration ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=18,
            pady=16
        )
        options_card.pack(fill="both", expand=True)

        # Length selection header
        len_header = tk.Frame(options_card, bg="#ffffff")
        len_header.pack(fill="x", pady=(0, 5))

        tk.Label(
            len_header,
            text="Password Length (chars):",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(side="left")

        # Synchronized Length Variables
        self.length_var = tk.IntVar(value=16)

        self.spinbox = ttk.Spinbox(
            len_header,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=5,
            font=("Segoe UI", 10, "bold"),
            command=self._sync_slider_from_spinbox
        )
        self.spinbox.pack(side="right")
        self.spinbox.bind("<KeyRelease>", lambda e: self._sync_slider_from_spinbox())

        # Slider (Scale)
        self.scale = ttk.Scale(
            options_card,
            from_=8,
            to=64,
            orient="horizontal",
            variable=self.length_var,
            command=self._sync_spinbox_from_slider
        )
        self.scale.pack(fill="x", pady=(0, 4))

        tk.Label(
            options_card,
            text="Recommended: 16+ characters for strong cryptographic security.",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 16))

        # Character Types Frame
        types_frame = tk.LabelFrame(
            options_card,
            text=" Character Types (Select at least 2) ",
            font=("Segoe UI", 9, "bold"),
            bg="#f8fafc",
            fg="#475569",
            padx=12,
            pady=10
        )
        types_frame.pack(fill="x", pady=(0, 15))

        self.var_upper = tk.BooleanVar(value=True)
        self.var_lower = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=True)
        self.var_exclude_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            types_frame,
            text="Uppercase Letters (A – Z)",
            variable=self.var_upper,
            style="TCheckbutton"
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types_frame,
            text="Lowercase Letters (a – z)",
            variable=self.var_lower,
            style="TCheckbutton"
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types_frame,
            text="Numbers (0 – 9)",
            variable=self.var_digits,
            style="TCheckbutton"
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types_frame,
            text="Special Symbols (! @ # $ % ^ & * ...)",
            variable=self.var_symbols,
            style="TCheckbutton"
        ).pack(anchor="w", pady=3)

        # Ambiguous characters exclusion
        amb_frame = tk.Frame(options_card, bg="#ffffff")
        amb_frame.pack(fill="x", pady=(0, 15))

        ttk.Checkbutton(
            amb_frame,
            text="Exclude Ambiguous Characters (0, O, 1, l, I, |)",
            variable=self.var_exclude_ambiguous,
            style="TCheckbutton"
        ).pack(anchor="w", pady=2)

        tk.Label(
            amb_frame,
            text="Prevents confusion between look-alike glyphs in printed passwords.",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#ffffff"
        ).pack(anchor="w")

        # Primary Action Buttons
        btn_frame = tk.Frame(options_card, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        gen_btn = ttk.Button(
            btn_frame,
            text="⚡ Generate Password",
            style="Primary.TButton",
            command=self.handle_generate
        )
        gen_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        reset_btn = ttk.Button(
            btn_frame,
            text="↺ Reset",
            style="Secondary.TButton",
            command=self.handle_reset
        )
        reset_btn.pack(side="left", padx=(4, 0))

    def _sync_spinbox_from_slider(self, val=None):
        """Update spinbox integer when slider changes."""
        try:
            self.length_var.set(int(float(self.scale.get())))
        except Exception:
            pass

    def _sync_slider_from_spinbox(self):
        """Update slider position when spinbox is edited."""
        try:
            val = self.length_var.get()
            if 8 <= val <= 64:
                self.scale.set(val)
        except Exception:
            pass

    def _build_display_card(self, parent):
        """Construct the generated password display with quick-copy."""
        display_card = tk.LabelFrame(
            parent,
            text=" Generated Password ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=18,
            pady=14
        )
        display_card.pack(fill="x", pady=(0, 10))

        entry_row = tk.Frame(display_card, bg="#ffffff")
        entry_row.pack(fill="x", pady=(0, 6))

        self.password_entry = tk.Entry(
            entry_row,
            font=("Consolas", 15, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
            relief="solid",
            bd=1,
            justify="center"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=6)

        copy_btn = ttk.Button(
            entry_row,
            text="📋 Copy",
            style="Success.TButton",
            command=self.handle_copy
        )
        copy_btn.pack(side="right")

        # Feedback notification label
        self.feedback_lbl = tk.Label(
            display_card,
            text="Ready to copy.",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#ffffff"
        )
        self.feedback_lbl.pack(anchor="w")

    def _build_strength_card(self, parent):
        """Construct the visual strength indicator with color badge and entropy."""
        self.strength_card = tk.LabelFrame(
            parent,
            text=" Password Security Analysis ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=18,
            pady=12
        )
        self.strength_card.pack(fill="x", pady=(0, 10))

        badge_row = tk.Frame(self.strength_card, bg="#ffffff")
        badge_row.pack(fill="x", pady=(0, 6))

        tk.Label(
            badge_row,
            text="Strength Level:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).pack(side="left")

        self.strength_badge = tk.Label(
            badge_row,
            text="STRONG",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#0284c7",
            padx=12,
            pady=2
        )
        self.strength_badge.pack(side="left", padx=8)

        self.entropy_lbl = tk.Label(
            badge_row,
            text="Entropy: -- bits",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#ffffff"
        )
        self.entropy_lbl.pack(side="right")

        # Visual Progress Bar
        self.progress_canvas = tk.Canvas(self.strength_card, height=10, bg="#e2e8f0", highlightthickness=0)
        self.progress_canvas.pack(fill="x", pady=(0, 8))

        # Advice Text
        self.strength_advice_lbl = tk.Label(
            self.strength_card,
            text="",
            font=("Segoe UI", 9),
            fg="#475569",
            bg="#ffffff",
            wraplength=380,
            justify="left"
        )
        self.strength_advice_lbl.pack(anchor="w")

    def _build_history_card(self, parent):
        """Construct the session generation history display (strictly in-memory)."""
        hist_card = tk.LabelFrame(
            parent,
            text=" Session History (Last 5 Passwords) ",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            bd=1,
            padx=18,
            pady=10
        )
        hist_card.pack(fill="both", expand=True)

        tk.Label(
            hist_card,
            text="⚠️ In-memory only. History is securely wiped when the app is closed.",
            font=("Segoe UI", 8, "italic"),
            fg="#64748b",
            bg="#ffffff"
        ).pack(anchor="w", pady=(0, 6))

        self.history_list_frame = tk.Frame(hist_card, bg="#ffffff")
        self.history_list_frame.pack(fill="both", expand=True)

    def _update_history_display(self):
        """Render the last 5 session passwords with timestamp and copy button."""
        for widget in self.history_list_frame.winfo_children():
            widget.destroy()

        if not self.session_history:
            tk.Label(
                self.history_list_frame,
                text="No passwords generated yet.",
                font=("Segoe UI", 9),
                fg="#94a3b8",
                bg="#ffffff"
            ).pack(pady=10)
            return

        for pwd, ts, level, color in reversed(self.session_history[-5:]):
            row = tk.Frame(self.history_list_frame, bg="#f8fafc", relief="solid", bd=1, padx=8, pady=4)
            row.pack(fill="x", pady=2)

            # Dot indicator
            tk.Label(row, text="●", fg=color, font=("Segoe UI", 10, "bold"), bg="#f8fafc").pack(side="left", padx=(0, 5))

            # Masked/preview password
            preview_pwd = pwd if len(pwd) <= 20 else f"{pwd[:18]}..."
            tk.Label(
                row,
                text=preview_pwd,
                font=("Consolas", 10, "bold"),
                fg="#1e293b",
                bg="#f8fafc"
            ).pack(side="left")

            # Timestamp
            tk.Label(
                row,
                text=ts,
                font=("Segoe UI", 8),
                fg="#94a3b8",
                bg="#f8fafc"
            ).pack(side="left", padx=(10, 0))

            # Copy button
            c_btn = ttk.Button(
                row,
                text="Copy",
                style="Secondary.TButton",
                command=lambda p=pwd: self._copy_history_password(p)
            )
            c_btn.pack(side="right")

    def handle_generate(self):
        """Validate options and generate a cryptographically secure password."""
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Invalid Length", "Password length must be an integer between 8 and 64.")
            return

        if length < 8:
            messagebox.showerror("Invalid Length", "Password length must be at least 8 characters.")
            return

        u = self.var_upper.get()
        l = self.var_lower.get()
        d = self.var_digits.get()
        s = self.var_symbols.get()
        amb = self.var_exclude_ambiguous.get()

        try:
            password = generate_secure_password(
                length=length,
                use_upper=u,
                use_lower=l,
                use_digits=d,
                use_symbols=s,
                exclude_ambiguous=amb
            )

            # Update entry
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.feedback_lbl.config(
                text=f"Generated {length}-char password using secrets module (CSPRNG).",
                fg="#16a34a"
            )

            # Evaluate strength
            # Approximate pool size
            pool_sz = (26 if u else 0) + (26 if l else 0) + (10 if d else 0) + (len(CHAR_SETS['symbols']) if s else 0)
            level, score, color, advice, entropy = evaluate_password_strength(password, pool_size=max(pool_sz, 2))

            # Update strength card
            self.strength_badge.config(text=level.upper(), bg=color)
            self.entropy_lbl.config(text=f"Entropy: {entropy} bits")
            self.strength_advice_lbl.config(text=advice)

            # Draw progress bar
            self.progress_canvas.delete("all")
            self.update_idletasks()
            c_w = self.progress_canvas.winfo_width()
            fill_w = max(4, int(c_w * (score / 100.0)))
            self.progress_canvas.create_rectangle(0, 0, fill_w, 10, fill=color, outline="")

            # Add to session history
            now_ts = datetime.now().strftime("%H:%M:%S")
            self.session_history.append((password, now_ts, level, color))
            self._update_history_display()

        except ValueError as ve:
            messagebox.showwarning("Validation Warning", str(ve))
        except Exception as e:
            messagebox.showerror("Generation Error", f"Failed to generate password:\n{str(e)}")

    def handle_copy(self):
        """Copy active password to Windows clipboard with visual confirmation."""
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showwarning("No Password", "No password available to copy. Please generate one first.")
            return

        copied = False
        # 1. Try pyperclip
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(password)
                copied = True
            except Exception:
                copied = False

        # 2. Graceful fallback to Tkinter clipboard
        if not copied:
            try:
                self.clipboard_clear()
                self.clipboard_append(password)
                self.update()
                copied = True
            except Exception as e:
                messagebox.showerror("Clipboard Error", f"Failed to copy to clipboard:\n{str(e)}")
                return

        if copied:
            self.feedback_lbl.config(text="✔ Password copied to clipboard!", fg="#16a34a")
            messagebox.showinfo("Success", "Password copied to clipboard.")

    def _copy_history_password(self, pwd: str):
        """Copy a password from the session history list."""
        copied = False
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(pwd)
                copied = True
            except Exception:
                copied = False

        if not copied:
            try:
                self.clipboard_clear()
                self.clipboard_append(pwd)
                self.update()
                copied = True
            except Exception as e:
                messagebox.showerror("Clipboard Error", f"Failed to copy to clipboard:\n{str(e)}")
                return

        if copied:
            self.feedback_lbl.config(text="✔ History password copied to clipboard!", fg="#16a34a")
            messagebox.showinfo("Copied", "History password copied to clipboard.")

    def handle_reset(self):
        """Reset controls to default recommended settings."""
        self.length_var.set(16)
        self.scale.set(16)
        self.var_upper.set(True)
        self.var_lower.set(True)
        self.var_digits.set(True)
        self.var_symbols.set(True)
        self.var_exclude_ambiguous.set(False)
        self.feedback_lbl.config(text="Settings reset to defaults.", fg="#64748b")
        self.handle_generate()


def main():
    """Application entry point."""
    app = PasswordGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()

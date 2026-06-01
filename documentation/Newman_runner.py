import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# Paleta de colores profesional
BG_PRIMARY = "#1e1e2f"
BG_SECONDARY = "#2a2a3b"
BG_ENTRY = "#2d2d3f"
ACCENT = "#5a67d8"
ACCENT_HOVER = "#6b79e8"
SUCCESS = "#48bb78"
ERROR = "#f56565"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#cbd5e0"
BORDER = "#3f3f55"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_FIELD = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_LOG = ("Consolas", 9)


class NewmanRunnerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Newman Runner — Postman Automation")
        self.geometry("780x620")
        self.resizable(False, False)
        self.configure(bg=BG_PRIMARY)

        self.collection_path = tk.StringVar()
        self.environment_path = tk.StringVar()
        self.output_folder_name = tk.StringVar(value="newman-report")
        self.status_text = tk.StringVar(value="Ready")
        self.running = False

        self._build_ui()

    def _build_ui(self):
        # Header (línea de acento)
        header = tk.Frame(self, bg=ACCENT, height=4)
        header.pack(fill="x")

        # Título
        title_frame = tk.Frame(self, bg=BG_PRIMARY)
        title_frame.pack(fill="x", padx=35, pady=(20, 10))

        tk.Label(
            title_frame,
            text="Newman Runner",
            font=FONT_TITLE,
            bg=BG_PRIMARY,
            fg=TEXT_PRIMARY
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Run Postman collections with environment",
            font=FONT_SUBTITLE,
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY
        ).pack(anchor="w")

        # Separador
        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x", padx=35, pady=(5, 15))

        # Frame principal
        main_frame = tk.Frame(self, bg=BG_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=35, pady=(0, 15))

        # Campo Colección
        self._crear_campo(
            main_frame,
            label="Postman Collection",
            hint="JSON file (required)",
            variable=self.collection_path,
            command=self._browse_collection,
            row=0
        )

        # Campo Environment
        self._crear_campo(
            main_frame,
            label="Postman Environment",
            hint="JSON file (required)",
            variable=self.environment_path,
            command=self._browse_environment,
            row=1
        )

        # Configuración salida
        output_frame = tk.LabelFrame(
            main_frame,
            text="HTML Report",
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY,
            font=FONT_FIELD,
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        output_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=15, padx=2)
        output_frame.columnconfigure(0, weight=1)

        tk.Label(
            output_frame,
            text="Output folder:",
            font=FONT_FIELD,
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        folder_entry = tk.Entry(
            output_frame,
            textvariable=self.output_folder_name,
            font=FONT_FIELD,
            bg=BG_ENTRY,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER
        )
        folder_entry.grid(row=1, column=0, sticky="ew", ipady=5, padx=10, pady=(0, 10))

        # Botones
        btn_frame = tk.Frame(main_frame, bg=BG_PRIMARY)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.run_btn = self._crear_boton(
            btn_frame,
            text="RUN NEWMAN",
            bg=ACCENT,
            fg=TEXT_PRIMARY,
            command=self._run_newman,
            side="left",
            padx=25
        )

        self._crear_boton(
            btn_frame,
            text="CLEAR",
            bg=BG_SECONDARY,
            fg=TEXT_SECONDARY,
            command=self._clear_fields,
            side="left",
            padx=20
        )

        # Consola
        log_frame = tk.LabelFrame(
            main_frame,
            text="Execution Log",
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY,
            font=FONT_FIELD,
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        log_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=(
                10,
                5),
            padx=2)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_box = tk.Text(
            log_frame,
            font=FONT_LOG,
            bg=BG_SECONDARY,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            state="disabled",
            wrap="word",
            padx=8,
            pady=8
        )
        self.log_box.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.log_box, command=self.log_box.yview)
        self.log_box.configure(yscrollcommand=scrollbar.set)

        # Barra de estado
        status_bar = tk.Frame(self, bg=BG_SECONDARY, pady=6)
        status_bar.pack(fill="x", side="bottom")

        self.status_indicator = tk.Label(
            status_bar,
            text="●",
            font=("Segoe UI", 12),
            bg=BG_SECONDARY,
            fg=SUCCESS
        )
        self.status_indicator.pack(side="left", padx=(20, 5))

        tk.Label(
            status_bar,
            textvariable=self.status_text,
            font=FONT_FIELD,
            bg=BG_SECONDARY,
            fg=TEXT_SECONDARY
        ).pack(side="left")

        # Ajuste de expansión
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def _crear_campo(self, parent, label, hint, variable, command, row):
        frame = tk.Frame(parent, bg=BG_PRIMARY)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=8, padx=2)
        frame.columnconfigure(0, weight=1)

        tk.Label(
            frame,
            text=label,
            font=FONT_FIELD,
            bg=BG_PRIMARY,
            fg=TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", pady=(0, 2))

        tk.Label(
            frame,
            text=hint,
            font=("Segoe UI", 8),
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY
        ).grid(row=1, column=0, sticky="w", pady=(0, 5))

        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=FONT_FIELD,
            bg=BG_ENTRY,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER
        )
        entry.grid(row=2, column=0, sticky="ew", ipady=5, padx=(0, 8))

        btn = tk.Button(
            frame,
            text="Browse",
            font=FONT_FIELD,
            bg=BG_SECONDARY,
            fg=TEXT_PRIMARY,
            activebackground=BORDER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=2,
            command=command
        )
        btn.grid(row=2, column=1, sticky="e")

    def _crear_boton(self, parent, text, bg, fg, command, side, padx):
        btn = tk.Button(
            parent,
            text=text,
            font=FONT_BUTTON,
            bg=bg,
            fg=fg,
            activebackground=ACCENT_HOVER if bg == ACCENT else BORDER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=padx,
            pady=8,
            command=command
        )
        btn.pack(side=side, padx=6)
        return btn

    def _browse_collection(self):
        path = filedialog.askopenfilename(
            title="Select Postman Collection",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.collection_path.set(path)

    def _browse_environment(self):
        path = filedialog.askopenfilename(
            title="Select Postman Environment",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.environment_path.set(path)

    def _clear_fields(self):
        self.collection_path.set("")
        self.environment_path.set("")
        self.output_folder_name.set("newman-report")
        self._set_log("")
        self._set_status("Ready", SUCCESS)

    def _set_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        if text:
            self.log_box.insert("end", text)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def _append_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def _set_status(self, msg, color=None):
        self.status_text.set(msg)
        if color:
            self.status_indicator.configure(fg=color)

    def _get_newman_command(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform == "win32":
            newman_local = os.path.join(
                script_dir, "node_modules", ".bin", "newman.cmd")
        else:
            newman_local = os.path.join(script_dir, "node_modules", ".bin", "newman")
        if os.path.isfile(newman_local):
            return [newman_local]
        else:
            return ["npx", "newman"]

    def _validate_inputs(self):
        if not self.collection_path.get():
            messagebox.showerror("Error", "Collection file is required.")
            return False
        if not os.path.isfile(self.collection_path.get()):
            messagebox.showerror("Error", "Collection file does not exist.")
            return False
        if not self.environment_path.get():
            messagebox.showerror("Error", "Environment file is required.")
            return False
        if not os.path.isfile(self.environment_path.get()):
            messagebox.showerror("Error", "Environment file does not exist.")
            return False
        folder_name = self.output_folder_name.get().strip()
        if not folder_name:
            messagebox.showerror("Error", "Output folder name is required.")
            return False
        invalid_chars = set(r'\/:*?"<>|')
        if any(c in invalid_chars for c in folder_name):
            messagebox.showerror(
                "Error", f"Folder name contains invalid characters: {invalid_chars}")
            return False
        return True

    def _check_newman(self):
        cmd = self._get_newman_command()
        try:
            test_cmd = cmd + ["--version"]
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=10,
                shell=(sys.platform == "win32")
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _run_newman(self):
        if self.running:
            return
        if not self._validate_inputs():
            return
        if not self._check_newman():
            messagebox.showerror(
                "Newman Not Found",
                "Local Newman installation not found.\n\nRun in terminal (in this folder):\n  npm init -y\n  npm install newman newman-reporter-html --save-dev"
            )
            return
        self.running = True
        self.run_btn.configure(state="disabled", text="RUNNING...")
        self._set_log("")
        self._set_status("Executing Newman...", ACCENT)
        threading.Thread(target=self._execute_newman, daemon=True).start()

    def _execute_newman(self):
        collection = self.collection_path.get()
        environment = self.environment_path.get()
        folder_name = self.output_folder_name.get().strip()

        output_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            folder_name)
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "report.html")

        base_cmd = self._get_newman_command()
        cmd = base_cmd + [
            "run", collection,
            "--reporters", "cli,html",
            f"--reporter-html-export={report_path}",
            "-e", environment
        ]

        self.after(0, lambda: self._append_log(f"Output directory: {output_dir}\n"))
        self.after(0, lambda: self._append_log(f"Command: {' '.join(cmd)}\n\n"))

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32")
            )
            for line in process.stdout:
                self.after(0, lambda l=line: self._append_log(l))

            process.wait()
            rc = process.returncode

            if rc == 0:
                self.after(
                    0, lambda: self._set_status(
                        f"Completed - Report: {report_path}", SUCCESS))
                self.after(
                    0, lambda: self._append_log(
                        f"\nHTML report generated: {report_path}\n"))
                self.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Success",
                        f"Newman finished successfully.\n\nReport: {report_path}"))
            else:
                self.after(
                    0, lambda: self._set_status(
                        "Newman finished with errors", ERROR))
                self.after(0, lambda: self._append_log(f"\nExit code: {rc}\n"))
        except Exception as e:
            self.after(0, lambda: self._append_log(f"\nUnexpected error: {e}\n"))
            self.after(0, lambda: self._set_status("Execution error", ERROR))
        finally:
            self.after(0, self._reset_button)

    def _reset_button(self):
        self.running = False
        self.run_btn.configure(state="normal", text="RUN NEWMAN")


if __name__ == "__main__":
    app = NewmanRunnerApp()
    app.mainloop()

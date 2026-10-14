"""Campus Lost & Found Tracker - a beginner-friendly Tkinter application."""

import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk

import database


class LostFoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Lost & Found Tracker")
        self.root.geometry("1120x760")
        self.root.minsize(930, 650)

        database.initialize_database()
        self.selected_report_id = None

        self.setup_styles()
        self.build_interface()
        self.load_reports()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#f4f7fb")
        style.configure("TLabel", background="#f4f7fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#15324b", foreground="white",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Subheader.TLabel", background="#15324b", foreground="#d8e8f5",
                        font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#f4f7fb", foreground="#15324b",
                        font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
        style.configure("Primary.TButton", background="#176b87", foreground="white")
        style.map("Primary.TButton", background=[("active", "#12566d")])
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe", background="#f4f7fb")
        style.configure("TLabelframe.Label", background="#f4f7fb",
                        foreground="#15324b", font=("Segoe UI", 10, "bold"))

    def build_interface(self):
        page = ttk.Frame(self.root, padding=0)
        page.pack(fill="both", expand=True)

        header = tk.Frame(page, bg="#15324b", padx=24, pady=18)
        header.pack(fill="x")
        ttk.Label(header, text="Campus Lost & Found Tracker", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Report misplaced items, search reports, and keep track of returned belongings.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        content = ttk.Frame(page, padding=18)
        content.pack(fill="both", expand=True)

        form = ttk.LabelFrame(content, text="Add a report", padding=12)
        form.pack(fill="x", pady=(0, 14))

        self.report_type = tk.StringVar(value="Lost")
        self.item_name = tk.StringVar()
        self.category = tk.StringVar(value="Other")
        self.location = tk.StringVar()
        self.report_date = tk.StringVar(value=date.today().isoformat())
        self.contact_info = tk.StringVar()

        ttk.Label(form, text="Report type *").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=5)
        type_frame = ttk.Frame(form)
        type_frame.grid(row=0, column=1, sticky="w", padx=(0, 18), pady=5)
        ttk.Radiobutton(type_frame, text="Lost", variable=self.report_type, value="Lost").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(type_frame, text="Found", variable=self.report_type, value="Found").pack(side="left")

        ttk.Label(form, text="Item name *").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(form, textvariable=self.item_name, width=27).grid(row=0, column=3, sticky="ew", padx=(0, 18), pady=5)
        ttk.Label(form, text="Category *").grid(row=0, column=4, sticky="w", padx=(0, 8), pady=5)
        categories = ["Electronics", "ID / Cards", "Books / Notes", "Clothing", "Keys", "Bags", "Water Bottle", "Other"]
        ttk.Combobox(form, textvariable=self.category, values=categories, state="readonly", width=18).grid(row=0, column=5, sticky="ew", pady=5)

        ttk.Label(form, text="Location *").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(form, textvariable=self.location, width=25).grid(row=1, column=1, sticky="ew", padx=(0, 18), pady=5)
        ttk.Label(form, text="Date (YYYY-MM-DD) *").grid(row=1, column=2, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(form, textvariable=self.report_date, width=27).grid(row=1, column=3, sticky="ew", padx=(0, 18), pady=5)
        ttk.Label(form, text="Contact (optional)").grid(row=1, column=4, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(form, textvariable=self.contact_info, width=20).grid(row=1, column=5, sticky="ew", pady=5)

        ttk.Label(form, text="Description *").grid(row=2, column=0, sticky="nw", padx=(0, 8), pady=5)
        self.description = tk.Text(form, height=3, wrap="word", font=("Segoe UI", 10), relief="solid", borderwidth=1)
        self.description.grid(row=2, column=1, columnspan=5, sticky="ew", pady=5)

        button_row = ttk.Frame(form)
        button_row.grid(row=3, column=0, columnspan=6, sticky="e", pady=(8, 0))
        ttk.Button(button_row, text="Clear form", command=self.clear_form).pack(side="right", padx=(8, 0))
        ttk.Button(button_row, text="Add report", style="Primary.TButton", command=self.add_report).pack(side="right")

        for column in (1, 3, 5):
            form.columnconfigure(column, weight=1)

        list_header = ttk.Frame(content)
        list_header.pack(fill="x", pady=(0, 8))
        ttk.Label(list_header, text="Reported items", style="Section.TLabel").pack(side="left")
        self.search_text = tk.StringVar()
        search_box = ttk.Entry(list_header, textvariable=self.search_text, width=30)
        search_box.pack(side="right", padx=(8, 0))
        search_box.bind("<Return>", lambda _event: self.load_reports())
        ttk.Button(list_header, text="Clear search", command=self.clear_search).pack(side="right", padx=(8, 0))
        ttk.Button(list_header, text="Search", command=self.load_reports).pack(side="right")

        table_frame = ttk.Frame(content)
        table_frame.pack(fill="both", expand=True)
        columns = ("id", "type", "item", "category", "location", "date", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "ID", "type": "Type", "item": "Item", "category": "Category",
            "location": "Location", "date": "Date", "status": "Status",
        }
        widths = {"id": 45, "type": 75, "item": 170, "category": 120,
                  "location": 190, "date": 105, "status": 95}
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column], anchor="w")
        self.table.column("id", anchor="center")
        self.table.column("status", anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.show_selected_details)
        self.table.bind("<Double-1>", self.show_full_details)
        self.table.tag_configure("resolved", foreground="#77838e")

        action_row = ttk.Frame(content)
        action_row.pack(fill="x", pady=(10, 5))
        self.status_label = ttk.Label(action_row, text="Select a row to view details.")
        self.status_label.pack(side="left", fill="x", expand=True)
        ttk.Button(action_row, text="Delete selected", command=self.remove_report).pack(side="right", padx=(8, 0))
        ttk.Button(action_row, text="Mark resolved", command=self.resolve_report).pack(side="right")

        note = tk.Label(
            content,
            text="Privacy note: this version stores records only on this computer. Avoid entering sensitive personal information.",
            bg="#f4f7fb", fg="#566575", font=("Segoe UI", 9), anchor="w",
        )
        note.pack(fill="x", pady=(7, 0))

    def add_report(self):
        item_name = self.item_name.get().strip()
        category = self.category.get().strip()
        location = self.location.get().strip()
        date_value = self.report_date.get().strip()
        description = self.description.get("1.0", "end").strip()
        contact_info = self.contact_info.get().strip()

        if not item_name or not category or not location or not date_value or not description:
            messagebox.showwarning("Missing information", "Please fill in all required fields marked with *.")
            return

        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date", "Enter the date in YYYY-MM-DD format, for example 2026-10-14.")
            return

        report = {
            "report_type": self.report_type.get(),
            "item_name": item_name,
            "category": category,
            "location": location,
            "report_date": date_value,
            "description": description,
            "contact_info": contact_info,
        }

        try:
            database.add_report(report)
        except Exception as error:
            messagebox.showerror("Could not save report", f"The report could not be saved.\n\nDetails: {error}")
            return

        self.clear_form()
        self.search_text.set("")
        self.load_reports()
        messagebox.showinfo("Report added", "Your report has been saved successfully.")

    def load_reports(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            reports = database.get_reports(self.search_text.get())
        except Exception as error:
            messagebox.showerror("Database error", f"Could not load reports.\n\nDetails: {error}")
            return

        for report in reports:
            values = (
                report["id"], report["report_type"], report["item_name"],
                report["category"], report["location"], report["report_date"],
                report["status"],
            )
            tags = ("resolved",) if report["status"] == "Resolved" else ()
            self.table.insert("", "end", iid=str(report["id"]), values=values, tags=tags)

        self.status_label.config(text=f"Showing {len(reports)} report(s). Double-click a row to view full details.")

    def selected_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a report from the table first.")
            return None
        try:
            return int(selected[0])
        except ValueError:
            return None

    def resolve_report(self):
        report_id = self.selected_id()
        if report_id is None:
            return
        if database.mark_resolved(report_id):
            self.load_reports()
            self.status_label.config(text=f"Report #{report_id} marked as resolved.")
        else:
            messagebox.showwarning("Report not found", "This report may already have been deleted.")
            self.load_reports()

    def remove_report(self):
        report_id = self.selected_id()
        if report_id is None:
            return
        answer = messagebox.askyesno("Confirm deletion", f"Delete report #{report_id}? This cannot be undone.")
        if not answer:
            return
        if database.delete_report(report_id):
            self.load_reports()
            self.status_label.config(text=f"Report #{report_id} deleted.")
        else:
            messagebox.showwarning("Report not found", "This report may already have been deleted.")
            self.load_reports()

    def show_selected_details(self, _event=None):
        report_id = self.selected_id_silent()
        if report_id is None:
            return
        report = database.get_report(report_id)
        if report:
            short_description = report["description"].replace("\n", " ")
            if len(short_description) > 95:
                short_description = short_description[:92] + "..."
            self.status_label.config(
                text=f"#{report['id']} · {report['report_type']} {report['item_name']} · {report['status']} · {short_description}"
            )

    def show_full_details(self, _event=None):
        report_id = self.selected_id_silent()
        if report_id is None:
            return
        report = database.get_report(report_id)
        if not report:
            return

        details = (
            f"Report ID: {report['id']}\n"
            f"Type: {report['report_type']}\n"
            f"Item: {report['item_name']}\n"
            f"Category: {report['category']}\n"
            f"Location: {report['location']}\n"
            f"Date: {report['report_date']}\n"
            f"Status: {report['status']}\n\n"
            f"Description:\n{report['description']}\n\n"
            f"Optional contact information:\n{report['contact_info'] or 'Not provided'}"
        )
        messagebox.showinfo(f"Details for report #{report_id}", details)

    def selected_id_silent(self):
        selected = self.table.selection()
        if not selected:
            return None
        try:
            return int(selected[0])
        except ValueError:
            return None

    def clear_form(self):
        self.report_type.set("Lost")
        self.item_name.set("")
        self.category.set("Other")
        self.location.set("")
        self.report_date.set(date.today().isoformat())
        self.contact_info.set("")
        self.description.delete("1.0", "end")

    def clear_search(self):
        self.search_text.set("")
        self.load_reports()


def main():
    root = tk.Tk()
    LostFoundApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

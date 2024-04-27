import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog

class CompanyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Company Information Viewer")
        self.geometry("1200x600")

        self.company_data = []
        self.filtered_data = []
        self.create_ui()

    def load_company_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                self.company_data = list(reader)
                self.filtered_data = self.company_data
                self.update_treeview()
        except FileNotFoundError:
            print("CSV file not found.")

    def apply_filters(self, name_filter, city_filter, has_website_filter):
        filtered_data = self.company_data

        if name_filter:
            filtered_data = [company for company in filtered_data if name_filter.lower() in company["Name"].lower()]
        if city_filter:
            filtered_data = [company for company in filtered_data if city_filter.lower() in company["Address"].lower()]
        if has_website_filter:
            if has_website_filter.lower() == "yes":
                filtered_data = [company for company in filtered_data if company["Has Website"].lower() == "true"]
            elif has_website_filter.lower() == "no":
                filtered_data = [company for company in filtered_data if company["Has Website"].lower() == "false"]

        self.filtered_data = filtered_data
        self.update_treeview()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for company in self.filtered_data:
            self.tree.insert("", "end", text=company["Name"], values=(
                company["Address"], company["Phone Number"], company["Has Website"], 
                company["Opening Hours"]
            ))

    def create_ui(self):
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10)

        load_button = ttk.Button(filter_frame, text="Load Company Data", command=self.load_company_data_wrapper)
        load_button.grid(row=0, column=0)

        name_label = ttk.Label(filter_frame, text="Company Name:")
        name_label.grid(row=1, column=0)
        self.name_entry = ttk.Entry(filter_frame)
        self.name_entry.grid(row=1, column=1)

        city_label = ttk.Label(filter_frame, text="Address:")
        city_label.grid(row=1, column=2)
        self.city_entry = ttk.Entry(filter_frame)
        self.city_entry.grid(row=1, column=3)

        website_label = ttk.Label(filter_frame, text="Has Website (Yes/No):")
        website_label.grid(row=1, column=4)
        self.website_entry = ttk.Entry(filter_frame)
        self.website_entry.grid(row=1, column=5)

        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters_wrapper)
        filter_button.grid(row=1, column=6)

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Address", "Phone Number", "Has Website", "Opening Hours")
        self.tree.heading("#0", text="Company Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Has Website", text="Has Website")
        self.tree.heading("Opening Hours", text="Opening Hours")

        self.tree.pack(expand=True, fill="both")

    def load_company_data_wrapper(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_company_data(file_path)

    def apply_filters_wrapper(self):
        name_filter = self.name_entry.get()
        address_filter = self.city_entry.get()
        has_website_filter = self.website_entry.get()
        self.apply_filters(name_filter, address_filter, has_website_filter)

if __name__ == "__main__":
    app = CompanyApp()
    app.mainloop()

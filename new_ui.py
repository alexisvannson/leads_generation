import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog
import tkinter.simpledialog as simpledialog

class CompanyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Company Information Viewer")
        self.geometry("1200x800")

        self.business_types = [
            'Local Coffee Shops', 'Boutique Clothing Stores', 'Artisanal Bakeries',
            'Independent Bookstores', 'Vintage Furniture Shops', 'Pet Grooming Salons',
            'Organic Grocery Stores', 'Local Butchers', 'Flower Shops', 'Craft Breweries',
            'Gyms and Fitness Studios', 'Family-Owned Restaurants', 'Homemade Ice Cream Parlors',
            'Handmade Jewelry Stores', 'Interior Design Studios', 'Custom Tailoring Shops',
            'Record Stores', 'Gift Shops', 'Nail Salons', 'Farmers\' Markets Vendors',
            'Yoga Studios', 'Photography Studios', 'Tech Startups', 'Marketing Agencies',
            'Legal Firms', 'Dental Clinics', 'Architectural Firms', 'Educational Institutions',
            'Art Galleries', 'Music Schools'
        ]
        self.company_data = []
        self.filtered_data = []
        self.create_ui()

    def load_company_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                self.company_data = [{**row, 'Contact Status': 'Not contacted'} for row in reader]
                self.filtered_data = self.company_data
                self.update_treeview()
        except FileNotFoundError:
            print("CSV file not found.")

    def apply_filters(self, name_filter, city_filter, business_type_filter, phone_number_filter):
        filtered_data = self.company_data

        if name_filter:
            filtered_data = [company for company in filtered_data if name_filter.lower() in company["Name"].lower()]
        if city_filter:
            filtered_data = [company for company in filtered_data if city_filter.lower() in company["Address"].lower()]
        if business_type_filter:
            filtered_data = [company for company in filtered_data if business_type_filter.lower() in company.get("Business Type", "").lower()]
        if phone_number_filter:
            filtered_data = [company for company in filtered_data if phone_number_filter in company.get("Phone Number", "")]

        self.filtered_data = filtered_data
        self.update_treeview()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for company in self.filtered_data:
            has_website = company.get("Has Website", "no").lower() == "yes"
            self.tree.insert("", "end", iid=company["Name"], text=company["Name"], values=(
                company.get("Address", ""), 
                company.get("Phone Number", ""), 
                "Yes" if has_website else "No", 
                company.get("Opening Hours", ""),
                company.get("Contact Status", "Not contacted")
            ))

    def create_ui(self):
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10, fill='x', expand=True)

        # Row 0: Business Type and Phone Number
        business_type_label = ttk.Label(filter_frame, text="Business Type:")
        business_type_label.grid(row=0, column=0, sticky='e')
        self.business_type_combobox = ttk.Combobox(filter_frame, values=self.business_types, state="readonly")
        self.business_type_combobox.grid(row=0, column=1, sticky='ew')

        phone_label = ttk.Label(filter_frame, text="Phone Number:")
        phone_label.grid(row=0, column=2, sticky='e')
        self.phone_entry = ttk.Entry(filter_frame)
        self.phone_entry.grid(row=0, column=3, sticky='ew')

        # Row 1: Name and City
        name_label = ttk.Label(filter_frame, text="Company Name:")
        name_label.grid(row=1, column=0, sticky='e')
        self.name_entry = ttk.Entry(filter_frame)
        self.name_entry.grid(row=1, column=1, sticky='ew')

        city_label = ttk.Label(filter_frame, text="City:")
        city_label.grid(row=1, column=2, sticky='e')
        self.city_entry = ttk.Entry(filter_frame)
        self.city_entry.grid(row=1, column=3, sticky='ew')

        # Load and Filter Buttons
        load_button = ttk.Button(filter_frame, text="Load Company Data", command=self.load_company_data_wrapper)
        load_button.grid(row=0, column=4, rowspan=2, sticky='ew')
        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters_wrapper)
        filter_button.grid(row=0, column=5, rowspan=2, sticky='ew')

        # Treeview
        self.tree = ttk.Treeview(self, columns=("Address", "Phone Number", "Has Website", "Opening Hours", "Contact Status"), selectmode='browse')
        self.tree.heading("#0", text="Company Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Has Website", text="Has Website")
        self.tree.heading("Opening Hours", text="Opening Hours")
        self.tree.heading("Contact Status", text="Contact Status")
        self.tree.pack(expand=True, fill="both")

        # Edit Contact Status by double-clicking
        self.tree.bind('<Double-1>', self.edit_contact_status)

    def load_company_data_wrapper(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_company_data(file_path)

    def apply_filters_wrapper(self):
        self.apply_filters(
            name_filter=self.name_entry.get(),
            city_filter=self.city_entry.get(),
            business_type_filter=self.business_type_combobox.get(),
            phone_number_filter=self.phone_entry.get()
        )

    def edit_contact_status(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region == 'cell':
            item_id = self.tree.selection()[0]
            column = self.tree.identify_column(event.x)
            if column == '#5':  # Contact Status column
                current_value = self.tree.item(item_id, 'values')[4]
                new_status = simpledialog.askstring("Update Status", "Enter the new contact status:", initialvalue=current_value)
                if new_status:
                    self.tree.set(item_id, column=4, value=new_status)
                    # Update data structure
                    for company in self.company_data:
                        if company["Name"] == item_id:
                            company["Contact Status"] = new_status
                            break

if __name__ == "__main__":
    app = CompanyApp()
    app.mainloop()

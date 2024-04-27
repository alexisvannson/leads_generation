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

    def apply_filters(self, name_filter, city_filter, business_type_filter, phone_number_filter,contact_status_filter):
        filtered_data = self.company_data

        if name_filter:
            filtered_data = [company for company in filtered_data if name_filter.lower() in company["Name"].lower()]
        if city_filter:
            filtered_data = [company for company in filtered_data if city_filter.lower() in company["Address"].lower()]
        if business_type_filter:
            filtered_data = [company for company in filtered_data if business_type_filter.lower() in company.get("Business Type", "").lower()]
        if phone_number_filter:
            filtered_data = [company for company in filtered_data if phone_number_filter in company.get("Phone Number", "")]
        if contact_status_filter:
            filtered_data = [company for company in filtered_data if contact_status_filter.lower() == company.get("Contact Status", "").lower()]

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
            # Main frame for filters
        filter_frame = ttk.Frame(self, padding="3 3 12 12")
        filter_frame.pack(fill='x', expand=True)

        # Configuring the grid layout manager
        filter_frame.columnconfigure(0, weight=1)
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(2, weight=1)
        filter_frame.columnconfigure(3, weight=1)
        filter_frame.columnconfigure(4, weight=1)
        filter_frame.columnconfigure(5, weight=1)

        # Adding widgets to the filter_frame
        ttk.Label(filter_frame, text="Filters", font=('Helvetica', 16)).grid(column=0, row=0, columnspan=6)

        ttk.Label(filter_frame, text="Business Type:").grid(column=0, row=1, sticky='e')
        self.business_type_combobox = ttk.Combobox(filter_frame, values=self.business_types, state="readonly")
        self.business_type_combobox.grid(column=1, row=1, sticky='ew')

        ttk.Label(filter_frame, text="Phone Number:").grid(column=2, row=1, sticky='e')
        self.phone_entry = ttk.Entry(filter_frame)
        self.phone_entry.grid(column=3, row=1, sticky='ew')

        ttk.Label(filter_frame, text="Company Name:").grid(column=0, row=2, sticky='e')
        self.name_entry = ttk.Entry(filter_frame)
        self.name_entry.grid(column=1, row=2, sticky='ew')

        ttk.Label(filter_frame, text="City:").grid(column=2, row=2, sticky='e')
        self.city_entry = ttk.Entry(filter_frame)
        self.city_entry.grid(column=3, row=2, sticky='ew')

        ttk.Label(filter_frame, text="Contact Status:").grid(column=4, row=1, sticky='e')
        self.contact_status_entry = ttk.Entry(filter_frame)
        self.contact_status_entry.grid(column=5, row=1, sticky='ew')

        load_button = ttk.Button(filter_frame, text="Load Company Data", command=self.load_company_data_wrapper)
        load_button.grid(column=4, row=2, sticky='ew')

        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filters_wrapper)
        filter_button.grid(column=5, row=2, sticky='ew')

        save_button = ttk.Button(filter_frame, text="Save Changes", command=self.save_company_data)
        save_button.grid(column=6, row=2, sticky='ew')


        # Treeview for displaying data
        self.tree = ttk.Treeview(self, columns=("Address", "Phone Number", "Has Website", "Opening Hours", "Contact Status"), selectmode='browse')
        self.tree.heading("#0", text="Company Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Has Website", text="Has Website")
        self.tree.heading("Opening Hours", text="Opening Hours")
        self.tree.heading("Contact Status", text="Contact Status")
        self.tree.pack(fill='both', expand=True)

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
            phone_number_filter=self.phone_entry.get(),
            contact_status_filter=self.contact_status_entry.get()
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
    def save_company_data(self):
        with filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files", "*.csv")]) as filename:
            if filename:
                fieldnames = ['Name', 'Address', 'Phone Number', 'Has Website', 'Opening Hours', 'Contact Status']  # Update as needed
                try:
                    with open(filename, 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        for company in self.company_data:
                            writer.writerow(company)
                    print("Data saved successfully.")
                except Exception as e:
                    print(f"Failed to save data: {e}")


if __name__ == "__main__":
    app = CompanyApp()
    app.mainloop()

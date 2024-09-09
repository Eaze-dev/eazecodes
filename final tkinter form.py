import tkinter as tk
from tkinter import ttk, messagebox

# Function to format numbers with commas and two decimal places
def format_currency(amount):
    return f"R{amount:,.2f}"

# Calculate the amortization schedule and Right-of-Use Asset
def calculate_amortization():
    try:
        lease_term = int(lease_term_entry.get())
        annual_payment = float(annual_payment_entry.get())
        residual_payment = float(residual_payment_entry.get())
        interest_rate = float(interest_rate_entry.get()) / 100
        initial_direct_cost = float(initial_direct_cost_entry.get())
        
        # Calculate the initial lease liability
        pv_annual_payments = annual_payment * (1 - (1 + interest_rate) ** -lease_term) / interest_rate
        pv_residual_payment = residual_payment / ((1 + interest_rate) ** lease_term)
        initial_lease_liability = pv_annual_payments + pv_residual_payment

        # Amortization schedule
        schedule = []
        beginning_balance = initial_lease_liability

        for year in range(1, lease_term + 1):
            interest = beginning_balance * interest_rate
            principal = annual_payment - interest
            
            if year < lease_term:
                payment = annual_payment
                ending_balance = beginning_balance - principal
            else:
                payment = principal + interest  # Make sure the final balance equals residual_payment
                ending_balance = residual_payment  # Set the final ending balance to the residual value
            
            schedule.append({
                "Year": year,
                "Beginning Balance": beginning_balance,
                "Payment": payment,
                "Interest": interest,
                "Principal": principal,
                "Ending Balance": ending_balance
            })
            beginning_balance = ending_balance

        right_of_use_asset = initial_lease_liability + initial_direct_cost
        depreciation_per_year = right_of_use_asset / lease_term

        # Calculate subsequent measurements
        depreciation_year_1 = depreciation_per_year
        carrying_amount_year_1 = right_of_use_asset - depreciation_year_1

        depreciation_year_2 = depreciation_per_year
        carrying_amount_year_2 = carrying_amount_year_1 - depreciation_year_2

        # Display the results
        display_results(schedule, right_of_use_asset, depreciation_per_year, 
                        carrying_amount_year_1, carrying_amount_year_2,
                        initial_lease_liability, initial_direct_cost)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Display the amortization schedule and Right-of-Use Asset
def display_results(schedule, right_of_use_asset, depreciation_per_year, 
                    carrying_amount_year_1, carrying_amount_year_2,
                    initial_lease_liability, initial_direct_cost):
    # Clear previous results
    for widget in schedule_frame.winfo_children():
        widget.destroy()
    for widget in asset_frame.winfo_children():
        widget.destroy()

    # Define headers for amortization schedule
    headers = ["Year", "Beginning Balance", "Payment", "Interest", "Principal", "Ending Balance"]
    for col, header in enumerate(headers):
        lbl = tk.Label(schedule_frame, text=header, borderwidth=1, relief="solid", width=15, bg="#d9d9d9")
        lbl.grid(row=0, column=col, sticky="nsew")

    # Populate the schedule
    for row, entry in enumerate(schedule, start=1):
        tk.Label(schedule_frame, text=entry["Year"], borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
        tk.Label(schedule_frame, text=format_currency(entry["Beginning Balance"]), borderwidth=1, relief="solid", width=15).grid(row=row, column=1)
        tk.Label(schedule_frame, text=format_currency(entry["Payment"]), borderwidth=1, relief="solid", width=15).grid(row=row, column=2)
        tk.Label(schedule_frame, text=format_currency(entry["Interest"]), borderwidth=1, relief="solid", width=15).grid(row=row, column=3)
        tk.Label(schedule_frame, text=format_currency(entry["Principal"]), borderwidth=1, relief="solid", width=15).grid(row=row, column=4)
        tk.Label(schedule_frame, text=format_currency(entry["Ending Balance"]), borderwidth=1, relief="solid", width=15).grid(row=row, column=5)

    # Display the Right-of-Use Asset
    tk.Label(asset_frame, text="Initial Recognition:", font=("Arial", 12, "bold")).pack()
    tk.Label(asset_frame, text=f"Lease Liability: {format_currency(initial_lease_liability)}").pack()
    tk.Label(asset_frame, text=f"Initial Direct Costs: {format_currency(initial_direct_cost)}").pack()
    tk.Label(asset_frame, text=f"Total (Initial Recognition): {format_currency(right_of_use_asset)}").pack()
    
    tk.Label(asset_frame, text="Subsequent Measurement:", font=("Arial", 12, "bold")).pack()
    tk.Label(asset_frame, text=f"Depreciation per Year: {format_currency(depreciation_per_year)}").pack()
    tk.Label(asset_frame, text=f"Carrying Amount (Dec Year 1): {format_currency(carrying_amount_year_1)}").pack()
    tk.Label(asset_frame, text=f"Depreciation (Year 2): {format_currency(depreciation_per_year)}").pack()
    tk.Label(asset_frame, text=f"Carrying Amount (Dec Year 2): {format_currency(carrying_amount_year_2)}").pack()

# Create the main window
root = tk.Tk()
root.title("Lease Amortization Schedule and Right-of-Use Asset")
root.geometry("800x600")
root.resizable(True, True)

# Create a frame for input fields
input_frame = tk.LabelFrame(root, text="Lease Details", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="x")

# Lease term input
tk.Label(input_frame, text="Lease Term (Years):").grid(row=0, column=0, sticky="w")
lease_term_entry = tk.Entry(input_frame)
lease_term_entry.grid(row=0, column=1, padx=10, pady=5)

# Annual payment input
tk.Label(input_frame, text="Annual Lease Payment (R):").grid(row=1, column=0, sticky="w")
annual_payment_entry = tk.Entry(input_frame)
annual_payment_entry.grid(row=1, column=1, padx=10, pady=5)

# Residual payment input
tk.Label(input_frame, text="Residual Value Guarantee (R):").grid(row=2, column=0, sticky="w")
residual_payment_entry = tk.Entry(input_frame)
residual_payment_entry.grid(row=2, column=1, padx=10, pady=5)

# Interest rate input
tk.Label(input_frame, text="Interest Rate (%):").grid(row=3, column=0, sticky="w")
interest_rate_entry = tk.Entry(input_frame)
interest_rate_entry.grid(row=3, column=1, padx=10, pady=5)

# Initial direct cost input
tk.Label(input_frame, text="Initial Direct Costs (R):").grid(row=4, column=0, sticky="w")
initial_direct_cost_entry = tk.Entry(input_frame)
initial_direct_cost_entry.grid(row=4, column=1, padx=10, pady=5)

# Button to calculate the schedule
calculate_button = tk.Button(input_frame, text="Calculate", command=calculate_amortization)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Create a canvas for scrolling
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a frame inside the canvas to hold all content
scrollable_frame = tk.Frame(canvas)

# Add the frame to the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Update the scrollregion of the canvas whenever the frame changes size
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scrollregion)

# Create a frame for the amortization schedule inside the scrollable frame
schedule_frame = tk.LabelFrame(scrollable_frame, text="Amortization Schedule", padx=10, pady=10)
schedule_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Create a frame for the Right-of-Use Asset inside the scrollable frame
asset_frame = tk.LabelFrame(scrollable_frame, text="Right-of-Use Asset", padx=10, pady=10)
asset_frame.pack(padx=10, pady=10, fill="x")

# Run the application
root.mainloop()

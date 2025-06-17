# Copyright (c) 2025 Manoel-Ferreira-V-Del-Piero-Rodrigues
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

import tkinter as tk
from tkinter import ttk, messagebox

# --- Conversion factors and formulas ---

unit_categories = {
    "Length": {
        "base": "Meters",
        "units": {
            "Meters": 1.0,
            "Kilometers": 1000.0,
            "Centimeters": 0.01,
            "Millimeters": 0.001,
            "Miles": 1609.34,
            "Yards": 0.9144,
            "Feet": 0.3048,
            "Inches": 0.0254,
        }
    },
    "Weight": {
        "base": "Kilograms",
        "units": {
            "Kilograms": 1.0,
            "Grams": 0.001,
            "Milligrams": 0.000001,
            "Pounds": 0.453592,
            "Ounces": 0.0283495,
            "Tonnes": 1000.0,
        }
    },
    "Temperature": {
        "units": [
            "Celsius",
            "Fahrenheit",
            "Kelvin"
        ]
    },
    "Area": {
        "base": "Square meters",
        "units": {
            "Square meters": 1.0,
            "Square kilometers": 1e6,
            "Square centimeters": 0.0001,
            "Square millimeters": 0.000001,
            "Square miles": 2.59e6,
            "Square yards": 0.836127,
            "Square feet": 0.092903,
            "Square inches": 0.00064516,
            "Hectares": 10000.0,
            "Acres": 4046.86,
        }
    },
    "Volume": {
        "base": "Liters",
        "units": {
            "Liters": 1.0,
            "Milliliters": 0.001,
            "Cubic meters": 1000.0,
            "Cubic centimeters": 0.001,
            "Cubic inches": 0.0163871,
            "Cubic feet": 28.3168,
            "Gallons (US)": 3.78541,
            "Quarts (US)": 0.946353,
            "Pints (US)": 0.473176,
            "Cups (US)": 0.236588,
            "Fluid ounces (US)": 0.0295735,
        }
    },
    "Speed": {
        "base": "Meters/second",
        "units": {
            "Meters/second": 1.0,
            "Kilometers/hour": 0.277778,
            "Miles/hour": 0.44704,
            "Feet/second": 0.3048,
            "Knots": 0.514444,
        }
    },
    "Time": {
        "base": "Seconds",
        "units": {
            "Seconds": 1.0,
            "Minutes": 60.0,
            "Hours": 3600.0,
            "Days": 86400.0,
            "Milliseconds": 0.001,
            "Microseconds": 0.000001,
        }
    },
    "Pressure": {
        "base": "Pascals",
        "units": {
            "Pascals": 1.0,
            "Bar": 100000,
            "Atmospheres": 101325,
            "PSI": 6894.76,
            "mmHg": 133.322,
        }
    }
}

# --- Conversion logic ---

def convert():
    category = category_var.get()
    unit_from = unit_from_var.get()
    unit_to = unit_to_var.get()
    value_str = value_var.get().strip()
    try:
        value = float(value_str)
    except ValueError:
        result_var.set("Please enter a valid number.")
        result_entry.config(foreground="#d7263d")
        return

    if unit_from == unit_to:
        result_var.set("Please select different units.")
        result_entry.config(foreground="#d7263d")
        return

    # Temperature conversion needs special handling
    if category == "Temperature":
        temp = value
        # Convert FROM source to Celsius
        if unit_from == "Celsius":
            temp_c = temp
        elif unit_from == "Fahrenheit":
            temp_c = (temp - 32) * 5/9
        elif unit_from == "Kelvin":
            temp_c = temp - 273.15
        else:
            result_var.set("Unsupported temperature unit.")
            return
        # Convert FROM Celsius to destination
        if unit_to == "Celsius":
            result = temp_c
        elif unit_to == "Fahrenheit":
            result = temp_c * 9/5 + 32
        elif unit_to == "Kelvin":
            result = temp_c + 273.15
        else:
            result_var.set("Unsupported temperature unit.")
            return
        result_var.set(f"{value} {unit_from} = {result:.4f} {unit_to}")
        result_entry.config(foreground="#218380")
        return

    # Standard conversion using base unit
    cat_info = unit_categories[category]
    units = cat_info["units"]
    base = cat_info["base"]
    to_base = value * units[unit_from]       # Convert to base unit
    result = to_base / units[unit_to]        # Convert from base to target unit
    result_var.set(f"{value} {unit_from} = {result:.6g} {unit_to}")
    result_entry.config(foreground="#218380")

def update_units(*args):
    category = category_var.get()
    result_var.set("")
    value_var.set("")
    if category == "Temperature":
        unit_list = unit_categories[category]["units"]
    else:
        unit_list = list(unit_categories[category]["units"].keys())
    unit_from_menu['values'] = unit_list
    unit_to_menu['values'] = unit_list
    unit_from_var.set(unit_list[0])
    unit_to_var.set(unit_list[1])

def clear_fields():
    value_var.set("")
    result_var.set("")
    update_units()
    result_entry.config(foreground="#22223b")

def on_unit_change(*args):
    if unit_from_var.get() == unit_to_var.get():
        convert_btn.state(['disabled'])
        result_var.set("Please select different units.")
        result_entry.config(foreground="#d7263d")
    else:
        convert_btn.state(['!disabled'])
        result_var.set("")
        result_entry.config(foreground="#22223b")

def validate_input(P):
    # Only allow numeric input, including decimal points and minus sign for temperature
    if P == "" or P.replace('-', '', 1).replace('.', '', 1).isdigit():
        return True
    return False

# --- GUI setup ---

root = tk.Tk()
root.title("MetVerter - Unit Converter")
root.resizable(False, False)

# --- Colors and styles ---
BG = "#e8e0d5"
ACCENT = "#967114"
TITLE = "#02466A"
BTN = "#226F82"
BTN_TXT = "#f5f5f5"
ENTRY_BG = "#fff"
RESULT_BG = "#f1faee"
RESULT_TXT = "#22223b"

root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, font=("Roboto", 11))
style.configure("TButton", background=BTN, foreground=BTN_TXT, font=("Roboto", 11, "bold"))
style.map("TButton", background=[('active', ACCENT)])
style.configure("TCombobox", fieldbackground=ENTRY_BG, background=BG, font=("Roboto", 11))

main_frame = ttk.Frame(root, padding="22 16 22 16")
main_frame.grid(row=0, column=0)

category_var = tk.StringVar(value="Length")
unit_from_var = tk.StringVar()
unit_to_var = tk.StringVar()
value_var = tk.StringVar()
result_var = tk.StringVar()

# Title
title_lbl = ttk.Label(
    main_frame, 
    text="MetVerter", 
    font=("Roboto", 20, "bold"), 
    background=BG, 
    foreground=TITLE
)
title_lbl.grid(row=0, column=0, columnspan=9, pady=(0, 22))

# Category dropdown
ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=5)
category_menu = ttk.Combobox(main_frame, textvariable=category_var, values=list(unit_categories.keys()), state="readonly", width=20)
category_menu.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)
category_menu.bind("<<ComboboxSelected>>", update_units)

# From/To units
ttk.Label(main_frame, text="From:").grid(row=2, column=0, sticky="w", pady=5)
unit_from_menu = ttk.Combobox(main_frame, textvariable=unit_from_var, state="readonly", width=20)
unit_from_menu.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)
unit_from_var.trace('w', on_unit_change)

ttk.Label(main_frame, text="To:").grid(row=3, column=0, sticky="w", pady=5)
unit_to_menu = ttk.Combobox(main_frame, textvariable=unit_to_var, state="readonly", width=20)
unit_to_menu.grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)
unit_to_var.trace('w', on_unit_change)

# Value entry with validation
vcmd = (root.register(validate_input), '%P')
ttk.Label(main_frame, text="Value:").grid(row=4, column=0, sticky="w", pady=5)
value_entry = ttk.Entry(main_frame, textvariable=value_var, validate="key", validatecommand=vcmd, width=22, font=("Roboto", 12), background=ENTRY_BG)
value_entry.grid(row=4, column=1, columnspan=2, sticky="ew", pady=5, padx=(0, 0))

# Convert and clear buttons
convert_btn = ttk.Button(main_frame, text="Convert", command=convert)
convert_btn.grid(row=5, column=1, sticky="ew", pady=16, padx=(0, 6))
clear_btn = ttk.Button(main_frame, text="Clear", command=clear_fields)
clear_btn.grid(row=5, column=2, sticky="ew", pady=16)

# Result display (colorful!)
ttk.Label(main_frame, text="Result:").grid(row=6, column=0, sticky="w", pady=5)
result_entry = tk.Entry(main_frame, textvariable=result_var, state="readonly", width=46, font=("Roboto", 12, "bold"),
                      bg=RESULT_BG, fg=RESULT_TXT, relief="flat", borderwidth=4,
                      readonlybackground=RESULT_BG)
result_entry.grid(row=6, column=1, columnspan=2, sticky="ew", pady=8)

update_units()
value_entry.focus()

main_frame.config(borderwidth=3, relief="ridge")
root.mainloop()
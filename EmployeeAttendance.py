import tkinter as tk
import pandas as pd
from datetime import datetime

# Create the main window
root = tk.Tk()
root.title("Employee Attendance System")
root.geometry("800x500")  # Adjust the size

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Create main container
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create frames (layers)
frames = {}
for frame_name in ["main", "employees", "excel_sheet", "complaints"]:
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    frames[frame_name] = frame

# Main menu frame
title_label = tk.Label(frames["main"], text="The Club", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

button_frame = tk.Frame(frames["main"])
button_frame.pack(side="top", anchor="ne", padx=20, pady=20)

tk.Button(button_frame, text="الموظفين", font=("Arial", 10), width=10, command=lambda: show_frame(frames["employees"])).pack(pady=2)
tk.Button(button_frame, text="شيت الاكسل", font=("Arial", 10), width=10, command=lambda: show_frame(frames["excel_sheet"])).pack(pady=2)
tk.Button(button_frame, text="شكاوي", font=("Arial", 10), width=10, command=lambda: show_frame(frames["complaints"])).pack(pady=2)

# Employee frame
tk.Label(frames["employees"], text="Employee Management", font=("Arial", 20)).pack(pady=20)
employee_entry = tk.Entry(frames["employees"])
employee_entry.pack(pady=5)
tk.Button(frames["employees"], text="Add Employee", command=lambda: add_employee(employee_entry.get())).pack(pady=5)

attendance_data = []
employee_list = []

# Dropdown menu for employees
selected_employee = tk.StringVar(frames["employees"])
selected_employee.set("Select Employee")

def update_dropdown():
    menu = employee_dropdown["menu"]
    menu.delete(0, "end")
    for name in employee_list:
        menu.add_command(label=name, command=lambda value=name: selected_employee.set(value))

employee_dropdown = tk.OptionMenu(frames["employees"], selected_employee, "Select Employee")
employee_dropdown.pack(pady=5)

attendance_box = tk.Listbox(frames["employees"], width=50)
attendance_box.pack(pady=10)

def add_employee(name):
    if name and name not in employee_list:
        employee_list.append(name)
        update_dropdown()

def mark_attendance(status):
    employee = selected_employee.get()
    if employee != "Select Employee":
        current_time = datetime.now().strftime("%I:%M %p, %d-%m-%Y")
        if status == "Start":
            attendance_data.append({"Employee": employee, "Start": current_time, "End": ""})
            attendance_box.insert(tk.END, f"{employee} - {current_time}")
        elif status == "End":
            for i, entry in enumerate(attendance_data):
                if entry["Employee"] == employee and entry["End"] == "":
                    attendance_data[i]["End"] = current_time
                    attendance_box.delete(i)
                    break

tk.Button(frames["employees"], text="Start Attendance", command=lambda: mark_attendance("Start")).pack(pady=5)
tk.Button(frames["employees"], text="End Attendance", command=lambda: mark_attendance("End")).pack(pady=5)
tk.Button(frames["employees"], text="Back", command=lambda: show_frame(frames["main"])).pack()

# Excel sheet frame
def save_to_excel():
    df = pd.DataFrame(attendance_data)
    df.to_excel("attendance.xlsx", index=False)

tk.Label(frames["excel_sheet"], text="Excel Sheet", font=("Arial", 20)).pack(pady=20)
tk.Button(frames["excel_sheet"], text="Save to Excel", command=save_to_excel).pack(pady=5)
tk.Button(frames["excel_sheet"], text="Back", command=lambda: show_frame(frames["main"])).pack()

# Complaints frame
tk.Label(frames["complaints"], text="Complaints", font=("Arial", 20)).pack(pady=20)
tk.Button(frames["complaints"], text="Back", command=lambda: show_frame(frames["main"])).pack()

# Show the main frame initially
show_frame(frames["main"])

# Run the application
root.mainloop()

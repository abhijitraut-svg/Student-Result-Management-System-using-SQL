import tkinter as tk
from tkinter import messagebox
import mysql.connector

#Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhijit@123",
    database="student_db"
)
cursor = conn.cursor()

#Functions
def add_student():
    roll = roll_entry.get()
    name = name_entry.get()
    marks = marks_entry.get()

    if not roll or not name or not marks:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    try:
        roll = int(roll)
        marks = float(marks)
    except ValueError:
        messagebox.showerror("Error", "Roll must be number, Marks must be numeric!")
        return

    try:
        cursor.execute("INSERT INTO students (roll_no, name, marks) VALUES (%s, %s, %s)", (roll, name, marks))
        conn.commit()
        messagebox.showinfo("Success", f"Student {name} added successfully!")
        show_students()
        clear_fields()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")

def show_students():
    text_box.delete("1.0", tk.END)
    cursor.execute("SELECT * FROM students ORDER BY roll_no ASC")
    rows = cursor.fetchall()
    if not rows:
        text_box.insert(tk.END, "No student records found!\n")
        return
    for row in rows:
        text_box.insert(tk.END, f"Roll: {row[0]} | Name: {row[1]} | Marks: {row[2]}\n")

def search_student():
    roll = search_entry.get()
    if not roll:
        messagebox.showwarning("Warning", "Enter Roll No to search")
        return

    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll,))
    result = cursor.fetchone()
    text_box.delete("1.0", tk.END)
    if result:
        text_box.insert(tk.END, f" Found: Roll: {result[0]} | Name: {result[1]} | Marks: {result[2]}\n")
    else:
        text_box.insert(tk.END, " Student not found!\n")

def update_student():
    roll = roll_entry.get()
    marks = marks_entry.get()

    if not roll or not marks:
        messagebox.showwarning("Warning", "Enter Roll No and new Marks to update!")
        return

    try:
        roll = int(roll)
        marks = float(marks)
    except ValueError:
        messagebox.showerror("Error", "Invalid input!")
        return

    cursor.execute("UPDATE students SET marks=%s WHERE roll_no=%s", (marks, roll))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Updated", f"Marks updated for Roll {roll}")
        show_students()
    else:
        messagebox.showerror("Error", "No student found with that Roll No.")

def delete_student():
    roll = delete_entry.get()
    if not roll:
        messagebox.showwarning("Warning", "Enter Roll No to delete")
        return

    cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", f"Student with Roll {roll} deleted.")
        show_students()
    else:
        messagebox.showerror("Error", "No student found with that Roll No.")

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    delete_entry.delete(0, tk.END)

def clear_all_records():
    cursor.execute("DELETE FROM students")
    conn.commit()
    messagebox.showinfo("Cleared", "All records deleted!")
    show_students()

#GUI Setup
root = tk.Tk()
root.title("Student Result Management System")
root.geometry("700x600")
root.config(bg="#f0f8ff")

title = tk.Label(root, text="Student Result Management System", font=("Arial", 16, "bold"), bg="#004080", fg="white")
title.pack(fill=tk.X, pady=5)

# Add Frame
add_frame = tk.Frame(root, bg="#f0f8ff")
add_frame.pack(pady=10)

tk.Label(add_frame, text="Roll No:", bg="#f0f8ff", font=("Arial", 11)).grid(row=0, column=0)
roll_entry = tk.Entry(add_frame, width=10)
roll_entry.grid(row=0, column=1, padx=5)

tk.Label(add_frame, text="Name:", bg="#f0f8ff", font=("Arial", 11)).grid(row=0, column=2)
name_entry = tk.Entry(add_frame, width=15)
name_entry.grid(row=0, column=3, padx=5)

tk.Label(add_frame, text="Marks:", bg="#f0f8ff", font=("Arial", 11)).grid(row=0, column=4)
marks_entry = tk.Entry(add_frame, width=10)
marks_entry.grid(row=0, column=5, padx=5)

tk.Button(add_frame, text="Add", command=add_student, bg="#0066cc", fg="white").grid(row=0, column=6, padx=5)
tk.Button(add_frame, text="Update", command=update_student, bg="#33cc33", fg="white").grid(row=0, column=7, padx=5)

# Search Section
search_frame = tk.Frame(root, bg="#f0f8ff")
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search Roll No:", bg="#f0f8ff", font=("Arial", 11)).pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=10)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_student, bg="#800080", fg="white").pack(side=tk.LEFT, padx=5)

# Delete Section
delete_frame = tk.Frame(root, bg="#f0f8ff")
delete_frame.pack(pady=10)
tk.Label(delete_frame, text="Delete Roll No:", bg="#f0f8ff", font=("Arial", 11)).pack(side=tk.LEFT)
delete_entry = tk.Entry(delete_frame, width=10)
delete_entry.pack(side=tk.LEFT, padx=5)
tk.Button(delete_frame, text="Delete", command=delete_student, bg="#ff3333", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(delete_frame, text="Clear All Records", command=clear_all_records, bg="#ff9966", fg="black").pack(side=tk.LEFT, padx=10)

# Display Section
text_box = tk.Text(root, width=80, height=15, wrap="word", font=("Courier New", 10))
text_box.pack(pady=10)

tk.Button(root, text="Show All Students", command=show_students, bg="#009999", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, bg="#cc0000", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

root.mainloop()

#Close Database
cursor.close()
conn.close()
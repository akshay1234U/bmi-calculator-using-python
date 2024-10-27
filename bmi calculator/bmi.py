import tkinter as tk
from tkinter import messagebox
import json
import datetime
import matplotlib.pyplot as plt


def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100 
        bmi = round(weight / (height ** 2), 2)
        bmi_result_label.config(text=f"Your BMI: {bmi}")
        save_bmi(bmi)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for weight and height.")


def save_bmi(bmi):
    user_id = user_id_entry.get()
    if not user_id:
        messagebox.showerror("Error", "Please enter a user ID.")
        return
    
   
    bmi_data = load_bmi_data()
    if user_id not in bmi_data:
        bmi_data[user_id] = []
    
    bmi_data[user_id].append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bmi": bmi
    })
    
    with open("bmi_data.json", "w") as file:
        json.dump(bmi_data, file)
    
    messagebox.showinfo("Success", "BMI saved successfully!")
    view_history()


def load_bmi_data():
    try:
        with open("bmi_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def view_history():
    user_id = user_id_entry.get()
    bmi_data = load_bmi_data()
    
    if user_id in bmi_data:
        history_text.delete(1.0, tk.END) 
        history_text.insert(tk.END, f"Date and BMI for user {user_id}:\n\n")
        for record in bmi_data[user_id]:
            history_text.insert(tk.END, f"{record['date']}: {record['bmi']}\n")
    else:
        messagebox.showerror("Error", "No data found for this user.")


def show_bmi_trends():
    user_id = user_id_entry.get()
    bmi_data = load_bmi_data()

    if user_id in bmi_data:
        dates = [datetime.datetime.strptime(record['date'], "%Y-%m-%d %H:%M:%S") for record in bmi_data[user_id]]
        bmi_values = [record['bmi'] for record in bmi_data[user_id]]

        plt.figure(figsize=(8, 5))
        plt.plot(dates, bmi_values, marker='o', linestyle='-', color='b')
        plt.title(f"BMI Trends for User {user_id}")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "No data available to plot.")


app = tk.Tk()
app.title("BMI Calculator")
app.geometry("500x600")


tk.Label(app, text="User ID:").pack(pady=5)
user_id_entry = tk.Entry(app)
user_id_entry.pack()

tk.Label(app, text="Height (in cm):").pack(pady=5)
height_entry = tk.Entry(app)
height_entry.pack()


tk.Label(app, text="Weight (in kg):").pack(pady=5)
weight_entry = tk.Entry(app)
weight_entry.pack()


calculate_button = tk.Button(app, text="Calculate BMI", command=calculate_bmi)
calculate_button.pack(pady=10)


bmi_result_label = tk.Label(app, text="Your BMI will appear here.", font=("Arial", 14))
bmi_result_label.pack(pady=10)


view_history_button = tk.Button(app, text="View History", command=view_history)
view_history_button.pack(pady=10)


history_text = tk.Text(app, height=10, width=50)
history_text.pack(pady=10)


show_trends_button = tk.Button(app, text="Show BMI Trends", command=show_bmi_trends)
show_trends_button.pack(pady=10)

app.mainloop()

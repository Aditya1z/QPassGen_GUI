import tkinter as tk
from tkinter import messagebox
import pyperclip
from qpassgen_engine import generate_password_info, show_distribution

root = tk.Tk()
root.title("QPassGen")
root.geometry("430x320")
root.configure(bg="#2d2d2d")

pwd = tk.StringVar()
entropy = tk.StringVar()
crack = tk.StringVar()
strength = tk.StringVar()
last_data = {}

def check_strength(data):
    sc = 0
    if data['has_upper']:
        sc += 1
    if data['has_lower']:
        sc += 1
    if data['has_digit']:
        sc += 1
    if data['has_special']:
        sc += 1
    if data['length'] >= 12 and sc >= 3 and data['entropy'] > 60:
        return "Strong"
    if data['length'] >= 10 and sc >= 2:
        return "moderate"
    return "Weak"

def gen_pwd():
    try:
        info = generate_password_info()
        pwd.set(info["password"])
        entropy.set(str(round(info["entropy"], 2)) + " bits")
        crack.set(f"{info['crack_time']:.2e} yrs")
        strength.set(check_strength(info))
        global last_data
        last_data = info["counts"]
    except Exception as e:
        messagebox.showerror("error", str(e))

def copy_pwd():
    pyperclip.copy(pwd.get())
    messagebox.showinfo("copied", "password copied")

def show_graph():
    if last_data:
        show_distribution(last_data)

tk.Label(root, text="QPassGen", font=("Arial", 16), fg="white", bg="#2d2d2d").pack(pady=10)
tk.Label(root, text="Quantum Password Tool", font=("Arial", 9), fg="lightgrey", bg="#2d2d2d").pack()

e = tk.Entry(root, textvariable=pwd, font=("Consolas", 12), width=34, justify="center", bd=0, bg="#fff")
e.pack(pady=12, ipady=4)

f = tk.Frame(root, bg="#2d2d2d")
f.pack(pady=5)
tk.Button(f, text="Generate", width=10, command=gen_pwd).grid(row=0, column=0, padx=5)
tk.Button(f, text="Copy", width=10, command=copy_pwd).grid(row=0, column=1, padx=5)
tk.Button(f, text="Graph", width=10, command=show_graph).grid(row=0, column=2, padx=5)

def stat(label, var):
    tk.Label(root, text=label + ":", font=("Arial", 9), fg="white", bg="#2d2d2d").pack()
    tk.Label(root, textvariable=var, font=("Arial", 10), fg="white", bg="#2d2d2d").pack(pady=2)

stat("Entropy", entropy)
stat("Crack time", crack)
stat("Strength", strength)

tk.Label(root, text="Made by Aditya Raj", font=("Arial", 8), fg="#888", bg="#2d2d2d").pack(side="bottom", pady=10)

root.mainloop()

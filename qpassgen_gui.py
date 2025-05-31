import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import os
from qpassgen_engine import generate_password_info, show_distribution

root = tk.Tk()
root.title("QPassGen - Quantum Password Generator")
root.geometry("560x540")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

icon_path = os.path.join(os.path.dirname(__file__), "qpassgen.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 10), padding=6, background="#3b3f53", foreground="white")
style.configure("TLabel", background="#1e1e2e", foreground="white")
style.configure("TFrame", background="#1e1e2e")
style.configure("TProgressbar", troughcolor="#2a2d3e", background="#4ade80", thickness=14)
style.map("TButton", background=[("active", "#4ade80")], foreground=[("active", "#000000")])

password_var = tk.StringVar()
entropy_var = tk.StringVar()
crack_time_var = tk.StringVar()
strength_var = tk.StringVar()
latest_counts = {}

def animate_output(text, i=0):
    if i < len(text):
        output_box.delete(0, tk.END)
        output_box.insert(0, text[:i+1])
        root.after(40, lambda: animate_output(text, i+1))

def update_strength_bar(score):
    progress["value"] = score * 25
    colors = ["#ef4444", "#facc15", "#4ade80"]
    strength_color = colors[min(score - 1, 2)] if score > 0 else "#ef4444"
    style.configure("TProgressbar", background=strength_color)

def analyze_strength(info):
    score = sum([info['has_upper'], info['has_lower'], info['has_digit'], info['has_special']])
    update_strength_bar(score)
    if info["length"] >= 12 and score >= 3 and info["entropy"] > 60:
        return "🟢 Strong"
    elif info["length"] >= 10 and score >= 2:
        return "🟡 Moderate"
    else:
        return "🔴 Weak"

def generate():
    try:
        info = generate_password_info()
        animate_output(info["password"])
        entropy_var.set(f"{info['entropy']:.2f} bits")
        crack_time_var.set(f"{info['crack_time']:.2e} years")
        strength_var.set(analyze_strength(info))
        global latest_counts
        latest_counts = info["counts"]
        output_box.configure(fg="#60a5fa")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_password():
    pyperclip.copy(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def show_graph():
    if latest_counts:
        show_distribution(latest_counts)

tk.Label(root, text="🔐 QPassGen", font=("Segoe UI", 20, "bold"), bg="#1e1e2e", fg="#4ade80").pack(pady=(20, 5))
tk.Label(root, text="Quantum Secure Password Generator", font=("Segoe UI", 11), bg="#1e1e2e", fg="#cbd5e1").pack(pady=(0, 12))

output_box = tk.Entry(root, textvariable=password_var, font=("Consolas", 14), width=36, justify='center', bd=1, relief="flat", bg="#2a2d3e", fg="#60a5fa", insertbackground="#ffffff")
output_box.pack(pady=12, ipady=6)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=8)
ttk.Button(btn_frame, text="🔁 Generate", command=generate).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="📋 Copy", command=copy_password).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="📊 Quantum Graph", command=show_graph).grid(row=0, column=2, padx=10)

tk.Label(root, text="Password Strength", font=("Segoe UI", 10), bg="#1e1e2e", fg="#cbd5e1").pack(pady=(12, 0))
progress = ttk.Progressbar(root, orient="horizontal", length=360, mode="determinate")
progress.pack(pady=6)

def add_stat(label, var):
    ttk.Label(root, text=label + ":", font=("Segoe UI", 10, "bold")).pack()
    ttk.Label(root, textvariable=var, font=("Segoe UI", 11), foreground="white").pack(pady=3)

add_stat("🧠 Entropy", entropy_var)
add_stat("⏳ Crack Time", crack_time_var)
add_stat("🔎 Strength", strength_var)

tk.Label(root, text="🧠 Made by Aditya Raj • Powered by Qiskit", font=("Segoe UI", 9), bg="#1e1e2e", fg="#777").pack(side="bottom", pady=16)

root.mainloop()

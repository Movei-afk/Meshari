import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import winreg
import sys
import ctypes

def disable_pointer_precision():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\Mouse', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "MouseSpeed", 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(key, "MouseThreshold1", 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(key, "MouseThreshold2", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)
        return "✅ Pointer Precision disabled"
    except:
        return "❌ Failed to disable pointer precision"

def set_high_performance_power_plan():
    try:
        subprocess.run('powercfg /setactive SCHEME_MIN', shell=True)
        return "⚡ Power plan set to High Performance"
    except:
        return "❌ Failed to set power plan"

def set_game_priority(process_name):
    try:
        subprocess.run(f'powershell "Get-Process {process_name} | ForEach-Object {{ $_.PriorityClass = \'High\' }}"', shell=True)
        return f"🎮 Game '{process_name}' priority set to High"
    except:
        return f"❌ Failed to set priority for {process_name}"

def add_to_startup():
    file_path = sys.argv[0]
    name = "MouseBoostStartup"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)
    return "📌 Added to startup"

def boost():
    result1 = disable_pointer_precision()
    result2 = set_high_performance_power_plan()
    result3 = set_game_priority(entry_game.get())
    messagebox.showinfo("Boost Done", f"{result1}\n{result2}\n{result3}\n\n✅ تأكد أن الماوس يدعم 1000Hz أو أكثر من السوفتوير الرسمي")

def enable_startup():
    msg = add_to_startup()
    messagebox.showinfo("Startup Enabled", msg)

# واجهة GUI
root = tk.Tk()
root.title("🎯 Mouse + FPS Booster")
root.geometry("420x300")
root.configure(bg="#1e1e2f")

tk.Label(root, text="🎮 اسم اللعبة (مثلاً: arma3_x64)", bg="#1e1e2f", fg="white", font=("Segoe UI", 10)).pack(pady=(20,5))
entry_game = tk.Entry(root, font=("Segoe UI", 12), justify="center")
entry_game.insert(0, "arma3_x64")  # يمكنك تغييره حسب لعبتك
entry_game.pack(pady=5)

tk.Button(root, text="🚀 Boost Now", font=("Segoe UI", 12), command=boost, bg="#4CAF50", fg="white", width=20).pack(pady=15)

tk.Button(root, text="🧷 تفعيل التشغيل التلقائي", font=("Segoe UI", 10), command=enable_startup, bg="#607D8B", fg="white", width=25).pack(pady=5)

tk.Label(root, text="🖱️ تأكد أن الماوس يدعم 1000Hz أو أكثر من الإعدادات الرسمية", bg="#1e1e2f", fg="#aaaaaa", font=("Segoe UI", 9)).pack(pady=20)

root.mainloop()

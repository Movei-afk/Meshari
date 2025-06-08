import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import psutil
import json
import threading
import time
import re
import socket
import requests
import urllib.request

vpn_process = None
selected_ovpn = None
selected_game = None
fields_locked = False
credentials_file = "credentials.txt"
config_file = "config.json"
ping_host = None
stop_ping = False
ip_info_label = None
o_vpn_type = ""
vpn_connected_time = None
vpn_timer_running = False

def check_openvpn_installed():
    openvpn_path = "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe"
    if os.path.exists(openvpn_path):
        return True
    else:
        answer = messagebox.askyesno("OpenVPN Missing", "OpenVPN not found.\nDo you want to download and install it automatically?")
        if answer:
            try:
                url = "https://swupdate.openvpn.org/community/releases/openvpn-install-latest.exe"
                download_path = os.path.join(os.getcwd(), "openvpn-installer.exe")
                messagebox.showinfo("Download", "Downloading OpenVPN installer...")
                urllib.request.urlretrieve(url, download_path)
                subprocess.Popen([download_path])
                messagebox.showinfo("Installer", "Installer launched. Please complete the setup manually.\nThen restart the app.")
            except Exception as e:
                messagebox.showerror("Download Error", f"Could not download OpenVPN:\n{e}")
        else:
            messagebox.showwarning("Missing Dependency", "You need to install OpenVPN manually to continue.")
        return False

def save_config():
    data = {"ovpn": selected_ovpn, "game": selected_game}
    with open(config_file, "w") as f:
        json.dump(data, f)

def load_config():
    global selected_ovpn, selected_game
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            data = json.load(f)
            selected_ovpn = data.get("ovpn", "")
            selected_game = data.get("game", "")
            if selected_ovpn and os.path.exists(selected_ovpn):
                extract_vpn_type(selected_ovpn)
                label_ovpn_name.config(text=f"🔵 {os.path.basename(selected_ovpn)}", fg="green")
                color = "blue" if "TCP" in o_vpn_type or "UDP" in o_vpn_type else "red"
                label_ovpn_type.config(text=f"{o_vpn_type}", fg=color)
                check_auth_requirement(selected_ovpn)
                extract_ping_host(selected_ovpn)

def save_credentials():
    with open(credentials_file, "w") as f:
        f.write(username_entry.get().strip() + "\n")
        f.write(password_entry.get().strip() + "\n")

def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                username_entry.insert(0, lines[0])
                password_entry.insert(0, lines[1])

def is_vpn_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'openvpn.exe' in proc.info['name'].lower():
            return proc.info['pid']
    return None

def kill_vpn_process():
    pid = is_vpn_running()
    if pid:
        try:
            p = psutil.Process(pid)
            p.terminate()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop VPN: {e}")
    return False

def choose_ovpn():
    global selected_ovpn
    path = filedialog.askopenfilename(title="Choose OpenVPN File", filetypes=[("OVPN files", "*.ovpn")])
    if path:
        selected_ovpn = path
        extract_vpn_type(path)
        label_ovpn_name.config(text=f"🔵 {os.path.basename(path)}", fg="green")
        color = "blue" if "TCP" in o_vpn_type or "UDP" in o_vpn_type else "red"
        label_ovpn_type.config(text=f"{o_vpn_type}", fg=color)
        check_auth_requirement(path)
        extract_ping_host(path)
        save_config()

def extract_vpn_type(path):
    global o_vpn_type
    with open(path, "r") as f:
        content = f.read().lower()
        has_tcp = "proto tcp" in content
        has_udp = "proto udp" in content
        if has_tcp and has_udp:
            o_vpn_type = "[TCP + UDP]"
        elif has_tcp:
            o_vpn_type = "[TCP]"
        elif has_udp:
            o_vpn_type = "[UDP]"
        else:
            o_vpn_type = "[Unknown]"

def choose_game():
    global selected_game
    path = filedialog.askopenfilename(title="Choose Game Executable", filetypes=[("Executable files", "*.exe")])
    if path:
        selected_game = path
        messagebox.showinfo("Game", f"Game selected: {os.path.basename(path)}")
        save_config()

def check_auth_requirement(path):
    with open(path, "r") as f:
        content = f.read()
        if "auth-user-pass" in content:
            username_label.pack()
            username_entry.pack()
            password_label.pack()
            password_entry.pack()
            lock_button.pack(pady=5)
        else:
            username_label.pack_forget()
            username_entry.pack_forget()
            password_label.pack_forget()
            password_entry.pack_forget()
            lock_button.pack_forget()

def extract_ping_host(path):
    global ping_host
    with open(path, "r") as f:
        content = f.read()
        match = re.search(r'remote\s+([^\s]+)', content)
        if match:
            ping_host = match.group(1)
            update_ip_info()
        else:
            ping_host = None
            ip_info_label.config(text="🌍 IP Info: Unknown", fg="gray")

def update_ip_info():
    global ping_host
    try:
        ip = socket.gethostbyname(ping_host)
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = response.get("country", "Unknown")
        city = response.get("city", "")
        ip_info_label.config(text=f"🌍 IP: {ip} | {country} {city}", fg="blue")
    except:
        ip_info_label.config(text="🌍 IP Info: Unavailable", fg="gray")

def ping_loop():
    global stop_ping
    while not stop_ping:
        if ping_host:
            try:
                result = subprocess.run(["ping", "-n", "1", ping_host], capture_output=True, text=True)
                match = re.search(r"Average = (\d+)ms", result.stdout)
                if match:
                    ping_value = match.group(1)
                    ping_label.config(text=f"🌐 Ping: {ping_value} ms", fg="green")
                    ping_time_label.config(text=f"📡 {time.strftime('%H:%M:%S')}")
                else:
                    ping_label.config(text="❌ Ping Failed", fg="red")
            except:
                ping_label.config(text="❌ Ping Error", fg="red")
        else:
            ping_label.config(text="⏳ No Host", fg="gray")
        time.sleep(5)

def toggle_lock():
    global fields_locked
    if fields_locked:
        username_entry.config(state="normal")
        password_entry.config(state="normal")
        lock_button.config(text="🔒 Lock")
        fields_locked = False
    else:
        username_entry.config(state="readonly")
        password_entry.config(state="readonly")
        lock_button.config(text="🔓 Unlock")
        fields_locked = True

def connect_vpn():
    global vpn_process, selected_ovpn
    if vpn_process or is_vpn_running():
        messagebox.showinfo("VPN", "Already connected.")
        return

    if not selected_ovpn or not os.path.exists(selected_ovpn):
        messagebox.showerror("Error", "Please select a valid .ovpn file.")
        return

    requires_auth = "auth-user-pass" in open(selected_ovpn, "r").read()

    if requires_auth:
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and Password required.")
            return
        save_credentials()
        with open("userpass.txt", "w") as f:
            f.write(f"{username}\n{password}\n")

    temp_ovpn = "temp.ovpn"
    with open(selected_ovpn, "r") as original, open(temp_ovpn, "w") as modified:
        for line in original:
            if line.strip().startswith("auth-user-pass"):
                continue
            modified.write(line)
        if requires_auth:
            modified.write("\nauth-user-pass userpass.txt\n")

    try:
        vpn_process = subprocess.Popen([
            "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe", "--config", temp_ovpn
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status_label.config(text="🔌 Connecting...", fg="orange")
        root.after(5000, on_connected_launch_game)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start OpenVPN:\n{e}")

def on_connected_launch_game():
    global vpn_process, vpn_connected_time, vpn_timer_running
    if vpn_process and vpn_process.poll() is None:
        status_label.config(text="✅ Connected", fg="green")
        vpn_connected_time = time.time()
        vpn_timer_running = True
        update_vpn_duration()
        launch_game()
    elif is_vpn_running():
        status_label.config(text="✅ Already Connected", fg="green")
        vpn_connected_time = time.time()
        vpn_timer_running = True
        update_vpn_duration()
        launch_game()
    else:
        status_label.config(text="❌ Failed to connect", fg="red")
        vpn_process = None

def update_vpn_duration():
    if vpn_timer_running:
        elapsed = int(time.time() - vpn_connected_time)
        hrs, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        duration_label.config(text=f"⏱️ VPN Duration: {hrs:02}:{mins:02}:{secs:02}")
        root.after(1000, update_vpn_duration)

def launch_game():
    if not selected_game or not os.path.exists(selected_game):
        choose_game()
    else:
        try:
            subprocess.Popen([selected_game])
            messagebox.showinfo("Game", f"Launching: {os.path.basename(selected_game)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch game:\n{e}")

def disconnect_vpn():
    global vpn_process, vpn_timer_running
    if vpn_process:
        vpn_process.terminate()
        vpn_process = None
        status_label.config(text="🔌 Disconnected", fg="gray")
    elif is_vpn_running():
        kill_vpn_process()
        status_label.config(text="🔌 Disconnected", fg="gray")
    else:
        messagebox.showinfo("VPN", "VPN is not running.")

    vpn_timer_running = False
    duration_label.config(text="⏱️ VPN Duration: 00:00:00")

# GUI
root = tk.Tk()
root.title("Meshari Dis: ok.8")
root.geometry("400x530")
root.resizable(False, False)

if not check_openvpn_installed():
    root.destroy()
    exit()
tk.Label(root, text="🎮", font=("Arial", 14)).pack(pady=10)

##tk.Label(root, text="🎮 Meshari Dis: ok.8", font=("Arial", 14)).pack(pady=10)

ovpn_frame = tk.Frame(root)
ovpn_frame.pack()
label_ovpn_name = tk.Label(ovpn_frame, text="🔘 No .ovpn file selected", fg="gray")
label_ovpn_name.pack(side=tk.LEFT)
label_ovpn_type = tk.Label(ovpn_frame, text="", fg="blue")
label_ovpn_type.pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Select OVPN File", command=choose_ovpn).pack(pady=5)
tk.Button(root, text="Select Game EXE", command=choose_game).pack(pady=5)

username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root, width=30)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, width=30, show="*")
lock_button = tk.Button(root, text="🔒 Lock", command=toggle_lock, width=10)

tk.Button(root, text="Connect + Launch Game", command=connect_vpn, width=25).pack(pady=5)
tk.Button(root, text="Disconnect VPN", command=disconnect_vpn, width=25).pack(pady=5)
tk.Button(root, text="🔴 Force Stop VPN", command=kill_vpn_process, fg="red", width=25).pack(pady=5)

status_label = tk.Label(root, text="🔌 Disconnected", fg="gray", font=("Arial", 12))
status_label.pack(pady=10)

ip_info_label = tk.Label(root, text="🌍 IP Info: Waiting...", fg="gray", font=("Arial", 9))
ip_info_label.pack(pady=2)

ping_label = tk.Label(root, text="🌐 Ping: Waiting...", fg="gray", font=("Arial", 10))
ping_label.pack()

ping_time_label = tk.Label(root, text="📡 Last Ping: --:--:--", fg="gray", font=("Arial", 9))
ping_time_label.pack(pady=2)

duration_label = tk.Label(root, text="⏱️ VPN Duration: 00:00:00", fg="blue", font=("Arial", 10))
duration_label.pack(pady=2)

load_config()
load_credentials()

if is_vpn_running():
    if messagebox.askyesno("VPN Running", "VPN is already running. Do you want to stop it?"):
        kill_vpn_process()
        status_label.config(text="🔌 Disconnected", fg="gray")
    else:
        status_label.config(text="✅ Running", fg="green")

ping_thread = threading.Thread(target=ping_loop, daemon=True)
ping_thread.start()

root.mainloop()
stop_ping = True

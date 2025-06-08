import subprocess
拤=None
ﶻ=False
𪅯=True
ﬠ=Exception
𣫿=open
ﺦ=len
𞹋=int
𞢩=divmod
𐩨=exit
𗔔=subprocess.DEVNULL
𧆔=subprocess.run
𦟍=subprocess.Popen
import tkinter as tk
残=tk.Entry
𞺢=tk.Button
𨕲=tk.LEFT
Ꮣ=tk.Frame
מּ=tk.Label
閮=tk.Tk
from tkinter import filedialog,messagebox
𐪏=messagebox.showwarning
𪶪=messagebox.showerror
ﰊ=messagebox.showinfo
ۿ=messagebox.askyesno
倬=filedialog.askopenfilename
import os
𥕫=os.getcwd
𠸕=os.path
import psutil
ڌ=psutil.Process
ﱤ=psutil.process_iter
import json
𧇥=json.load
ᤇ=json.dump
import threading
𡧡=threading.Thread
import time
儢=time.time
ﺻ=time.sleep
import re
즡=re.search
import socket
𗒴=socket.gethostbyname
import requests
ط=requests.get
import urllib.request
雹=拤
𑚍=拤
ࢸ=拤
𢝖=ﶻ
𨾺="credentials.txt"
ﭺ="config.json"
Პ=拤
瑞=ﶻ
𠸙=拤
𠈧=""
ﲍ=拤
קּ=ﶻ
def 𭴩():
 𡖁="C:\\Program Files\\OpenVPN\\bin\\openvpn.exe"
 if 𠸕.exists(𡖁):
  return 𪅯
 else:
  踀=ۿ("OpenVPN Missing","OpenVPN not found.\nDo you want to download and install it automatically?")
  if 踀:
   try:
    𞺴="https://swupdate.openvpn.org/community/releases/openvpn-install-latest.exe"
    Ꮵ=𠸕.join(𥕫(),"openvpn-installer.exe")
    ﰊ("Download","Downloading OpenVPN installer...")
    urllib.request.urlretrieve(𞺴,Ꮵ)
    𦟍([Ꮵ])
    ﰊ("Installer","Installer launched. Please complete the setup manually.\nThen restart the app.")
   except ﬠ as e:
    𪶪("Download Error",f"Could not download OpenVPN:\n{e}")
  else:
   𐪏("Missing Dependency","You need to install OpenVPN manually to continue.")
  return ﶻ
def 𐲘():
 箯={"ovpn":𑚍,"game":ࢸ}
 with 𣫿(ﭺ,"w")as ﰈ:
  ᤇ(箯,ﰈ)
def ﺚ():
 global 𑚍,ࢸ
 if 𠸕.exists(ﭺ):
  with 𣫿(ﭺ,"r")as ﰈ:
   箯=𧇥(ﰈ)
   𑚍=箯.get("ovpn","")
   ࢸ=箯.get("game","")
   if 𑚍 and 𠸕.exists(𑚍):
    𗝐(𑚍)
    𪤈.config(text=f"🔵 {os.path.basename(selected_ovpn)}",fg="green")
    𩁍="blue" if "TCP" in 𠈧 or "UDP" in 𠈧 else "red"
    ﲪ.config(text=f"{o_vpn_type}",fg=𩁍)
    㓅(𑚍)
    ﰣ(𑚍)
def ﳽ():
 with 𣫿(𨾺,"w")as ﰈ:
  ﰈ.write(ﭤ.get().strip()+"\n")
  ﰈ.write(𐠔.get().strip()+"\n")
def ܧ():
 if 𠸕.exists(𨾺):
  with 𣫿(𨾺,"r")as ﰈ:
   𐪆=ﰈ.read().splitlines()
   if ﺦ(𐪆)>=2:
    ﭤ.insert(0,𐪆[0])
    𐠔.insert(0,𐪆[1])
def 𠼏():
 for 𐠒 in ﱤ(['pid','name','cmdline']):
  if 'openvpn.exe' in 𐠒.info['name'].lower():
   return 𐠒.info['pid']
 return 拤
def 𭒫():
 𫞲=𠼏()
 if 𫞲:
  try:
   𡜝=ڌ(𫞲)
   𡜝.terminate()
   return 𪅯
  except ﬠ as e:
   𪶪("Error",f"Failed to stop VPN: {e}")
 return ﶻ
def 멷():
 global 𑚍
 𞢍=倬(title="Choose OpenVPN File",filetypes=[("OVPN files","*.ovpn")])
 if 𞢍:
  𑚍=𞢍
  𗝐(𞢍)
  𪤈.config(text=f"🔵 {os.path.basename(path)}",fg="green")
  𩁍="blue" if "TCP" in 𠈧 or "UDP" in 𠈧 else "red"
  ﲪ.config(text=f"{o_vpn_type}",fg=𩁍)
  㓅(𞢍)
  ﰣ(𞢍)
  𐲘()
def 𗝐(𞢍):
 global 𠈧
 with 𣫿(𞢍,"r")as ﰈ:
  𐡕=ﰈ.read().lower()
  𫼘="proto tcp" in 𐡕
  𠲥="proto udp" in 𐡕
  if 𫼘 and 𠲥:
   𠈧="[TCP + UDP]"
  elif 𫼘:
   𠈧="[TCP]"
  elif 𠲥:
   𠈧="[UDP]"
  else:
   𠈧="[Unknown]"
def ࡄ():
 global ࢸ
 𞢍=倬(title="Choose Game Executable",filetypes=[("Executable files","*.exe")])
 if 𞢍:
  ࢸ=𞢍
  ﰊ("Game",f"Game selected: {os.path.basename(path)}")
  𐲘()
def 㓅(𞢍):
 with 𣫿(𞢍,"r")as ﰈ:
  𐡕=ﰈ.read()
  if "auth-user-pass" in 𐡕:
   㪼.pack()
   ﭤ.pack()
   ࠌ.pack()
   𐠔.pack()
   ٻ.pack(pady=5)
  else:
   㪼.pack_forget()
   ﭤ.pack_forget()
   ࠌ.pack_forget()
   𐠔.pack_forget()
   ٻ.pack_forget()
def ﰣ(𞢍):
 global Პ
 with 𣫿(𞢍,"r")as ﰈ:
  𐡕=ﰈ.read()
  𪱭=즡(r'remote\s+([^\s]+)',𐡕)
  if 𪱭:
   Პ=𪱭.group(1)
   𮑌()
  else:
   Პ=拤
   𠸙.config(text="🌍 IP Info: Unknown",fg="gray")
def 𮑌():
 global Პ
 try:
  ﻉ=𗒴(Პ)
  𐲈=ط(f"http://ip-api.com/json/{ip}").json()
  𣶑=𐲈.get("country","Unknown")
  𦧕=𐲈.get("city","")
  𠸙.config(text=f"🌍 IP: {ip} | {country} {city}",fg="blue")
 except:
  𠸙.config(text="🌍 IP Info: Unavailable",fg="gray")
def 𒉷():
 global 瑞
 while not 瑞:
  if Პ:
   try:
    𭧡=𧆔(["ping","-n","1",Პ],capture_output=𪅯,text=𪅯)
    𪱭=즡(r"Average = (\d+)ms",𭧡.stdout)
    if 𪱭:
     𐠎=𪱭.group(1)
     ᡗ.config(text=f"🌐 Ping: {ping_value} ms",fg="green")
     𦗸.config(text=f"📡 {time.strftime('%H:%M:%S')}")
    else:
     ᡗ.config(text="❌ Ping Failed",fg="red")
   except:
    ᡗ.config(text="❌ Ping Error",fg="red")
  else:
   ᡗ.config(text="⏳ No Host",fg="gray")
  ﺻ(5)
def 𘇘():
 global 𢝖
 if 𢝖:
  ﭤ.config(state="normal")
  𐠔.config(state="normal")
  ٻ.config(text="🔒 Lock")
  𢝖=ﶻ
 else:
  ﭤ.config(state="readonly")
  𐠔.config(state="readonly")
  ٻ.config(text="🔓 Unlock")
  𢝖=𪅯
def 𞢎():
 global 雹,𑚍
 if 雹 or 𠼏():
  ﰊ("VPN","Already connected.")
  return
 if not 𑚍 or not 𠸕.exists(𑚍):
  𪶪("Error","Please select a valid .ovpn file.")
  return
 굗="auth-user-pass" in 𣫿(𑚍,"r").read()
 if 굗:
  𐠁=ﭤ.get().strip()
  𨟢=𐠔.get().strip()
  if not 𐠁 or not 𨟢:
   𪶪("Error","Username and Password required.")
   return
  ﳽ()
  with 𣫿("userpass.txt","w")as ﰈ:
   ﰈ.write(f"{username}\n{password}\n")
 ﳿ="temp.ovpn"
 with 𣫿(𑚍,"r")as original,𣫿(ﳿ,"w")as 𐨗:
  for ࢻ in original:
   if ࢻ.strip().startswith("auth-user-pass"):
    continue
   𐨗.write(ࢻ)
  if 굗:
   𐨗.write("\nauth-user-pass userpass.txt\n")
 try:
  雹=𦟍(["C:\\Program Files\\OpenVPN\\bin\\openvpn.exe","--config",ﳿ],stdout=𗔔,stderr=𗔔)
  𣴘.config(text="🔌 Connecting...",fg="orange")
  𑒑.after(5000,ڎ)
 except ﬠ as e:
  𪶪("Error",f"Failed to start OpenVPN:\n{e}")
def ڎ():
 global 雹,ﲍ,קּ
 if 雹 and 雹.poll()is 拤:
  𣴘.config(text="✅ Connected",fg="green")
  ﲍ=儢()
  קּ=𪅯
  𨁙()
  ﱻ()
 elif 𠼏():
  𣴘.config(text="✅ Already Connected",fg="green")
  ﲍ=儢()
  קּ=𪅯
  𨁙()
  ﱻ()
 else:
  𣴘.config(text="❌ Failed to connect",fg="red")
  雹=拤
def 𨁙():
 if קּ:
  𢙜=𞹋(儢()-ﲍ)
  𐭄,𬖢=𞢩(𢙜,3600)
  לּ,ሜ=𞢩(𬖢,60)
  𣯈.config(text=f"⏱️ VPN Duration: {hrs:02}:{mins:02}:{secs:02}")
  𑒑.after(1000,𨁙)
def ﱻ():
 if not ࢸ or not 𠸕.exists(ࢸ):
  ࡄ()
 else:
  try:
   𦟍([ࢸ])
   ﰊ("Game",f"Launching: {os.path.basename(selected_game)}")
  except ﬠ as e:
   𪶪("Error",f"Could not launch game:\n{e}")
def ﺩ():
 global 雹,קּ
 if 雹:
  雹.terminate()
  雹=拤
  𣴘.config(text="🔌 Disconnected",fg="gray")
 elif 𠼏():
  𭒫()
  𣴘.config(text="🔌 Disconnected",fg="gray")
 else:
  ﰊ("VPN","VPN is not running.")
 קּ=ﶻ
 𣯈.config(text="⏱️ VPN Duration: 00:00:00")
𑒑=閮()
𑒑.title("Meshari Dis: ok.8")
𑒑.geometry("400x530")
𑒑.resizable(ﶻ,ﶻ)
if not 𭴩():
 𑒑.destroy()
 𐩨()
מּ(𑒑,text="🎮",font=("Arial",14)).pack(pady=10)
𞸧=Ꮣ(𑒑)
𞸧.pack()
𪤈=מּ(𞸧,text="🔘 No .ovpn file selected",fg="gray")
𪤈.pack(side=𨕲)
ﲪ=מּ(𞸧,text="",fg="blue")
ﲪ.pack(side=𨕲,padx=5)
𞺢(𑒑,text="Select OVPN File",command=멷).pack(pady=5)
𞺢(𑒑,text="Select Game EXE",command=ࡄ).pack(pady=5)
㪼=מּ(𑒑,text="Username:")
ﭤ=残(𑒑,width=30)
ࠌ=מּ(𑒑,text="Password:")
𐠔=残(𑒑,width=30,show="*")
ٻ=𞺢(𑒑,text="🔒 Lock",command=𘇘,width=10)
𞺢(𑒑,text="Connect + Launch Game",command=𞢎,width=25).pack(pady=5)
𞺢(𑒑,text="Disconnect VPN",command=ﺩ,width=25).pack(pady=5)
𞺢(𑒑,text="🔴 Force Stop VPN",command=𭒫,fg="red",width=25).pack(pady=5)
𣴘=מּ(𑒑,text="🔌 Disconnected",fg="gray",font=("Arial",12))
𣴘.pack(pady=10)
𠸙=מּ(𑒑,text="🌍 IP Info: Waiting...",fg="gray",font=("Arial",9))
𠸙.pack(pady=2)
ᡗ=מּ(𑒑,text="🌐 Ping: Waiting...",fg="gray",font=("Arial",10))
ᡗ.pack()
𦗸=מּ(𑒑,text="📡 Last Ping: --:--:--",fg="gray",font=("Arial",9))
𦗸.pack(pady=2)
𣯈=מּ(𑒑,text="⏱️ VPN Duration: 00:00:00",fg="blue",font=("Arial",10))
𣯈.pack(pady=2)
ﺚ()
ܧ()
if 𠼏():
 if ۿ("VPN Running","VPN is already running. Do you want to stop it?"):
  𭒫()
  𣴘.config(text="🔌 Disconnected",fg="gray")
 else:
  𣴘.config(text="✅ Running",fg="green")
ﶈ=𡧡(target=𒉷,daemon=𪅯)
ﶈ.start()
𑒑.mainloop()
瑞=𪅯

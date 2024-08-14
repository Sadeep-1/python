import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox

def scanHost(ip, startPort, endPort):
    output_text.insert(tk.END, f'[*] Starting TCP port scan on host {ip}\n')
    tcp_scan(ip, startPort, endPort)
    output_text.insert(tk.END, f'[+] TCP scan on host {ip} complete\n')

def tcp_scan(ip, startPort, endPort):
    for port in range(startPort, endPort + 1):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(0.01)
            if not tcp.connect_ex((ip, port)):
                output_text.insert(tk.END, f'[+] {ip}:{port}/TCP Open\n')
            tcp.close()
        except Exception:
            pass

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def on_scan_button_click():
    ip = ip_entry.get()
    startPort = start_port_entry.get()
    endPort = end_port_entry.get()

    if not validate_ip(ip):
        messagebox.showerror("Invalid IP", "Please enter a valid IP address.")
        return

    if not startPort.isdigit() or not endPort.isdigit():
        messagebox.showerror("Invalid Ports", "Please enter valid port numbers.")
        return

    startPort = int(startPort)
    endPort = int(endPort)

    if startPort > endPort:
        messagebox.showerror("Invalid Range", "Start Port should be less than or equal to End Port.")
        return

    output_text.delete(1.0, tk.END)  # Clear the previous output
    scanHost(ip, startPort, endPort)

# GUI setup
root = tk.Tk()
root.title("Port Scanner")
root.geometry("500x400")
root.resizable(False, False)

# Configure grid layout
root.columnconfigure(0, weight=1)

# Title label
title_label = tk.Label(root, text="TCP Port Scanner", font=("Arial", 16))
title_label.grid(row=0, column=0, pady=10)

# IP address input
ip_frame = tk.Frame(root)
ip_frame.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
ip_label = tk.Label(ip_frame, text="IP Address:", font=("Arial", 12))
ip_label.grid(row=0, column=0, sticky="w")
ip_entry = tk.Entry(ip_frame, width=30)
ip_entry.grid(row=0, column=1, padx=10)

# Start and end port inputs
port_frame = tk.Frame(root)
port_frame.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

start_port_label = tk.Label(port_frame, text="Start Port:", font=("Arial", 12))
start_port_label.grid(row=0, column=0, sticky="w")
start_port_entry = tk.Entry(port_frame, width=10)
start_port_entry.grid(row=0, column=1, padx=10)

end_port_label = tk.Label(port_frame, text="End Port:", font=("Arial", 12))
end_port_label.grid(row=0, column=2, sticky="w")
end_port_entry = tk.Entry(port_frame, width=10)
end_port_entry.grid(row=0, column=3, padx=10)

# Start scan button
scan_button = tk.Button(root, text="Start Scan", command=on_scan_button_click, width=20, bg="lightblue")
scan_button.grid(row=3, column=0, pady=20)

# Output display
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 10))
output_text.grid(row=4, column=0, pady=10, padx=10)

# Run the GUI
root.mainloop()

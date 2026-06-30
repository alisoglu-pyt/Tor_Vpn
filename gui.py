#!/usr/bin/env python3

import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox


SYSTEM_DIST_PACKAGES = "/usr/lib/python3/dist-packages"


def _ensure_system_site_packages():
    """Expose system GTK bindings to the virtualenv when available."""
    if not sys.platform.startswith("linux"):
        return

    for path in (SYSTEM_DIST_PACKAGES, "/usr/local/lib/python3/dist-packages"):
        if os.path.isdir(path) and path not in sys.path:
            sys.path.append(path)


def _prefer_gtk_tray_backend():
    """Use GTK on Linux so tray menus respond to right-click."""
    if os.environ.get("PYSTRAY_BACKEND") or not sys.platform.startswith("linux"):
        return

    try:
        _ensure_system_site_packages()
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk  # noqa: F401
    except Exception:
        return

    os.environ["PYSTRAY_BACKEND"] = "gtk"


_prefer_gtk_tray_backend()

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

# Simple Tkinter GUI to control the Tor tunnel scripts
def _resource_dir():
    candidates = []
    if hasattr(sys, "_MEIPASS"):
        candidates.append(sys._MEIPASS)
    if getattr(sys, "frozen", False):
        candidates.append(os.path.dirname(sys.executable))
    candidates.append(os.path.dirname(os.path.abspath(__file__)))

    for candidate in candidates:
        if os.path.exists(os.path.join(candidate, "start_vpn.py")):
            return candidate

    return candidates[0]


BASE_DIR = _resource_dir()
START_SCRIPT = os.path.join(BASE_DIR, "start_vpn.py")
STATE_FILE = "/tmp/tor_tunnel_state"
REGION_CODES = ['any', 'us', 'de', 'nl', 'fr', 'se', 'ca', 'gb', 'ch', 'es', 'it', 'jp', 'sg']


class TorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tor Tunnel Controller")
        self.geometry("520x420")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 11), padding=8)

        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=self.on_quit, accelerator='Ctrl+Q')
        menubar.add_cascade(label='File', menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=self.on_about)
        menubar.add_cascade(label='Help', menu=help_menu)
        self.config(menu=menubar)
        self.bind_all('<Control-q>', lambda _event: self.on_quit())

        header = ttk.Label(self, text="🚀 Tor Tunnel", font=("Segoe UI", 20, 'bold'))
        header.pack(pady=(14, 6))

        self.status_var = tk.StringVar()
        self.status_var.set("Unknown")

        self.status_label = ttk.Label(self, textvariable=self.status_var, font=("Segoe UI", 12))
        self.status_label.pack(pady=(0, 10))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=6)

        self.toggle_btn = ttk.Button(btn_frame, text="Toggle Start/Stop", command=self.on_toggle)
        self.toggle_btn.grid(row=0, column=0, padx=8)

        self.refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.refresh_status)
        self.refresh_btn.grid(row=0, column=1, padx=8)

        # SOCKS control
        socks_frame = ttk.Frame(self)
        socks_frame.pack(pady=(6, 0))
        self.socks_var = tk.BooleanVar()
        self.socks_check = ttk.Checkbutton(socks_frame, text="Expose SOCKS proxy (127.0.0.1:9050)", variable=self.socks_var, command=self.on_toggle_socks)
        self.socks_check.grid(row=0, column=0, padx=8)

        # Region control
        region_frame = ttk.Frame(self)
        region_frame.pack(pady=(6, 0))
        ttk.Label(region_frame, text="Exit country:").grid(row=0, column=0, padx=(0,6))
        self.region_cb = ttk.Combobox(region_frame, values=['any','us','de','nl','fr','se','ca','gb','ch','es','it','jp','sg'], state='readonly')
        self.region_cb.grid(row=0, column=1, padx=6)
        self.region_btn = ttk.Button(region_frame, text="Set Region", command=self.on_set_region)
        self.region_btn.grid(row=0, column=2, padx=6)
        self.region_cb.set('any')
        log_frame = ttk.LabelFrame(self, text="Logs")
        log_frame.pack(fill='both', expand=True, padx=12, pady=12)

        self.log = tk.Text(log_frame, height=10, state='disabled', wrap='word', font=("Segoe UI", 9))
        self.log.pack(fill='both', expand=True, padx=6, pady=6)

        # If not running as root, warn and disable control buttons
        if os.geteuid() != 0:
            self.append_log("[!] GUI is not running as root. Start/Stop controls are disabled.\n")
            self.toggle_btn.state(['disabled'])

        self.refresh_status()
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        if PYSTRAY_AVAILABLE:
            self.setup_tray()
        else:
            self.append_log("[!] pystray/Pillow not installed: tray icon unavailable.\n")
        # poll status periodically
        self.after(2000, self.poll_status)

    def build_appindicator_menu(self):
        menu = Gtk.Menu()

        region_item = Gtk.MenuItem(label='Change Region')
        region_submenu = Gtk.Menu()
        for code in REGION_CODES:
            item = Gtk.MenuItem(label=code.upper())
            item.connect('activate', lambda _, c=code: self.after(0, self.on_tray_region, c))
            region_submenu.append(item)
        region_item.set_submenu(region_submenu)
        menu.append(region_item)

        exit_item = Gtk.MenuItem(label='Exit')
        exit_item.connect('activate', lambda _: self.after(0, self.on_quit))
        menu.append(exit_item)

        menu.show_all()
        return menu

    def setup_appindicator(self):
        icon = AppIndicator3.Indicator.new(
            'tor-vpn',
            'network-transmit-receive',
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        icon.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        icon.set_menu(self.build_appindicator_menu())
        self.indicator = icon
        # Start the GTK loop in a daemon thread
        threading.Thread(target=Gtk.main, daemon=True).start()

    def setup_tray(self):
        def create_region_menu():
            items = []
            for code in REGION_CODES:
                items.append(pystray.MenuItem(
                    code.upper(),
                    lambda _, c=code: self.after(0, self.on_tray_region, c),
                    checked=lambda item, c=code: self.region_cb.get() == c
                ))
            return pystray.Menu(*items)

        tray_menu = pystray.Menu(
            pystray.MenuItem('Show GUI', lambda _: self.after(0, self.show_window), default=True, visible=False),
            pystray.MenuItem('Change Region', create_region_menu()),

            pystray.MenuItem('Exit', lambda _: self.after(0, self.on_quit))
        )

        # Create simple icon
        icon_img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon_img)
        draw.ellipse((8, 8, 56, 56), fill=(0, 198, 255), outline=(255, 255, 255))
        draw.ellipse((20, 20, 44, 44), fill=(20, 20, 30))

        self.tray_icon = pystray.Icon('tor-vpn', icon_img, 'Tor VPN', menu=tray_menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self):
        if not self.winfo_viewable():
            self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()

    def on_quit(self):
        try:
            if PYSTRAY_AVAILABLE and hasattr(self, 'tray_icon'):
                self.tray_icon.stop()
        except Exception:
            pass
        self.destroy()

    def on_about(self):
        messagebox.showinfo(
            'About',
            "Tor Tunnel Controller\n\nAuthor: Bekir Alişoğlu\nalisoglu@yahoo.com"
        )

    def on_tray_region(self, code):
        self.region_cb.set(code)
        self.append_log(f"[+] Tray: set region to {code}\n")
        self.on_set_region()

    def append_log(self, text: str):
        self.log.configure(state='normal')
        self.log.insert('end', text)
        self.log.see('end')
        self.log.configure(state='disabled')

    def run_module_action(self, action: str):
        """Call start/stop functions from the start_vpn module."""
        try:
            # import here to show errors in GUI if module missing
            import importlib.util
            spec = importlib.util.spec_from_file_location("start_vpn", START_SCRIPT)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if action == 'start':
                self.append_log("[+] Calling start_vpn.start_tor_tunnel()\n")
                mod.start_tor_tunnel()
            elif action == 'stop':
                self.append_log("[+] Calling start_vpn.stop_tor_tunnel()\n")
                mod.stop_tor_tunnel()
            elif action == 'enable_socks':
                self.append_log("[+] Enabling SOCKS proxy\n")
                mod.enable_socks()
            elif action == 'disable_socks':
                self.append_log("[+] Disabling SOCKS proxy\n")
                mod.disable_socks()
            elif action.startswith('set_region:'):
                _, cc = action.split(':', 1)
                self.append_log(f"[+] Setting exit country to {cc}\n")
                mod.set_exit_country(cc)

            self.append_log("[+] Action completed.\n")
        except Exception as e:
            self.append_log(f"[!] Exception while running module: {e}\n")
        finally:
            self.refresh_status()

    def on_toggle_socks(self):
        if os.geteuid() != 0:
            messagebox.showwarning("Permission", "Please run this GUI as root (sudo) to control SOCKS.")
            # revert checkbox state
            self.socks_var.set(not self.socks_var.get())
            return

        action = 'enable_socks' if self.socks_var.get() else 'disable_socks'
        t = threading.Thread(target=self.run_module_action, args=(action,), daemon=True)
        t.start()

    def on_set_region(self):
        if os.geteuid() != 0:
            messagebox.showwarning("Permission", "Please run this GUI as root (sudo) to change region.")
            return
        cc = self.region_cb.get()
        if not cc:
            messagebox.showinfo("Region", "Please select a region (or 'any').")
            return
        action = f"set_region:{cc}"
        t = threading.Thread(target=self.run_module_action, args=(action,), daemon=True)
        t.start()
    def on_toggle(self):
        # Run start/stop in a background thread
        if os.geteuid() != 0:
            messagebox.showwarning("Permission", "Please run this GUI as root (sudo) to control the tunnel.")
            return

        action = 'stop' if self.is_running() else 'start'
        t = threading.Thread(target=self.run_module_action, args=(action,), daemon=True)
        t.start()

    def is_running(self) -> bool:
        return os.path.exists(STATE_FILE)

    def refresh_status(self):
        running = self.is_running()
        if running:
            self.status_var.set("Status: ON ⚡")
            self.status_label.configure(foreground='#00c853')
            self.toggle_btn.config(text='Stop')
        else:
            self.status_var.set("Status: OFF ✖")
            self.status_label.configure(foreground='#d32f2f')
            self.toggle_btn.config(text='Start')

        # Update SOCKS and region information from torrc if module available
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("start_vpn", START_SCRIPT)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.socks_var.set(mod.is_socks_enabled())
            country = mod.get_exit_country() or 'any'
            self.region_cb.set(country)
        except Exception:
            pass

    def poll_status(self):
        self.refresh_status()
        self.after(2000, self.poll_status)

    # Removed web UI opening: GUI now acts as the VPN controller only.


def main():
    app = TorGUI()
    app.mainloop()


if __name__ == '__main__':
    main()

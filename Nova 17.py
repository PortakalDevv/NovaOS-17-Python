import tkinter as tk
from tkinter import messagebox, filedialog
import time
import random


# --- GÖNDERDİĞİN PÜRÜZSÜZ SÜRÜKLEME MOTORU ---
def make_draggable(window, header):
    def start_move(event):
        window.lift()
        window.drag_data = {"x": event.x, "y": event.y}

    def stop_move(event):
        window.drag_data = None

    def on_motion(event):
        if window.drag_data:
            deltax = event.x - window.drag_data["x"]
            deltay = event.y - window.drag_data["y"]
            x = window.winfo_x() + deltax
            y = window.winfo_y() + deltay
            window.place(x=x, y=y)

    header.bind("<ButtonPress-1>", start_move)
    header.bind("<ButtonRelease-1>", stop_move)
    header.bind("<B1-Motion>", on_motion)


class AdvancedWindowsOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nova 17.1")

        # Gerçek Tam Ekran Modu
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Renk Paleti (Windows 11 Dark / Fluent Tasarım)
        self.bg_desktop = "#1c2030"  # Derin Gece Mavisi Masaüstü
        self.bg_taskbar = "#141724"  # Koyu Akıllı Görev Çubuğu
        self.bg_window = "#1e2233"  # Pencere İç Gövdesi
        self.bg_header = "#252b42"  # Pencere Başlık Çubuğu
        self.fg_white = "#ffffff"

        self.configure(bg=self.bg_desktop)

        # Masaüstü Ana Katmanı
        self.desktop = tk.Frame(self, bg=self.bg_desktop)
        self.desktop.pack(fill=tk.BOTH, expand=True)

        # Arka Planda Büyük Logo Yazısı
        self.logo_lbl = tk.Label(self.desktop, text="Nova 17.1", font=("Segoe UI", 60, "bold"), fg="#282f44",
                                 bg=self.bg_desktop)
        self.logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Görev Çubuğu (Taskbar)
        self.taskbar = tk.Frame(self, bg=self.bg_taskbar, height=48)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.taskbar.pack_propagate(False)

        # Başlat Menüsü Paneli (Gizli Başlar)
        self.start_menu = tk.Frame(self.desktop, bg=self.bg_header, highlightbackground="#3d4666", highlightthickness=1)
        self.start_menu_visible = False

        # Sistem Bileşenlerini İnşa Et
        self.setup_taskbar()
        self.setup_desktop_icons()

    # --- PENCERE SİSTEMİ (NOVA DRAG MOTORU ENTEGRELİ) ---
    def create_window(self, title, w=500, h=400):
        if self.start_menu_visible:
            self.toggle_start_menu()

        # Pencere Çerçevesi
        win = tk.Frame(self.desktop, bg=self.bg_window, highlightbackground="#3d4666", highlightthickness=2)
        win.place(x=250, y=120, width=w, height=h)

        # Üst Başlık Çubuğu (Header)
        header = tk.Frame(win, bg=self.bg_header, height=35, cursor="fleur")
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Başlık Yazısı
        title_lbl = tk.Label(header, text=title, fg=self.fg_white, bg=self.bg_header, font=("Segoe UI", 10, "bold"))
        title_lbl.pack(side=tk.LEFT, padx=10, pady=5)

        # Kapatma Butonu (Modern Windows Tarzı)
        close_btn = tk.Button(header, text="✕", command=win.destroy, bg=self.bg_header, fg=self.fg_white,
                              bd=0, activebackground="#e81123", activeforeground="white", padx=12)
        close_btn.pack(side=tk.RIGHT, fill=tk.Y)

        # Sürükleme yeteneklerini veriyoruz
        make_draggable(win, header)
        make_draggable(win, title_lbl)

        # Uygulamaların Tasarım Yapacağı İç Alan
        content = tk.Frame(win, bg=self.bg_window)
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        return content

    # --- GÖREV ÇUBUĞU VE SAAT ---
    def setup_taskbar(self):
        # Başlat Butonu
        start_btn = tk.Button(self.taskbar, text="❖", font=("Segoe UI", 14), bg=self.bg_taskbar, fg="#0078d4",
                              activebackground="#202538", activeforeground="#0078d4", bd=0,
                              command=self.toggle_start_menu, padx=15)
        start_btn.pack(side=tk.LEFT, fill=tk.Y)

        # Sistem Saati (Sağ Köşe)
        self.clock_lbl = tk.Label(self.taskbar, bg=self.bg_taskbar, fg=self.fg_white, font=("Segoe UI", 9, "bold"))
        self.clock_lbl.pack(side=tk.RIGHT, padx=15)
        self.update_clock()

        # OS Kapatma Butonu (En Sağda)
        exit_btn = tk.Button(self.taskbar, text="⏻", font=("Segoe UI", 11), bg=self.bg_taskbar, fg="#ff5f56",
                             activebackground="#e81123", activeforeground="white", bd=0, command=self.destroy, padx=12)
        exit_btn.pack(side=tk.RIGHT, fill=tk.Y)

    def update_clock(self):
        self.clock_lbl.config(text=time.strftime("%H:%M:%S\n%d.%m.%Y"))
        self.after(1000, self.update_clock)

    # --- MASAÜSTÜ İKONLARI (GÖRÜNÜR UYGULAMALAR) ---
    def setup_desktop_icons(self):
        icons = [
            ("🌐 Browser", self.open_browser, 30, 30),
            ("📝 Notepad", self.open_notepad, 30, 130),
            ("🧮 Calculator", self.open_calculator, 30, 230),
            ("📁 File Explorer", self.open_file_explorer, 30, 330),
            ("⚙️ Settings", self.open_settings, 140, 30),
            ("💻 Terminal", self.open_terminal, 140, 130),
            ("🎮 Game Box", self.open_game, 140, 230)
        ]
        for name, cmd, x, y in icons:
            btn = tk.Button(self.desktop, text=name, bg=self.bg_desktop, fg=self.fg_white,
                            font=("Segoe UI", 9, "bold"), activebackground="#2c324d", activeforeground="white",
                            bd=0, cursor="hand2", command=cmd, compound="top", pady=5)
            btn.place(x=x, y=y, width=100, height=80)

    # --- BAŞLAT MENÜSÜ MANTIĞI ---
    def toggle_start_menu(self):
        if self.start_menu_visible:
            self.start_menu.place_forget()
            self.start_menu_visible = False
        else:
            self.start_menu.place(x=5, y=self.winfo_height() - 450, width=280, height=400)
            self.start_menu_visible = True

            for w in self.start_menu.winfo_children(): w.destroy()

            tk.Label(self.start_menu, text="FIXED ONES", bg=self.bg_header, fg="#0078d4",
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=10)

            apps = [
                ("🌐 Nova Web Browser", self.open_browser),
                ("📝 Advanced Notepad", self.open_notepad),
                ("🧮 Mathematical Calculator", self.open_calculator),
                ("📁 File System", self.open_file_explorer),
                ("⚙️ Control Panel (Settings)", self.open_settings),
                ("💻 Python Terminal Command Line", self.open_terminal),
                ("🎮 Mini Game World", self.open_game)
            ]
            for name, cmd in apps:
                btn = tk.Button(self.start_menu, text=name, bg=self.bg_header, fg=self.fg_white, font=("Segoe UI", 9),
                                anchor="w", relief=tk.FLAT, activebackground="#3d4666", activeforeground="white",
                                command=cmd)
                btn.pack(fill=tk.X, padx=10, pady=3)

    # ==================== GELİŞMİŞ UYGULAMALAR MODÜLÜ ====================

    # 1. DOSYA GEZGİNİ (Sanal Sürücü Sistemi)
    def open_file_explorer(self):
        area = self.create_window("📁 File Explorer", 550, 400)

        sidebar = tk.Frame(area, bg="#141724", width=130)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        main_explorer = tk.Frame(area, bg="#1e2233")
        main_explorer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        folders = ["Desktop", "Documents", "Downloads", "Projects", "Pictures"]

        def load_folder(name):
            for w in main_explorer.winfo_children(): w.destroy()
            tk.Label(main_explorer, text=f"Location: This Computer > {name}", fg="cyan", bg="#1e2233",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=5)

            # İçerik Örnekleri
            if name == "Projects":
                items = ["📄 OS.py", "📄 Project.py", "📁 Unreal_Engine_Scripts"]
            elif name == "Documents":
                items = ["📄 kernel.txt", "📄 readme.txt"]
            else:
                items = ["📁 Folder is Empty"]

            for item in items:
                tk.Label(main_explorer, text=f"  {item}", fg="white", bg="#1e2233", font=("Segoe UI", 10)).pack(
                    anchor="w", pady=4)

        for f in folders:
            tk.Button(sidebar, text=f"📁 {f}", bg="#141724", fg="white", bd=0, anchor="w",
                      activebackground="#3d4666", activeforeground="white",
                      command=lambda folder=f: load_folder(folder)).pack(fill=tk.X, pady=2, padx=5)
        load_folder("Masaüstü")

    # 2. SİMÜLE WEB TARAYICI (Sıfır Bağımlılık - Tkinter Native)
    def open_browser(self):
        area = self.create_window("🌐 Nova Web Browser", 650, 450)

        nav_bar = tk.Frame(area, bg="#141724", pady=5)
        nav_bar.pack(fill=tk.X)

        url_bar = tk.Entry(nav_bar, bg="#252b42", fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10))
        url_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=3)
        url_bar.insert(0, "www.novasearch.com")

        web_content = tk.Text(area, bg="#ffffff", fg="#000000", font=("Arial", 11), wrap=tk.WORD, padx=10, pady=10)
        web_content.pack(fill=tk.BOTH, expand=True)

        def go_to_url(event=None):
            url = url_bar.get().strip().lower()
            web_content.delete("1.0", tk.END)
            if "search" in url or "google" in url:
                web_content.insert(tk.END,
                                   "🔍 NOVA SEARCH ENGINE\n\nTest1:\n- Test2\n- Test3\n- Test4\n")
            elif "haber" in url:
                web_content.insert(tk.END,
                                   "📰 Test5\n\n- Test6\n- Test7")
            else:
                web_content.insert(tk.END,
                                   f"🌐 {url} Test Text\n\nTest Page")

        url_bar.bind("<Return>", go_to_url)
        go_to_url()

    # 3. NOT DEFTERİ (Dosya Kaydetme/Açma Destekli)
    def open_notepad(self):
        area = self.create_window("📝 Notebook", 500, 380)

        menu_bar = tk.Frame(area, bg="#252b42")
        menu_bar.pack(fill=tk.X)

        text_pad = tk.Text(area, bg="#ffffff", fg="#000000", font=("Consolas", 11), wrap=tk.WORD,
                           insertbackground="black")
        text_pad.pack(fill=tk.BOTH, expand=True)

        def save_file():
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text_pad.get("1.0", tk.END))
                messagebox.showinfo("System", "The file has been successfully saved to the computer!")

        tk.Button(menu_bar, text="💾 ", command=save_file, bg="#3d4666", fg="white", bd=0, padx=8,
                  pady=3).pack(side=tk.LEFT, padx=5, pady=2)

    # 4. HESAP MAKİNESİ
    def open_calculator(self):
        area = self.create_window("🧮 Calculator", 280, 360)
        entry = tk.Entry(area, font=("Segoe UI", 16), justify="right", bg="#141724", fg="white", bd=0,
                         insertbackground="white")
        entry.pack(fill=tk.X, pady=8, ipady=4)

        grid_frame = tk.Frame(area, bg=self.bg_window)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        buttons = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', 'C', '0', '=', '+']

        def calc_action(char):
            if char == 'C':
                entry.delete(0, tk.END)
            elif char == '=':
                try:
                    res = eval(entry.get())
                    entry.delete(0, tk.END);
                    entry.insert(tk.END, str(res))
                except:
                    entry.delete(0, tk.END);
                    entry.insert(tk.END, "Error")
            else:
                entry.insert(tk.END, char)

        r, c = 0, 0
        for b in buttons:
            btn = tk.Button(grid_frame, text=b, font=("Segoe UI", 11, "bold"), bg="#252b42", fg="white", bd=0,
                            activebackground="#3d4666", activeforeground="white", command=lambda x=b: calc_action(x))
            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
            c += 1
            if c > 3: c, r = 0, r + 1

        for i in range(4): grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(4): grid_frame.grid_rowconfigure(i, weight=1)

    # 5. AYARLAR VE KONTROL PANELİ
    def open_settings(self):
        area = self.create_window("⚙️ System Settings", 420, 350)

        tk.Label(area, text="Change Desktop Theme", fg="cyan", bg=self.bg_window,
                 font=("Segoe UI", 11, "bold")).pack(pady=5)

        themes = [("Midnight Blue", "#1c2030"), ("Deep Black", "#0a0a0a"), ("Classic Nova", "#0078d4"),
                  ("Emerald", "#0f3022")]
        for name, color in themes:
            tk.Button(area, text=name, bg="#252b42", fg="white", bd=0, width=20, pady=3,
                      command=lambda c=color: [self.desktop.config(bg=c), self.logo_lbl.config(bg=c)]).pack(pady=3)

        tk.Frame(area, height=1, bg="#3d4666").pack(fill=tk.X, pady=15)
        tk.Label(area, text="System Features", fg="cyan", bg=self.bg_window, font=("Segoe UI", 11, "bold")).pack(
            pady=5)

        specs = f"OS: Nova 17\nCore Structure: Deltax 4 Standard\nDisplay Mode: Borderless Sandbox Environment\nSituation: Safe and Stable"
        tk.Label(area, text=specs, fg="white", bg=self.bg_window, justify="left", font=("Segoe UI", 9)).pack(pady=5)

    # 6. SİMÜLE TERMINAL (CMD / POWERSHELL MANTIĞI)
    def open_terminal(self):
        area = self.create_window("💻 Terminal", 550, 360)
        out_box = tk.Text(area, bg="#000000", fg="#00ff00", font=("Consolas", 10), wrap=tk.WORD)
        out_box.pack(fill=tk.BOTH, expand=True)
        out_box.insert(tk.END,
                       "Nova [Version 17.0.13]\n(c) Nova Corporation. All rights reserved.\n\nC:\\Users\\Developer> ")

        cmd_entry = tk.Entry(area, bg="#111111", fg="#ffffff", insertbackground="white", bd=0, font=("Consolas", 10))
        cmd_entry.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
        cmd_entry.focus_set()

        def run_command(event):
            cmd = cmd_entry.get().strip().lower()
            cmd_entry.delete(0, tk.END)
            out_box.insert(tk.END, cmd + "\n")

            if cmd == "help":
                out_box.insert(tk.END,
                               "Available Commands:\n - help: Lists the commands.\n - ver: Indicates the kernel version.\n - clear: Clears the screen.\n - systeminfo: Shows system resource load.\n")
            elif cmd == "ver":
                out_box.insert(tk.END, "Nova-Deltax Core Engine v4.17.0\n")
            elif cmd == "clear":
                out_box.delete("3.0", tk.END)
            elif cmd == "systeminfo":
                out_box.insert(tk.END, f"CPU Load: %{random.randint(4, 18)}  |  RAM Usage: %{random.randint(22, 45)}\n")
            else:
                out_box.insert(tk.END, f"'{cmd}' It was not recognized as a valid internal or external command.\n")

            out_box.insert(tk.END, "\nC:\\Users\\Developer> ")
            out_box.see(tk.END)

        cmd_entry.bind("<Return>", run_command)

    # 7. MİNİ OYUN (Sayı Tahmin Arcade)
    def open_game(self):
        area = self.create_window("🎮 Number Guessing Game", 350, 250)
        secret = random.randint(1, 50)

        tk.Label(area, text="A Number Between 1 And 50 Was Chosen!", fg="white", bg=self.bg_window,
                 font=("Segoe UI", 10, "bold")).pack(pady=10)
        ent = tk.Entry(area, justify="center", font=("Segoe UI", 12), width=10)
        ent.pack(pady=5)

        hint_lbl = tk.Label(area, text="Enter Your Prediction and Check İt.", fg="yellow", bg=self.bg_window)
        hint_lbl.pack(pady=10)

        def check_guess():
            try:
                val = int(ent.get())
                if val < secret:
                    hint_lbl.config(text="Higher! ⬆️", fg="orange")
                elif val > secret:
                    hint_lbl.config(text="Lower! ⬇️", fg="orange")
                else:
                    hint_lbl.config(text="Congratulations! You Got İt Right 🎉", fg="lime")
            except:
                hint_lbl.config(text="Please Enter A Valid Number!", fg="red")
            ent.delete(0, tk.END)

        tk.Button(area, text="Check", command=check_guess, bg="#252b42", fg="white", bd=0, padx=10, pady=4).pack()


if __name__ == "__main__":
    app = AdvancedWindowsOS()
    app.mainloop()

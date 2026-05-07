import customtkinter as ctk
from tkinter import messagebox

# ==========================================
# 1. SINIFLARIN TANIMLANMASI (OOP)
# ==========================================

class Egitmen:
    """Eğitmen bilgilerini tutan ana sınıf."""
    def __init__(self, ad, uzmanlik):
        self.ad = ad           # Özellik: Ad Soyad
        self.uzmanlik = uzmanlik # Özellik: Uzmanlık alanı

class Ogrenci:
    """Sisteme giriş yapan kullanıcı türünü tanımlayan sınıf."""
    def __init__(self, ogrenci_id, ad, email):
        self.ogrenci_id = ogrenci_id # Özellik: No
        self.ad = ad                 # Özellik: Ad Soyad
        self.email = email           # Özellik: İletişim
        # Veri Yapısı: Kursları saklamak için bir liste
        self.kayitli_kurslar = []

    def kurs_listesi(self):
        """Öğrencinin aldığı kursların isimlerini döndürür."""
        return [kurs.kurs_adi for kurs in self.kayitli_kurslar]

class Kurs:
    """Platformdaki kursları ve kayıt işlemlerini yöneten sınıf."""
    def __init__(self, kurs_id, kurs_adi, egitmen, kontenjan):
        self.kurs_id = kurs_id      # Özellik: Kurs Kodu
        self.kurs_adi = kurs_adi    # Özellik: Kurs Adı
        self.egitmen = egitmen      # Özellik: Egitmen Nesnesi
        self.kontenjan = kontenjan  # Özellik: Kapasite
        # Veri Yapısı: Kayıtlı öğrencileri tutan liste
        self.kayitli_ogrenciler = []

    def ogrenci_kaydet(self, ogrenci):
        """Metod: Kursa yeni bir öğrenci kaydı gerçekleştirir."""
        # Senaryo Testi: Kontenjan dolu mu?
        if len(self.kayitli_ogrenciler) < self.kontenjan:
            # Senaryo Testi: Öğrenci zaten kayıtlı mı?
            if ogrenci not in self.kayitli_ogrenciler:
                self.kayitli_ogrenciler.append(ogrenci)
                ogrenci.kayitli_kurslar.append(self)
                return True, "Kayıt Başarılı!"
            return False, "Zaten kayıtlısınız."
        return False, "Kontenjan dolu!"

# ==========================================
# 2. ARAYÜZ TASARIMI VE KODLAMA
# ==========================================

class Uygulama(ctk.CTk):
    """Ana grafik arayüz akışını yöneten sınıf."""
    def __init__(self, ogrenci_verisi):
        super().__init__()
        
        # Veri Yapısı: Girişten gelen veriler Dictionary (Sözlük) olarak işlenir
        self.aktif_ogrenci = Ogrenci(
            ogrenci_verisi['id'], 
            ogrenci_verisi['ad'], 
            ogrenci_verisi['email']
        )
        
        self.title(f"İKÜ LYS Sistemi - {self.aktif_ogrenci.ad}")
        self.geometry("1200x750")
        self.configure(fg_color="#121212")
        
        self.veri_hazirla()
        self.setup_ui()
        self.show_page("home")

    def veri_hazirla(self):
        """Sistemdeki kurs ve eğitmen nesnelerini oluşturur."""
        e1 = Egitmen("Dr. Ahmet Yılmaz", "Yazılım")
        e2 = Egitmen("Prof. Dr. Elif Aksu", "Yapay Zeka")
        e3 = Egitmen("Dr. Bade Türk", "Matematik")
        e4 = Egitmen("Prof. Dr. Muhammed Aled Ora", "Fizik")
        
        # Veri Yapısı: Tüm kurslar bir Liste içerisinde saklanır
        self.kurslar = [
            Kurs(101, "Python Programlama", e1, 20),
            Kurs(102, "Veri Yapıları", e1, 30),
            Kurs(103, "Derin Öğrenme", e2, 15),
            Kurs(104, "Siber Güvenlik", e2, 10),
            Kurs(105, "Calculus", e3, 90),
            Kurs(106, "Fizik III", e4, 90),
        ]

    def setup_ui(self):
        """Grafik arayüz bileşenlerini oluşturur ve yerleştirir."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SOL SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1e1e1e", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="İKÜ LYS", font=("Arial", 22, "bold"), text_color="#2198A1").pack(pady=30)
        
        self.btn_home = ctk.CTkButton(self.sidebar, text="🏠 Ana Sayfa", fg_color="transparent", anchor="w", command=lambda: self.show_page("home"))
        self.btn_home.pack(fill="x", padx=15, pady=5)
        
        self.btn_list = ctk.CTkButton(self.sidebar, text="📘 Kurslarım", fg_color="transparent", anchor="w", command=lambda: self.show_page("lessons"))
        self.btn_list.pack(fill="x", padx=15, pady=5)

        # ORTA KONTEYNER (Sayfalar burada değişir)
        self.container = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20)
        self.container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.pages = {
            "home": self.create_home(),
            "lessons": self.create_lessons()
        }

        # SAĞ PANEL (Profil Kartı)
        self.r_sidebar = ctk.CTkFrame(self, width=280, fg_color="#1e1e1e", corner_radius=0)
        self.r_sidebar.grid(row=0, column=2, sticky="nsew")
        
        ctk.CTkLabel(self.r_sidebar, text="ÖĞRENCİ KARTI", font=("Arial", 14, "bold"), text_color="#2198A1").pack(pady=(40, 20))
        
        self.avatar = ctk.CTkFrame(self.r_sidebar, width=80, height=80, corner_radius=40, fg_color="#2198A1")
        self.avatar.pack(pady=10)
        ctk.CTkLabel(self.avatar, text=self.aktif_ogrenci.ad[0].upper(), font=("Arial", 30, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        info_card = ctk.CTkFrame(self.r_sidebar, fg_color="#282828", corner_radius=15)
        info_card.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(info_card, text="AD SOYAD", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(15, 0), padx=15, anchor="w")
        ctk.CTkLabel(info_card, text=self.aktif_ogrenci.ad, font=("Arial", 14, "bold"), text_color="white").pack(padx=15, anchor="w")
        
        ctk.CTkLabel(info_card, text="ÖĞRENCİ NO", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 0), padx=15, anchor="w")
        ctk.CTkLabel(info_card, text=f"#{self.aktif_ogrenci.ogrenci_id}", font=("Arial", 13), text_color="#2198A1").pack(padx=15, anchor="w")
        
        ctk.CTkLabel(info_card, text="E-POSTA", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 0), padx=15, anchor="w")
        ctk.CTkLabel(info_card, text=self.aktif_ogrenci.email, font=("Arial", 11), text_color="#aaaaaa").pack(pady=(0, 15), padx=15, anchor="w")

        stats_frame = ctk.CTkFrame(self.r_sidebar, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20)
        
        self.course_count_lbl = ctk.CTkLabel(stats_frame, text="Kayıtlı Kurslar: 0", font=("Arial", 12), text_color="white")
        self.course_count_lbl.pack(pady=5, anchor="w")
        
        ctk.CTkProgressBar(stats_frame, width=200, height=8, progress_color="#2198A1").pack(pady=5)

    def create_home(self):
        """Ana sayfa tasarımını oluşturur."""
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        f.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        ctk.CTkLabel(f, text="Eğitim Kataloğu", font=("Arial", 24, "bold"), text_color="#1a1a1a").pack(anchor="w", pady=(0, 20))
        
        scroll = ctk.CTkScrollableFrame(f, fg_color="transparent", height=500)
        scroll.pack(fill="both", expand=True)

        for k in self.kurslar:
            card = ctk.CTkFrame(scroll, fg_color="#f8f8f8", border_width=1, border_color="#eeeeee", corner_radius=12)
            card.pack(fill="x", pady=8, padx=5)
            
            txt = f"{k.kurs_adi}\n{k.egitmen.ad} - Kontenjan: {k.kontenjan}"
            ctk.CTkLabel(card, text=txt, text_color="#333", font=("Arial", 13), justify="left").pack(side="left", padx=20, pady=15)
            
            btn = ctk.CTkButton(card, text="Kayıt Ol", width=90, height=32, fg_color="#2198A1", corner_radius=8,
                                command=lambda x=k: self.kayit_yap(x))
            btn.pack(side="right", padx=20)
        return f

    def create_lessons(self):
        """Öğrencinin kendi kurslarını gördüğü paneli oluşturur."""
        self.l_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.l_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.update_lessons()
        return self.l_frame

    def kayit_yap(self, kurs):
        """Ders kayıt metodunu tetikler ve geri bildirim verir."""
        ok, msg = kurs.ogrenci_kaydet(self.aktif_ogrenci)
        messagebox.showinfo("Sistem Mesajı", msg)
        if ok:
            self.course_count_lbl.configure(text=f"Kayıtlı Kurslar: {len(self.aktif_ogrenci.kayitli_kurslar)}")
            self.update_lessons()

    def update_lessons(self):
        """Kayıtlı kurslar sayfasını dinamik olarak yeniler."""
        for w in self.l_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.l_frame, text="Öğrenim Panelim", font=("Arial", 24, "bold"), text_color="#1a1a1a").pack(anchor="w", pady=(0, 20))
        
        if not self.aktif_ogrenci.kayitli_kurslar:
            ctk.CTkLabel(self.l_frame, text="Henüz bir kursa kayıt olmadınız.", text_color="gray", font=("Arial", 14)).pack(pady=50)
        else:
            for k in self.aktif_ogrenci.kayitli_kurslar:
                item = ctk.CTkFrame(self.l_frame, fg_color="#f0f9fa", border_width=1, border_color="#2198A1", corner_radius=10)
                item.pack(fill="x", pady=5)
                ctk.CTkLabel(item, text=f"📘 {k.kurs_adi}", text_color="#1a1a1a", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=15)
                ctk.CTkButton(item, text="Derse Git", width=80, fg_color="#2198A1").pack(side="right", padx=20)

    def show_page(self, p):
        """Sayfa geçişlerini yönetir."""
        self.pages[p].tkraise()
        self.btn_home.configure(fg_color="#2198A1" if p == "home" else "transparent")
        self.btn_list.configure(fg_color="#2198A1" if p == "lessons" else "transparent")

# ==========================================
# 3. GİRİŞ EKRANI VE ANA AKIŞ
# ==========================================

class GirisEkrani(ctk.CTk):
    """Programın başlangıç noktasını (Giriş) temsil eder."""
    def __init__(self):
        super().__init__()
        self.title("İKÜ Uzaktan Eğitrim Portal Giriş")
        self.geometry("400x500")
        self.configure(fg_color="#1e1e1e")
        
        ctk.CTkLabel(self, text="İKÜ", font=("Arial", 40, "bold"), text_color="#2198A1").pack(pady=(50, 5))
        ctk.CTkLabel(self, text="Uzaktan Eğitim Portal Girişi", font=("Arial", 14), text_color="gray").pack(pady=(0, 30))
        
        self.e_id = ctk.CTkEntry(self, placeholder_text="Öğrenci Numarası", width=280, height=40)
        self.e_id.pack(pady=10)
        
        self.e_ad = ctk.CTkEntry(self, placeholder_text="Ad Soyad", width=280, height=40)
        self.e_ad.pack(pady=10)
        
        self.e_mail = ctk.CTkEntry(self, placeholder_text="E-posta", width=280, height=40)
        self.e_mail.pack(pady=10)
        
        ctk.CTkButton(self, text="Sisteme Giriş Yap", width=280, height=45, fg_color="#2198A1", font=("Arial", 14, "bold"),
                      command=self.giris_yap).pack(pady=30)

    def giris_yap(self):
        """Giriş bilgilerini doğrular ve ana uygulamayı başlatır."""
        if self.e_id.get() and self.e_ad.get() and self.e_mail.get():
            # VERİ YAPISI: Kullanıcı bilgileri Sözlük (Dictionary) formatında paketlenir
            data = {
                "id": self.e_id.get(), 
                "ad": self.e_ad.get(), 
                "email": self.e_mail.get()
            }
            self.destroy() # Giriş penceresini kapatır
            app = Uygulama(data) # Ana akışı başlatır
            app.mainloop()
        else:
            messagebox.showerror("Giriş Hatası", "Lütfen tüm alanları eksiksiz giriniz!")

# PROGRAMIN ÇALIŞTIRILMASI
if __name__ == "__main__":
    login_screen = GirisEkrani()
    login_screen.mainloop()
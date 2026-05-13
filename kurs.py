import re
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import random

# ============================================================
# 1. VERİ MODELİ (OOP)
# ============================================================

class Egitmen:
    """Eğitmen bilgilerini ve unvanını tutan sınıf."""
    def __init__(self, ad, uzmanlik, unvan="Dr."):
        self.ad = ad
        self.uzmanlik = uzmanlik
        self.unvan = unvan

    @property
    def tam_ad(self):
        return f"{self.unvan} {self.ad}"


class Kurs:
    """Bir kursu, eğitmenini ve kayıt işlemlerini yöneten sınıf."""

    KATEGORI_RENK = {
        "Yazılım":    "#2198A1",
        "Yapay Zeka": "#9B59B6",
        "Matematik":  "#E67E22",
        "Fizik":      "#27AE60",
        "Siber":      "#E74C3C",
        "Tasarım":    "#E91E8C",
        "Diğer":      "#607D8B",
    }

    def __init__(self, kurs_id, kurs_adi, egitmen, kontenjan,
                 kategori="Diğer", seviye="Başlangıç", sure_saat=30, puan=4.5):
        self.kurs_id = kurs_id
        self.kurs_adi = kurs_adi
        self.egitmen = egitmen
        self.kontenjan = kontenjan
        self.kategori = kategori
        self.seviye = seviye          # Başlangıç / Orta / İleri
        self.sure_saat = sure_saat    # Tahmini ders saati
        self.puan = puan              # Kurs puanı (1-5)
        self.kayitli_ogrenciler = []
        self.ders_sayisi = random.randint(8, 24)

    @property
    def dolu_mu(self):
        return len(self.kayitli_ogrenciler) >= self.kontenjan

    @property
    def doluluk_orani(self):
        return len(self.kayitli_ogrenciler) / self.kontenjan

    @property
    def bos_kontenjan(self):
        return self.kontenjan - len(self.kayitli_ogrenciler)

    @property
    def renk(self):
        return self.KATEGORI_RENK.get(self.kategori, "#607D8B")

    def ogrenci_kaydet(self, ogrenci):
        if self.dolu_mu:
            return False, "Kontenjan dolu! Bu kursa kayıt yapılamıyor."
        if ogrenci in self.kayitli_ogrenciler:
            return False, "Bu kursa zaten kayıtlısınız."
        self.kayitli_ogrenciler.append(ogrenci)
        ogrenci.kayitli_kurslar.append(self)
        ogrenci.toplam_saat += self.sure_saat
        return True, f"'{self.kurs_adi}' kursuna başarıyla kayıt oldunuz!"

    def ogrenci_birak(self, ogrenci):
        if ogrenci in self.kayitli_ogrenciler:
            self.kayitli_ogrenciler.remove(ogrenci)
            ogrenci.kayitli_kurslar.remove(self)
            ogrenci.toplam_saat -= self.sure_saat
            return True, f"'{self.kurs_adi}' kursundan ayrıldınız."
        return False, "Bu kursa kayıtlı değilsiniz."

    def yildiz_str(self):
        tam = int(self.puan)
        return "★" * tam + "☆" * (5 - tam)


class Ogrenci:
    """Sisteme giriş yapan kullanıcı."""
    def __init__(self, ogrenci_id, ad, email, bolum="Belirtilmedi"):
        self.ogrenci_id = ogrenci_id
        self.ad = ad
        self.email = email
        self.bolum = bolum
        self.kayitli_kurslar = []
        self.toplam_saat = 0
        self.kayit_tarihi = datetime.now().strftime("%d.%m.%Y")

    @property
    def ilerleme_yuzdesi(self):
        """Kayıtlı kurs sayısına göre basit ilerleme skoru."""
        return min(len(self.kayitli_kurslar) * 16, 100)

    def kurs_listesi(self):
        return [k.kurs_adi for k in self.kayitli_kurslar]

    def initials(self):
        parcalar = self.ad.strip().split()
        if len(parcalar) >= 2:
            return parcalar[0][0].upper() + parcalar[-1][0].upper()
        return self.ad[0].upper()


# ============================================================
# 2. YENİDEN KULLANILABİLİR BİLEŞENLER
# ============================================================

TEMA = {
    "bg":        "#0A0F1E",
    "panel":     "#111827",
    "kart":      "#1A2233",
    "kart2":     "#1E293B",
    "accent":    "#2198A1",
    "accent2":   "#17B3BE",
    "yazi":      "#E2E8F0",
    "yazi2":     "#94A3B8",
    "yazi3":     "#475569",
    "basari":    "#10B981",
    "uyari":     "#F59E0B",
    "hata":      "#EF4444",
    "sinir":     "#1E293B",
}


def _ayrac(parent, dikey=10):
    ctk.CTkFrame(parent, height=1, fg_color=TEMA["sinir"]).pack(
        fill="x", padx=20, pady=dikey)


class KursKarti(ctk.CTkFrame):
    """Katalog sayfasında tek bir kursu gösteren bileşen."""
    def __init__(self, master, kurs, kayitli_mi, on_kayit, on_birak, **kw):
        super().__init__(master, fg_color=TEMA["kart"], corner_radius=14,
                         border_width=1, border_color=TEMA["sinir"], **kw)
        self._build(kurs, kayitli_mi, on_kayit, on_birak)

    def _build(self, k, kayitli_mi, on_kayit, on_birak):
        # Sol renkli şerit
        bar = ctk.CTkFrame(self, width=4, fg_color=k.renk, corner_radius=0)
        bar.pack(side="left", fill="y")

        # İçerik
        ic = ctk.CTkFrame(self, fg_color="transparent")
        ic.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        # Üst satır: kategori badge + seviye
        ust = ctk.CTkFrame(ic, fg_color="transparent")
        ust.pack(fill="x")

        kat_f = ctk.CTkFrame(ust, fg_color=TEMA["kart2"], corner_radius=6)
        kat_f.pack(side="left")
        ctk.CTkLabel(kat_f, text=f"  {k.kategori}  ",
                     font=("Trebuchet MS", 10, "bold"),
                     text_color=k.renk).pack(padx=2, pady=2)

        sev_renkler = {"Başlangıç": TEMA["basari"], "Orta": TEMA["uyari"], "İleri": TEMA["hata"]}
        sev_f = ctk.CTkFrame(ust, fg_color=TEMA["kart2"], corner_radius=6)
        sev_f.pack(side="left", padx=8)
        ctk.CTkLabel(sev_f, text=f"  {k.seviye}  ",
                     font=("Trebuchet MS", 10, "bold"),
                     text_color=sev_renkler.get(k.seviye, TEMA["yazi2"])).pack(padx=2, pady=2)

        if kayitli_mi:
            r_f = ctk.CTkFrame(ust, fg_color=TEMA["kart2"], corner_radius=6)
            r_f.pack(side="left", padx=4)
            ctk.CTkLabel(r_f, text="  ✓ Kayıtlı  ",
                         font=("Trebuchet MS", 10, "bold"),
                         text_color=TEMA["basari"]).pack(padx=2, pady=2)

        # Kurs adı
        ctk.CTkLabel(ic, text=k.kurs_adi, font=("Georgia", 15, "bold"),
                     text_color=TEMA["yazi"], anchor="w").pack(anchor="w", pady=(6, 2))

        # Eğitmen
        ctk.CTkLabel(ic, text=f"👤  {k.egitmen.tam_ad}  ·  {k.egitmen.uzmanlik}",
                     font=("Trebuchet MS", 11),
                     text_color=TEMA["yazi2"], anchor="w").pack(anchor="w")

        # Alt bilgi çubuğu
        alt = ctk.CTkFrame(ic, fg_color="transparent")
        alt.pack(fill="x", pady=(8, 0))

        for ikon, deger in [
            ("⏱", f"{k.sure_saat}s"),
            ("📖", f"{k.ders_sayisi} ders"),
            ("👥", f"{k.bos_kontenjan}/{k.kontenjan}"),
            ("★", k.yildiz_str()),
        ]:
            bl = ctk.CTkFrame(alt, fg_color="transparent")
            bl.pack(side="left", padx=(0, 16))
            ctk.CTkLabel(bl, text=f"{ikon} {deger}",
                         font=("Trebuchet MS", 10),
                         text_color=TEMA["yazi3"]).pack()

        # Sağ taraf: buton
        sag = ctk.CTkFrame(self, fg_color="transparent")
        sag.pack(side="right", padx=20, pady=14)

        if kayitli_mi:
            ctk.CTkButton(sag, text="Bırak", width=88, height=34,
                          fg_color=TEMA["kart2"], hover_color=TEMA["sinir"],
                          border_width=1, border_color=TEMA["hata"],
                          font=("Trebuchet MS", 11, "bold"),
                          text_color=TEMA["hata"], corner_radius=8,
                          command=lambda: on_birak(k)).pack()
        elif k.dolu_mu:
            ctk.CTkLabel(sag, text="Dolu", font=("Trebuchet MS", 11),
                         text_color=TEMA["yazi3"]).pack()
        else:
            ctk.CTkButton(sag, text="Kayıt Ol", width=88, height=34,
                          fg_color=TEMA["accent"], hover_color=TEMA["accent2"],
                          font=("Trebuchet MS", 11, "bold"),
                          text_color="white", corner_radius=8,
                          command=lambda: on_kayit(k)).pack()


class DersKarti(ctk.CTkFrame):
    """'Derslerim' sayfasında kayıtlı kursu gösteren bileşen."""
    def __init__(self, master, kurs, on_birak, index, **kw):
        super().__init__(master, fg_color=TEMA["kart"], corner_radius=14,
                         border_width=1, border_color=TEMA["sinir"], **kw)
        self._build(kurs, on_birak, index)

    def _build(self, k, on_birak, idx):
        bar = ctk.CTkFrame(self, width=4, fg_color=k.renk, corner_radius=0)
        bar.pack(side="left", fill="y")

        ic = ctk.CTkFrame(self, fg_color="transparent")
        ic.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        ctk.CTkLabel(ic, text=k.kurs_adi, font=("Georgia", 14, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w")
        ctk.CTkLabel(ic, text=f"👤 {k.egitmen.tam_ad}",
                     font=("Trebuchet MS", 11),
                     text_color=TEMA["yazi2"]).pack(anchor="w", pady=(2, 6))

        # İlerleme çubuğu (sahte ama görsel)
        ilerleme = (idx * 37 + 21) % 101
        ctk.CTkLabel(ic, text=f"İlerleme  {ilerleme}%",
                     font=("Trebuchet MS", 10),
                     text_color=TEMA["yazi3"]).pack(anchor="w")
        bar2 = ctk.CTkProgressBar(ic, width=260, height=6,
                                   progress_color=k.renk,
                                   fg_color=TEMA["kart2"], corner_radius=3)
        bar2.pack(anchor="w", pady=(3, 0))
        bar2.set(ilerleme / 100)

        sag = ctk.CTkFrame(self, fg_color="transparent")
        sag.pack(side="right", padx=20, pady=14)

        ctk.CTkButton(sag, text="Devam Et →", width=100, height=34,
                      fg_color=k.renk, hover_color=TEMA["kart2"],
                      font=("Trebuchet MS", 11, "bold"),
                      text_color="white", corner_radius=8,
                      command=lambda: messagebox.showinfo(
                          "Ders", f"'{k.kurs_adi}' dersine hoş geldiniz! 🎓")).pack(pady=(0, 6))
        ctk.CTkButton(sag, text="Bırak", width=100, height=28,
                      fg_color="transparent", hover_color=TEMA["kart2"],
                      font=("Trebuchet MS", 10), text_color=TEMA["yazi3"],
                      corner_radius=8, border_width=1, border_color=TEMA["sinir"],
                      command=lambda: on_birak(k)).pack()


# ============================================================
# 3. ANA UYGULAMA
# ============================================================

class Uygulama(ctk.CTk):
    def __init__(self, ogrenci_verisi):
        super().__init__()
        ctk.set_appearance_mode("dark")

        self.aktif_ogrenci = Ogrenci(
            ogrenci_verisi['id'],
            ogrenci_verisi['ad'],
            ogrenci_verisi['email'],
            ogrenci_verisi.get('bolum', 'Belirtilmedi')
        )

        self.title(f"İKÜ LYS  ·  {self.aktif_ogrenci.ad}")
        self.geometry("1360x800")
        self.minsize(1100, 680)
        self.configure(fg_color=TEMA["bg"])

        self._filtre_kategori = "Tümü"
        self._filtre_seviye   = "Tümü"
        self._arama_str       = ""

        self._veri_hazirla()
        self._build_layout()
        self.show_page("home")

    # ── Veri ─────────────────────────────────────────────────
    def _veri_hazirla(self):
        e1 = Egitmen("Ahmet Yılmaz",         "Yazılım",    "Dr.")
        e2 = Egitmen("Elif Aksu",            "Yapay Zeka", "Prof. Dr.")
        e3 = Egitmen("Bade Türk",            "Matematik",  "Dr.")
        e4 = Egitmen("Muhammed Aled Ora",    "Fizik",      "Prof. Dr.")
        e5 = Egitmen("Selin Çelik",          "Siber",      "Uzm.")
        e6 = Egitmen("Tarık Özbek",          "Tasarım",    "Dr.")

        self.kurslar = [
            Kurs(101, "Python Programlama",          e1, 20, "Yazılım",    "Başlangıç", 32, 4.8),
            Kurs(102, "Veri Yapıları ve Algoritmalar",e1, 30, "Yazılım",   "Orta",      40, 4.6),
            Kurs(103, "Derin Öğrenme",               e2, 15, "Yapay Zeka", "İleri",     50, 4.9),
            Kurs(104, "Makine Öğrenmesi",             e2, 20, "Yapay Zeka", "Orta",     38, 4.7),
            Kurs(105, "Siber Güvenlik Temelleri",     e5, 10, "Siber",     "Başlangıç", 28, 4.5),
            Kurs(106, "Etik Hacking",                 e5, 10, "Siber",     "İleri",     36, 4.4),
            Kurs(107, "Calculus I",                   e3, 90, "Matematik", "Başlangıç", 42, 4.3),
            Kurs(108, "Lineer Cebir",                 e3, 90, "Matematik", "Orta",      38, 4.2),
            Kurs(109, "Fizik III",                    e4, 90, "Fizik",     "Orta",      44, 4.1),
            Kurs(110, "Kuantum Mekaniği",             e4, 30, "Fizik",     "İleri",     50, 4.6),
            Kurs(111, "UI/UX Tasarım",                e6, 25, "Tasarım",   "Başlangıç", 22, 4.7),
            Kurs(112, "Figma ile Prototip",           e6, 20, "Tasarım",   "Orta",      18, 4.5),
        ]

    # ── Layout ───────────────────────────────────────────────
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()
        self._build_profile()

    # ── Sol Sidebar ──────────────────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=230, fg_color=TEMA["panel"], corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # Logo
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(pady=(36, 8), padx=24, anchor="w")
        ctk.CTkLabel(logo, text="İKÜ", font=("Georgia", 26, "bold"),
                     text_color=TEMA["accent"]).pack(side="left")
        ctk.CTkLabel(logo, text=" LYS", font=("Georgia", 18),
                     text_color=TEMA["yazi"]).pack(side="left", pady=(5, 0))

        ctk.CTkLabel(sb, text="Uzaktan Eğitim Portalı",
                     font=("Trebuchet MS", 10),
                     text_color=TEMA["yazi3"]).pack(anchor="w", padx=24, pady=(0, 16))

        _ayrac(sb, 0)

        ctk.CTkLabel(sb, text="GEZINME", font=("Trebuchet MS", 9, "bold"),
                     text_color=TEMA["yazi3"]).pack(anchor="w", padx=24, pady=(16, 8))

        self._menu_btns = {}
        menüler = [
            ("home",      "🏠", "Ana Sayfa"),
            ("catalog",   "🗂", "Kurs Kataloğu"),
            ("lessons",   "📘", "Derslerim"),
            ("takvim",    "📅", "Akademik Takvim"),
            ("istatistik","📊", "İstatistiklerim"),
        ]
        for key, icon, label in menüler:
            btn = ctk.CTkButton(
                sb, text=f"  {icon}  {label}", anchor="w",
                fg_color="transparent", hover_color=TEMA["kart"],
                font=("Trebuchet MS", 12), text_color=TEMA["yazi2"],
                corner_radius=10, height=40,
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=14, pady=2)
            self._menu_btns[key] = btn

        # Alt
        ctk.CTkLabel(sb, text="İstanbul Kültür Üniversitesi\nSürüm 2.0",
                     font=("Trebuchet MS", 9), text_color=TEMA["yazi3"],
                     justify="center").place(relx=0.5, rely=0.97, anchor="s")

    # ── İçerik Alanı ────────────────────────────────────────
    def _build_content(self):
        self.container = ctk.CTkFrame(self, fg_color=TEMA["bg"], corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")

        self.pages = {
            "home":       self._page_home(),
            "catalog":    self._page_catalog(),
            "lessons":    self._page_lessons(),
            "takvim":     self._page_takvim(),
            "istatistik": self._page_istatistik(),
        }

    # ── Sağ Profil Paneli ───────────────────────────────────
    def _build_profile(self):
        rp = ctk.CTkFrame(self, width=280, fg_color=TEMA["panel"], corner_radius=0)
        rp.grid(row=0, column=2, sticky="nsew")
        rp.grid_propagate(False)

        ctk.CTkLabel(rp, text="PROFİL", font=("Trebuchet MS", 9, "bold"),
                     text_color=TEMA["yazi3"]).pack(pady=(36, 14))

        # Avatar
        av = ctk.CTkFrame(rp, width=76, height=76, corner_radius=38,
                          fg_color=TEMA["accent"])
        av.pack()
        av.pack_propagate(False)
        ctk.CTkLabel(av, text=self.aktif_ogrenci.initials(),
                     font=("Georgia", 26, "bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(rp, text=self.aktif_ogrenci.ad,
                     font=("Georgia", 15, "bold"),
                     text_color=TEMA["yazi"]).pack(pady=(10, 2))
        ctk.CTkLabel(rp, text=self.aktif_ogrenci.email,
                     font=("Trebuchet MS", 10),
                     text_color=TEMA["yazi3"]).pack()

        _ayrac(rp, 14)

        # Stat kartları
        sg = ctk.CTkFrame(rp, fg_color="transparent")
        sg.pack(fill="x", padx=16)
        sg.columnconfigure((0, 1), weight=1)

        self._stat_kurs_lbl  = self._stat_kart(sg, "Kayıtlı Kurs", "0", TEMA["accent"], 0)
        self._stat_saat_lbl  = self._stat_kart(sg, "Toplam Saat",  "0", TEMA["basari"], 1)

        _ayrac(rp, 14)

        # İlerleme
        ctk.CTkLabel(rp, text="Genel İlerleme",
                     font=("Trebuchet MS", 10, "bold"),
                     text_color=TEMA["yazi2"]).pack(anchor="w", padx=20)
        self._prog_lbl = ctk.CTkLabel(rp, text="0%",
                                       font=("Trebuchet MS", 10),
                                       text_color=TEMA["yazi3"])
        self._prog_lbl.pack(anchor="e", padx=20)
        self._prog_bar = ctk.CTkProgressBar(rp, width=230, height=8,
                                             progress_color=TEMA["accent"],
                                             fg_color=TEMA["kart"], corner_radius=4)
        self._prog_bar.pack(pady=(2, 0))
        self._prog_bar.set(0)

        _ayrac(rp, 14)

        # Kimlik
        id_f = ctk.CTkFrame(rp, fg_color=TEMA["kart"], corner_radius=12)
        id_f.pack(fill="x", padx=16)
        ctk.CTkLabel(id_f, text="ÖĞRENCİ NO",
                     font=("Trebuchet MS", 9, "bold"),
                     text_color=TEMA["yazi3"]).pack(pady=(10, 2))
        ctk.CTkLabel(id_f, text=f"#{self.aktif_ogrenci.ogrenci_id}",
                     font=("Courier", 22, "bold"),
                     text_color=TEMA["accent"]).pack(pady=(0, 4))
        ctk.CTkLabel(id_f, text=f"Kayıt: {self.aktif_ogrenci.kayit_tarihi}",
                     font=("Trebuchet MS", 9),
                     text_color=TEMA["yazi3"]).pack(pady=(0, 10))

    def _stat_kart(self, parent, etiket, deger, renk, sutun):
        k = ctk.CTkFrame(parent, fg_color=TEMA["kart"], corner_radius=12)
        k.grid(row=0, column=sutun, padx=4, pady=4, sticky="ew")
        lbl = ctk.CTkLabel(k, text=deger, font=("Georgia", 22, "bold"),
                           text_color=renk)
        lbl.pack(pady=(12, 2))
        ctk.CTkLabel(k, text=etiket, font=("Trebuchet MS", 9),
                     text_color=TEMA["yazi3"]).pack(pady=(0, 10))
        return lbl

    # ============================================================
    # 4. SAYFA TASARIMLARI
    # ============================================================

    def _page_home(self):
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        f.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Karşılama banner
        banner = ctk.CTkFrame(f, fg_color=TEMA["panel"], corner_radius=16,
                              border_width=1, border_color=TEMA["sinir"])
        banner.pack(fill="x", padx=30, pady=(30, 0))

        ic = ctk.CTkFrame(banner, fg_color="transparent")
        ic.pack(side="left", padx=30, pady=24)
        ctk.CTkLabel(ic, text=f"Hoş geldiniz, {self.aktif_ogrenci.ad.split()[0]}! 👋",
                     font=("Georgia", 22, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w")
        ctk.CTkLabel(ic, text="Bugün yeni bir şeyler öğrenmeye hazır mısınız?",
                     font=("Trebuchet MS", 12),
                     text_color=TEMA["yazi2"]).pack(anchor="w", pady=(4, 0))

        sag = ctk.CTkFrame(banner, fg_color=TEMA["kart"], corner_radius=12)
        sag.pack(side="right", padx=24, pady=16)
        ctk.CTkLabel(sag, text=datetime.now().strftime("%d %B %Y"),
                     font=("Trebuchet MS", 11, "bold"),
                     text_color=TEMA["accent"]).pack(padx=20, pady=(12, 2))
        ctk.CTkLabel(sag, text=datetime.now().strftime("%A"),
                     font=("Trebuchet MS", 10),
                     text_color=TEMA["yazi3"]).pack(padx=20, pady=(0, 12))

        # Hızlı istatistikler
        qs = ctk.CTkFrame(f, fg_color="transparent")
        qs.pack(fill="x", padx=30, pady=20)
        qs.columnconfigure((0, 1, 2, 3), weight=1)

        for i, (ikon, lbl, deger, renk) in enumerate([
            ("🗂", "Toplam Kurs",   str(len(self.kurslar)),  TEMA["accent"]),
            ("✅", "Kayıtlı",      "0",                      TEMA["basari"]),
            ("⏱", "Toplam Saat",  "0s",                     TEMA["uyari"]),
            ("🏆", "Seviye",       "Yeni",                   "#9B59B6"),
        ]):
            kart = ctk.CTkFrame(qs, fg_color=TEMA["panel"], corner_radius=14,
                                border_width=1, border_color=TEMA["sinir"])
            kart.grid(row=0, column=i, padx=6, sticky="ew")
            ctk.CTkLabel(kart, text=ikon, font=("Trebuchet MS", 22)).pack(pady=(16, 4))
            val = ctk.CTkLabel(kart, text=deger, font=("Georgia", 20, "bold"),
                               text_color=renk)
            val.pack()
            ctk.CTkLabel(kart, text=lbl, font=("Trebuchet MS", 10),
                         text_color=TEMA["yazi3"]).pack(pady=(2, 14))
            # Dinamik güncelleme için referans
            if lbl == "Kayıtlı":
                self._home_kayitli_lbl = val
            elif lbl == "Toplam Saat":
                self._home_saat_lbl = val

        # Önerilen kurslar
        ctk.CTkLabel(f, text="Önerilen Kurslar",
                     font=("Georgia", 18, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w", padx=30, pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                         scrollbar_button_color=TEMA["sinir"])
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for k in self.kurslar[:4]:
            KursKarti(scroll, k,
                      kayitli_mi=(k in self.aktif_ogrenci.kayitli_kurslar),
                      on_kayit=self._action_kayit,
                      on_birak=self._action_birak).pack(fill="x", pady=4, padx=4)

        return f

    def _page_catalog(self):
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        f.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Başlık + Filtreler
        hdr = ctk.CTkFrame(f, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(30, 0))
        ctk.CTkLabel(hdr, text="Kurs Kataloğu",
                     font=("Georgia", 24, "bold"),
                     text_color=TEMA["yazi"]).pack(side="left")

        # Arama
        self._arama_var = ctk.StringVar()
        self._arama_var.trace_add("write", lambda *_: self._refresh_catalog())
        arama = ctk.CTkEntry(hdr, placeholder_text="🔍 Kurs veya eğitmen ara...",
                             width=240, height=36, corner_radius=10,
                             fg_color=TEMA["kart"], border_color=TEMA["sinir"],
                             text_color=TEMA["yazi"],
                             textvariable=self._arama_var)
        arama.pack(side="right", padx=(8, 0))

        # Filtre satırı
        fil = ctk.CTkFrame(f, fg_color="transparent")
        fil.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(fil, text="Kategori:", font=("Trebuchet MS", 11),
                     text_color=TEMA["yazi2"]).pack(side="left")
        self._kat_var = ctk.StringVar(value="Tümü")
        self._kat_var.trace_add("write", lambda *_: self._refresh_catalog())
        kat_menu = ctk.CTkOptionMenu(fil, values=["Tümü", "Yazılım", "Yapay Zeka",
                                                   "Matematik", "Fizik", "Siber", "Tasarım"],
                                     variable=self._kat_var,
                                     fg_color=TEMA["kart"], button_color=TEMA["accent"],
                                     dropdown_fg_color=TEMA["kart"],
                                     text_color=TEMA["yazi"],
                                     font=("Trebuchet MS", 11), width=130)
        kat_menu.pack(side="left", padx=(6, 16))

        ctk.CTkLabel(fil, text="Seviye:", font=("Trebuchet MS", 11),
                     text_color=TEMA["yazi2"]).pack(side="left")
        self._sev_var = ctk.StringVar(value="Tümü")
        self._sev_var.trace_add("write", lambda *_: self._refresh_catalog())
        sev_menu = ctk.CTkOptionMenu(fil, values=["Tümü", "Başlangıç", "Orta", "İleri"],
                                     variable=self._sev_var,
                                     fg_color=TEMA["kart"], button_color=TEMA["accent"],
                                     dropdown_fg_color=TEMA["kart"],
                                     text_color=TEMA["yazi"],
                                     font=("Trebuchet MS", 11), width=120)
        sev_menu.pack(side="left", padx=6)

        self._katalog_sayac = ctk.CTkLabel(fil, text="",
                                            font=("Trebuchet MS", 10),
                                            text_color=TEMA["yazi3"])
        self._katalog_sayac.pack(side="right")

        self._katalog_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                       scrollbar_button_color=TEMA["sinir"])
        self._katalog_scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self._refresh_catalog()
        return f

    def _refresh_catalog(self):
        for w in self._katalog_scroll.winfo_children():
            w.destroy()
        arama = self._arama_var.get().lower() if hasattr(self, '_arama_var') else ""
        kat   = self._kat_var.get()   if hasattr(self, '_kat_var')   else "Tümü"
        sev   = self._sev_var.get()   if hasattr(self, '_sev_var')   else "Tümü"

        sonuc = [k for k in self.kurslar
                 if (arama in k.kurs_adi.lower() or arama in k.egitmen.ad.lower())
                 and (kat == "Tümü" or k.kategori == kat)
                 and (sev == "Tümü" or k.seviye == sev)]

        self._katalog_sayac.configure(text=f"{len(sonuc)} kurs listeleniyor")

        if not sonuc:
            ctk.CTkLabel(self._katalog_scroll, text="Arama kriterlerine uygun kurs bulunamadı.",
                         font=("Trebuchet MS", 13),
                         text_color=TEMA["yazi3"]).pack(pady=60)
            return

        for k in sonuc:
            KursKarti(self._katalog_scroll, k,
                      kayitli_mi=(k in self.aktif_ogrenci.kayitli_kurslar),
                      on_kayit=self._action_kayit,
                      on_birak=self._action_birak).pack(fill="x", pady=4, padx=4)

    def _page_lessons(self):
        self._lessons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self._lessons_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._refresh_lessons()
        return self._lessons_frame

    def _refresh_lessons(self):
        for w in self._lessons_frame.winfo_children():
            w.destroy()

        hdr = ctk.CTkFrame(self._lessons_frame, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(30, 5))
        ctk.CTkLabel(hdr, text="Derslerim",
                     font=("Georgia", 24, "bold"),
                     text_color=TEMA["yazi"]).pack(side="left")
        ctk.CTkLabel(hdr, text=f"{len(self.aktif_ogrenci.kayitli_kurslar)} kurs kayıtlı",
                     font=("Trebuchet MS", 11),
                     text_color=TEMA["accent"]).pack(side="right", pady=8)

        if not self.aktif_ogrenci.kayitli_kurslar:
            bos = ctk.CTkFrame(self._lessons_frame, fg_color="transparent")
            bos.pack(expand=True)
            ctk.CTkLabel(bos, text="📭", font=("Trebuchet MS", 56)).pack()
            ctk.CTkLabel(bos, text="Henüz hiçbir kursa kayıt olmadınız.",
                         font=("Trebuchet MS", 14),
                         text_color=TEMA["yazi2"]).pack(pady=8)
            ctk.CTkButton(bos, text="Kataloğa Git", width=140, height=36,
                          fg_color=TEMA["accent"], hover_color=TEMA["accent2"],
                          font=("Trebuchet MS", 12, "bold"), corner_radius=8,
                          command=lambda: self.show_page("catalog")).pack(pady=4)
        else:
            scroll = ctk.CTkScrollableFrame(self._lessons_frame, fg_color="transparent",
                                             scrollbar_button_color=TEMA["sinir"])
            scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))
            for i, k in enumerate(self.aktif_ogrenci.kayitli_kurslar):
                DersKarti(scroll, k, self._action_birak, i).pack(
                    fill="x", pady=4, padx=4)

    def _page_takvim(self):
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        f.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(f, text="Akademik Takvim",
                     font=("Georgia", 24, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w", padx=30, pady=(30, 20))

        etkinlikler = [
            ("10 Şubat 2025", "Bahar Dönemi Başlangıcı",       TEMA["basari"]),
            ("14 Şubat 2025", "Ders Ekleme-Bırakma Sonu",      TEMA["uyari"]),
            ("21-25 Nisan",   "Ara Sınavlar",                   TEMA["hata"]),
            ("19 Mayıs",      "19 Mayıs Tatili",                TEMA["accent"]),
            ("9-20 Haziran",  "Final Sınavları",                TEMA["hata"]),
            ("27 Haziran",    "Bahar Dönemi Sonu",              TEMA["yazi3"]),
        ]

        scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                         scrollbar_button_color=TEMA["sinir"])
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for tarih, etiket, renk in etkinlikler:
            row = ctk.CTkFrame(scroll, fg_color=TEMA["kart"], corner_radius=12,
                               border_width=1, border_color=TEMA["sinir"])
            row.pack(fill="x", pady=4, padx=4)

            bar = ctk.CTkFrame(row, width=4, fg_color=renk, corner_radius=0)
            bar.pack(side="left", fill="y")

            ic = ctk.CTkFrame(row, fg_color="transparent")
            ic.pack(side="left", padx=16, pady=12)
            ctk.CTkLabel(ic, text=etiket, font=("Georgia", 13, "bold"),
                         text_color=TEMA["yazi"]).pack(anchor="w")
            ctk.CTkLabel(ic, text=f"📅  {tarih}", font=("Trebuchet MS", 11),
                         text_color=TEMA["yazi3"]).pack(anchor="w", pady=(2, 0))

        return f

    def _page_istatistik(self):
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        f.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(f, text="İstatistiklerim",
                     font=("Georgia", 24, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w", padx=30, pady=(30, 20))

        # Kategori dağılımı
        ctk.CTkLabel(f, text="Kategori Dağılımı",
                     font=("Trebuchet MS", 13, "bold"),
                     text_color=TEMA["yazi2"]).pack(anchor="w", padx=30)

        self._istat_scroll = ctk.CTkScrollableFrame(f, fg_color="transparent",
                                                     scrollbar_button_color=TEMA["sinir"])
        self._istat_scroll.pack(fill="both", expand=True, padx=24, pady=10)
        self._refresh_istatistik()
        return f

    def _refresh_istatistik(self):
        for w in self._istat_scroll.winfo_children():
            w.destroy()

        sayim = {}
        for k in self.aktif_ogrenci.kayitli_kurslar:
            sayim[k.kategori] = sayim.get(k.kategori, 0) + 1

        if not sayim:
            ctk.CTkLabel(self._istat_scroll,
                         text="Kayıtlı kurs olmadığı için gösterilecek istatistik yok.",
                         font=("Trebuchet MS", 12),
                         text_color=TEMA["yazi3"]).pack(pady=40)
            return

        toplam = sum(sayim.values())
        for kat, adet in sorted(sayim.items(), key=lambda x: -x[1]):
            renk = Kurs.KATEGORI_RENK.get(kat, TEMA["yazi3"])
            row = ctk.CTkFrame(self._istat_scroll, fg_color=TEMA["kart"], corner_radius=12)
            row.pack(fill="x", pady=4, padx=4)
            ic = ctk.CTkFrame(row, fg_color="transparent")
            ic.pack(fill="x", padx=16, pady=12)
            ust = ctk.CTkFrame(ic, fg_color="transparent")
            ust.pack(fill="x")
            ctk.CTkLabel(ust, text=kat, font=("Trebuchet MS", 12, "bold"),
                         text_color=renk).pack(side="left")
            ctk.CTkLabel(ust, text=f"{adet} kurs",
                         font=("Trebuchet MS", 11),
                         text_color=TEMA["yazi3"]).pack(side="right")
            bar = ctk.CTkProgressBar(ic, height=8, progress_color=renk,
                                     fg_color=TEMA["kart2"], corner_radius=4)
            bar.pack(fill="x", pady=(6, 0))
            bar.set(adet / toplam)

        # Özet kartlar
        _ayrac(self._istat_scroll, 10)
        sg = ctk.CTkFrame(self._istat_scroll, fg_color="transparent")
        sg.pack(fill="x")
        sg.columnconfigure((0, 1, 2), weight=1)

        for i, (lbl, val, renk) in enumerate([
            ("Toplam Kurs",     str(len(self.aktif_ogrenci.kayitli_kurslar)), TEMA["accent"]),
            ("Toplam Saat",     f"{self.aktif_ogrenci.toplam_saat}s",          TEMA["basari"]),
            ("İlerleme",        f"{self.aktif_ogrenci.ilerleme_yuzdesi}%",     TEMA["uyari"]),
        ]):
            kart = ctk.CTkFrame(sg, fg_color=TEMA["panel"], corner_radius=12)
            kart.grid(row=0, column=i, padx=5, sticky="ew")
            ctk.CTkLabel(kart, text=val, font=("Georgia", 22, "bold"),
                         text_color=renk).pack(pady=(14, 2))
            ctk.CTkLabel(kart, text=lbl, font=("Trebuchet MS", 10),
                         text_color=TEMA["yazi3"]).pack(pady=(0, 14))

    # ============================================================
    # 5. EYLEMLER & YARDIMCI METODLAR
    # ============================================================

    def _action_kayit(self, kurs):
        ok, msg = kurs.ogrenci_kaydet(self.aktif_ogrenci)
        if ok:
            self._toast(msg, TEMA["basari"])
            self._refresh_all()
        else:
            messagebox.showwarning("Kayıt Başarısız", msg)

    def _action_birak(self, kurs):
        ok, msg = kurs.ogrenci_birak(self.aktif_ogrenci)
        if ok:
            self._toast(msg, TEMA["uyari"])
            self._refresh_all()

    def _refresh_all(self):
        count = len(self.aktif_ogrenci.kayitli_kurslar)
        saat  = self.aktif_ogrenci.toplam_saat
        pct   = self.aktif_ogrenci.ilerleme_yuzdesi

        # Profil paneli
        self._stat_kurs_lbl.configure(text=str(count))
        self._stat_saat_lbl.configure(text=str(saat))
        self._prog_lbl.configure(text=f"{pct}%")
        self._prog_bar.set(pct / 100)

        # Ana sayfa
        if hasattr(self, '_home_kayitli_lbl'):
            self._home_kayitli_lbl.configure(text=str(count))
        if hasattr(self, '_home_saat_lbl'):
            self._home_saat_lbl.configure(text=f"{saat}s")

        self._refresh_catalog()
        self._refresh_lessons()
        if hasattr(self, '_istat_scroll'):
            self._refresh_istatistik()

    def _toast(self, mesaj, renk):
        toast = ctk.CTkFrame(self, fg_color=renk, corner_radius=10)
        ctk.CTkLabel(toast, text=f"  {mesaj}  ",
                     font=("Trebuchet MS", 12, "bold"),
                     text_color="white").pack(padx=12, pady=10)
        toast.place(relx=0.5, rely=0.96, anchor="s")
        self.after(2800, toast.destroy)

    def show_page(self, p):
        self.pages[p].lift()
        for key, btn in self._menu_btns.items():
            if key == p:
                btn.configure(fg_color=TEMA["kart"], text_color=TEMA["yazi"])
            else:
                btn.configure(fg_color="transparent", text_color=TEMA["yazi2"])


# ============================================================
# 6. GİRİŞ EKRANI
# ============================================================

class GirisEkrani(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("İKÜ LYS · Giriş")
        self.geometry("460x620")
        self.resizable(False, False)
        self.configure(fg_color=TEMA["bg"])
        self._build()

    def _build(self):
        # Üst logo şeridi
        top = ctk.CTkFrame(self, fg_color=TEMA["panel"], corner_radius=0, height=150)
        top.pack(fill="x")
        top.pack_propagate(False)

        logo = ctk.CTkFrame(top, fg_color="transparent")
        logo.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(logo, text="İKÜ", font=("Georgia", 40, "bold"),
                     text_color=TEMA["accent"]).pack(side="left")
        ctk.CTkLabel(logo, text=" LYS", font=("Georgia", 28),
                     text_color=TEMA["yazi"]).pack(side="left", pady=(8, 0))

        ctk.CTkLabel(top, text="Uzaktan Eğitim Portalı",
                     font=("Trebuchet MS", 12),
                     text_color=TEMA["yazi3"]).place(relx=0.5, rely=0.82, anchor="center")

        # Form
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=55, pady=30)

        ctk.CTkLabel(form, text="Hesabınıza Giriş Yapın",
                     font=("Georgia", 17, "bold"),
                     text_color=TEMA["yazi"]).pack(anchor="w", pady=(0, 22))

        alanlar = [
            ("ÖĞRENCİ NUMARASI", "Örn: 2023001"),
            ("AD SOYAD",         "Örn: Ahmet Yılmaz"),
            ("E-POSTA",          "Örn: ahmet@iku.edu.tr"),
            ("BÖLÜM",            "Örn: Bilgisayar Müh."),
        ]
        self._girişler = []
        for lbl, ph in alanlar:
            ctk.CTkLabel(form, text=lbl, font=("Trebuchet MS", 10, "bold"),
                         text_color=TEMA["yazi3"]).pack(anchor="w", pady=(8, 2))
            e = ctk.CTkEntry(form, placeholder_text=ph, height=40, corner_radius=8,
                             fg_color=TEMA["kart"], border_color=TEMA["sinir"],
                             text_color=TEMA["yazi"])
            e.pack(fill="x")
            self._girişler.append(e)

        ctk.CTkButton(form, text="Portala Giriş Yap →", height=46,
                      fg_color=TEMA["accent"], hover_color=TEMA["accent2"],
                      font=("Trebuchet MS", 14, "bold"), corner_radius=10,
                      command=self._giris).pack(fill="x", pady=(28, 0))

        ctk.CTkLabel(self, text="İstanbul Kültür Üniversitesi  ·  2025",
                     font=("Trebuchet MS", 9),
                     text_color=TEMA["yazi3"]).pack(pady=(0, 14))

    def _giris(self):
        u_id, u_ad, u_mail, u_bolum = [e.get().strip() for e in self._girişler]

        if not all([u_id, u_ad, u_mail]):
            messagebox.showwarning("Eksik Bilgi", "Lütfen zorunlu alanları (No, Ad, E-posta) doldurun.")
            return
        if not u_id.isdigit():
            messagebox.showwarning("Geçersiz No", "Öğrenci numarası yalnızca rakamlardan oluşmalıdır.")
            return
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", u_mail):
            messagebox.showwarning("Geçersiz E-posta", "Lütfen geçerli bir e-posta adresi giriniz.")
            return

        data = {"id": u_id, "ad": u_ad, "email": u_mail, "bolum": u_bolum or "Belirtilmedi"}
        self.destroy()
        Uygulama(data).mainloop()


# ============================================================
# 7. BAŞLAT
# ============================================================
if __name__ == "__main__":
    app = GirisEkrani()
    app.mainloop()

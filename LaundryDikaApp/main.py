import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from database import init_db, get_conn
from login_page import LoginPage
from menu_page import MenuPage
from crud_page import CrudPage
from laporan_page import LaporanPage


class LaundryApp(QStackedWidget):
    """
    Aplikasi Utama Laundry Dika
    ---------------------------
    Mengatur seluruh halaman:
    - Login
    - Menu Utama
    - CRUD (Barang Masuk, Ambil Barang, Pengantaran, Pengerjaan)
    - Laporan
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Informasi Laundry Dika")
        self.resize(900, 600)

        # Inisialisasi halaman
        self.login_page = LoginPage()
        self.menu_page = MenuPage()
        self.page_barang = CrudPage("data_barang_masuk", [
            ("kodetransaksi", "Kode Transaksi", "text"),
            ("nama", "Nama", "text"),
            ("alamat", "Alamat", "text"),
            ("telepon", "Telepon", "text"),
            ("tgl_masuk", "Tanggal Masuk", "date"),
            ("tgl_selesai", "Tanggal Selesai", "date"),
            ("kodebarang", "Kode Barang", "text"),
            ("namabarang", "Nama Barang", "text"),
            ("jenis", "Jenis", "text"),
            ("harga", "Harga", "text"),
            ("jumlah", "Jumlah", "text"),
            ("subtotal", "Subtotal", "text"),
            ("total", "Total", "text"),
            ("bayar", "Bayar", "text"),
            ("kembalian", "Kembalian", "text")
        ])
        self.page_ambil = CrudPage("data_ambil_barang", [
            ("kodetransaksi", "Kode Transaksi", "text"),
            ("nama", "Nama", "text"),
            ("alamat", "Alamat", "text"),
            ("telepon", "Telepon", "text"),
            ("tgl_masuk", "Tanggal Masuk", "date"),
            ("tgl_selesai", "Tanggal Selesai", "date"),
            ("kodebarang", "Kode Barang", "text"),
            ("namabarang", "Nama Barang", "text"),
            ("jenis", "Jenis", "text"),
            ("jumlah", "Jumlah", "text"),
            ("subtotal", "Subtotal", "text"),
            ("total", "Total", "text"),
            ("bayar", "Bayar", "text"),
            ("kembalian", "Kembalian", "text"),
            ("status_pembayaran", "Status Pembayaran", "text"),
            ("tgl_pengambilan", "Tanggal Pengambilan", "date")
        ])
        self.page_pengantaran = CrudPage("data_pengantaran", [
            ("kodetransaksi", "Kode Transaksi", "text"),
            ("nama", "Nama", "text"),
            ("alamat", "Alamat", "text"),
            ("telepon", "Telepon", "text"),
            ("tgl_masuk", "Tanggal Masuk", "date"),
            ("tgl_selesai", "Tanggal Selesai", "date"),
            ("kodebarang", "Kode Barang", "text"),
            ("namabarang", "Nama Barang", "text"),
            ("jenis", "Jenis", "text"),
            ("jumlah", "Jumlah", "text"),
            ("subtotal", "Subtotal", "text"),
            ("total", "Total", "text"),
            ("bayar", "Bayar", "text"),
            ("kembalian", "Kembalian", "text"),
            ("status_pembayaran", "Status Pembayaran", "text"),
            ("tgl_pengambilan", "Tanggal Pengambilan", "date"),
            ("nama_kurir", "Nama Kurir", "text"),
            ("telepon_kurir", "Telepon Kurir", "text")
        ])
        self.page_pengerjaan = CrudPage("data_pengerjaan", [
            ("kodetransaksi", "Kode Transaksi", "text"),
            ("nama", "Nama", "text"),
            ("alamat", "Alamat", "text"),
            ("telepon", "Telepon", "text"),
            ("tgl_masuk", "Tanggal Masuk", "date"),
            ("tgl_selesai", "Tanggal Selesai", "date"),
            ("kodebarang", "Kode Barang", "text"),
            ("namabarang", "Nama Barang", "text"),
            ("jenis", "Jenis", "text"),
            ("jumlah", "Jumlah", "text"),
            ("tgl_pengerjaan", "Tanggal Pengerjaan", "date"),
            ("kode_pegawai", "Kode Pegawai", "text"),
            ("nama_pegawai", "Nama Pegawai", "text"),
            ("keterangan", "Keterangan", "multi")
        ])
        self.page_laporan = LaporanPage()

        # Tambahkan semua halaman ke QStackedWidget
        self.addWidget(self.login_page)         # index 0
        self.addWidget(self.menu_page)          # index 1
        self.addWidget(self.page_barang)        # index 2
        self.addWidget(self.page_ambil)         # index 3
        self.addWidget(self.page_pengantaran)   # index 4
        self.addWidget(self.page_pengerjaan)    # index 5
        self.addWidget(self.page_laporan)       # index 6

        # Koneksi tombol login & menu
        self.login_page.btn_login.clicked.connect(self.handle_login)
        self.login_page.btn_quit.clicked.connect(self.close)

        self.menu_page.btn_barang.clicked.connect(lambda: self.goto_page(2))
        self.menu_page.btn_ambil.clicked.connect(lambda: self.goto_page(3))
        self.menu_page.btn_pengantaran.clicked.connect(lambda: self.goto_page(4))
        self.menu_page.btn_pengerjaan.clicked.connect(lambda: self.goto_page(5))
        self.menu_page.btn_laporan.clicked.connect(lambda: self.goto_page(6))
        self.menu_page.btn_logout.clicked.connect(lambda: self.goto_page(0))

        # 🔙 Tombol kembali di setiap halaman CRUD dan laporan
        self.page_barang.btn_back.clicked.connect(lambda: self.goto_page(1))
        self.page_ambil.btn_back.clicked.connect(lambda: self.goto_page(1))
        self.page_pengantaran.btn_back.clicked.connect(lambda: self.goto_page(1))
        self.page_pengerjaan.btn_back.clicked.connect(lambda: self.goto_page(1))
        self.page_laporan.btn_back.clicked.connect(lambda: self.goto_page(1))


        # Default halaman pertama: login
        self.setCurrentIndex(0)

    # ==== LOGIKA ====
    def handle_login(self):
        """Cek login admin dari database."""
        username = self.login_page.username_input.text().strip()
        password = self.login_page.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Peringatan", "Masukkan username dan password.")
            return

        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            QMessageBox.information(self, "Sukses", f"Selamat datang, {admin['nama']}!")
            self.goto_page(1)
            self.login_page.username_input.clear()
            self.login_page.password_input.clear()
        else:
            QMessageBox.critical(self, "Gagal", "Username atau password salah!")

    def goto_page(self, index):
        """Pindah ke halaman tertentu berdasarkan index."""
        self.setCurrentIndex(index)


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    # 🌈 Tema warna lembut tapi kontras (semua teks terlihat)
    style = """
    QWidget {
        background-color: #f3f6fb;
        color: #1e293b;             /* warna teks utama */
        font-family: 'Segoe UI';
        font-size: 11pt;
    }

    QPushButton {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 6px 14px;
    }

    QPushButton:hover {
        background-color: #2563eb;
    }

    QPushButton:pressed {
        background-color: #1e40af;
    }

    QLabel {
        color: #1e293b;  /* teks label gelap */
    }

    QLineEdit, QTextEdit, QDateEdit, QComboBox {
        background-color: white;
        color: #1e293b;  /* teks hitam di dalam input */
        border: 1px solid #cbd5e1;
        border-radius: 5px;
        padding: 4px;
        selection-background-color: #bfdbfe; /* warna seleksi input */
        selection-color: #000000;
    }

    QTableWidget {
        background-color: white;
        color: #111827;  /* teks tabel hitam */
        border: 1px solid #cbd5e1;
        gridline-color: #cbd5e1;
        selection-background-color: #93c5fd;
        selection-color: black;
    }

    QPushButton#btn_back {
        background-color: #ef4444;
        color: white;
        border-radius: 8px;
        padding: 6px 14px;
    }

    QPushButton#btn_back:hover {
        background-color: #dc2626;
    }

    QPushButton#btn_back {
        background-color: #ef4444;
        color: white;
        border-radius: 8px;
        padding: 6px 14px;
    }

    QPushButton#btn_back:hover {
        background-color: #dc2626;
    }

    QHeaderView::section {
        background-color: #e2e8f0;
        color: #1e293b;
        font-weight: bold;
        padding: 4px;
        border: 1px solid #cbd5e1;
    }
    """

    app.setStyle("Fusion")
    app.setStyleSheet(style)

    window = LaundryApp()
    window.show()
    sys.exit(app.exec())

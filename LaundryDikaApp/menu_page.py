from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
)


class MenuPage(QWidget):
    """
    Halaman Menu Utama Laundry Dika
    --------------------------------
    Berisi tombol navigasi ke seluruh fitur:
    - Data Barang Masuk
    - Data Ambil Barang
    - Data Pengantaran
    - Data Pengerjaan
    - Laporan
    - Logout
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Judul halaman
        title = QLabel("<h2>Menu Utama - Laundry Dika</h2>")
        layout.addWidget(title)

        # Grid tombol menu
        grid = QGridLayout()

        self.btn_barang = QPushButton("Data Barang Masuk")
        self.btn_ambil = QPushButton("Data Ambil Barang")
        self.btn_pengantaran = QPushButton("Data Pengantaran")
        self.btn_pengerjaan = QPushButton("Data Pengerjaan")
        self.btn_laporan = QPushButton("Laporan")
        self.btn_logout = QPushButton("Logout")

        # Susunan tombol 3x2
        grid.addWidget(self.btn_barang, 0, 0)
        grid.addWidget(self.btn_ambil, 0, 1)
        grid.addWidget(self.btn_pengantaran, 1, 0)
        grid.addWidget(self.btn_pengerjaan, 1, 1)
        grid.addWidget(self.btn_laporan, 2, 0)
        grid.addWidget(self.btn_logout, 2, 1)

        layout.addLayout(grid)

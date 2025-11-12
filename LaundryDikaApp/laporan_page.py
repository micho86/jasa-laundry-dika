import csv
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QComboBox, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from database import get_conn


class LaporanPage(QWidget):
    """
    Halaman Laporan Laundry Dika
    ----------------------------
    Menampilkan data dari tabel:
    - data_ambil_barang
    - data_pengantaran
    - data_pengerjaan
    Dapat diekspor ke file CSV.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("<h3>Laporan Laundry Dika</h3>")
        layout.addWidget(title)

        # Pilihan jenis laporan
        control_layout = QHBoxLayout()
        self.combo_tabel = QComboBox()
        self.combo_tabel.addItems([
            "data_barang_masuk",
            "data_ambil_barang",
            "data_pengantaran",
            "data_pengerjaan"
        ])
        self.btn_tampil = QPushButton("Tampilkan Data")
        self.btn_export = QPushButton("Export ke CSV")
        self.btn_back = QPushButton("← Kembali ke Menu")  # ✅ tombol baru

        control_layout.addWidget(QLabel("Pilih Laporan:"))
        control_layout.addWidget(self.combo_tabel)
        control_layout.addWidget(self.btn_tampil)
        control_layout.addWidget(self.btn_export)
        control_layout.addWidget(self.btn_back)  # ✅ tambahkan ke layout
        layout.addLayout(control_layout)


        # Tabel data
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Event tombol
        self.btn_tampil.clicked.connect(self.tampilkan_data)
        self.btn_export.clicked.connect(self.export_csv)

    def tampilkan_data(self):
        """Menampilkan isi tabel yang dipilih."""
        table_name = self.combo_tabel.currentText()
        conn = get_conn()
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM {table_name}")
            rows = c.fetchall()
            headers = [d[0] for d in c.description]

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(rows):
                for j, h in enumerate(headers):
                    val = str(row[h]) if row[h] is not None else ""
                    item = QTableWidgetItem(val)
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.table.setItem(i, j, item)

            self.table.resizeColumnsToContents()
            QMessageBox.information(self, "Sukses", f"Laporan '{table_name}' berhasil dimuat.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat laporan:\n{e}")
        finally:
            conn.close()

    def export_csv(self):
        """Ekspor data tabel ke file CSV."""
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        if row_count == 0 or col_count == 0:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data untuk diekspor.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        headers = [self.table.horizontalHeaderItem(i).text() for i in range(col_count)]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for i in range(row_count):
                    row_data = [self.table.item(i, j).text() if self.table.item(i, j) else "" for j in range(col_count)]
                    writer.writerow(row_data)

            QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menulis CSV:\n{e}")

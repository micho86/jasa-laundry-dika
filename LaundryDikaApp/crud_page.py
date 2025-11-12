from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDateEdit, QTableWidget, QTableWidgetItem, QPushButton, QGridLayout,
    QMessageBox, QComboBox
)
from PySide6.QtCore import Qt, QDate
from database import get_conn


class CrudPage(QWidget):
    """
    Halaman CRUD Universal
    ----------------------
    Digunakan untuk semua tabel Laundry Dika:
    - Data Barang Masuk
    - Data Ambil Barang
    - Data Pengantaran
    - Data Pengerjaan
    """

    def __init__(self, table_name, fields, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.fields = fields  # daftar tuple: (kolom, label, tipe)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel(f"<h3>{self.table_name.replace('_', ' ').title()}</h3>")
        layout.addWidget(title)

        # Form input
        form_layout = QGridLayout()
        self.inputs = {}
        row = 0
        for col, label, ftype in self.fields:
            form_layout.addWidget(QLabel(label), row, 0)

            if ftype == "text":
                widget = QLineEdit()
            elif ftype == "date":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
            elif ftype == "multi":
                widget = QTextEdit()
            elif ftype == "combo":
                widget = QComboBox()
            else:
                widget = QLineEdit()

            self.inputs[col] = widget
            form_layout.addWidget(widget, row, 1)
            row += 1

        layout.addLayout(form_layout)

        # Tombol CRUD
            # --- Tombol CRUD + Kembali ---
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Tambah")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Hapus")
        self.btn_clear = QPushButton("Bersihkan")
        self.btn_back = QPushButton("← Kembali ke Menu")  # tombol baru

    # Tambahkan tombol ke layout
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_back)  # ← posisinya di kanan

        layout.addLayout(btn_layout)


        # Tabel data
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Koneksi tombol
        self.btn_add.clicked.connect(self.add_record)
        self.btn_update.clicked.connect(self.update_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_clear.clicked.connect(self.clear_form)
        self.table.itemSelectionChanged.connect(self.select_row)

    # ====== CRUD LOGIC ======
    def load_data(self):
        conn = get_conn()
        c = conn.cursor()
        c.execute(f"SELECT rowid, * FROM {self.table_name} ORDER BY rowid DESC")
        rows = c.fetchall()
        conn.close()

        headers = ["ID"] + [lbl for _, lbl, _ in self.fields]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for cidx, key in enumerate(row.keys()):
                item = QTableWidgetItem(str(row[key]) if row[key] is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r, cidx, item)

        self.table.resizeColumnsToContents()

    def get_values(self):
        vals = {}
        for col, _, ftype in self.fields:
            widget = self.inputs[col]
            if isinstance(widget, QLineEdit):
                vals[col] = widget.text().strip()
            elif isinstance(widget, QDateEdit):
                vals[col] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QTextEdit):
                vals[col] = widget.toPlainText().strip()
            elif isinstance(widget, QComboBox):
                vals[col] = widget.currentText()
            else:
                vals[col] = ""
        return vals

    def add_record(self):
        vals = self.get_values()
        keys = ", ".join(vals.keys())
        placeholders = ", ".join(["?"] * len(vals))
        sql = f"INSERT INTO {self.table_name} ({keys}) VALUES ({placeholders})"

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute(sql, tuple(vals.values()))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            self.load_data()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambah data:\n{e}")

    def update_record(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan diupdate.")
            return

        rowid = selected[0].text()
        vals = self.get_values()
        set_clause = ", ".join([f"{k}=?" for k in vals.keys()])
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE rowid=?"

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute(sql, tuple(vals.values()) + (rowid,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sukses", "Data berhasil diupdate.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal update:\n{e}")

    def delete_record(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan dihapus.")
            return

        rowid = selected[0].text()
        confirm = QMessageBox.question(self, "Konfirmasi", f"Hapus data ID {rowid}?")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            conn = get_conn()
            c = conn.cursor()
            c.execute(f"DELETE FROM {self.table_name} WHERE rowid=?", (rowid,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
            self.load_data()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus:\n{e}")

    def clear_form(self):
        for w in self.inputs.values():
            if isinstance(w, QLineEdit):
                w.clear()
            elif isinstance(w, QTextEdit):
                w.clear()
            elif isinstance(w, QDateEdit):
                w.setDate(QDate.currentDate())
        self.table.clearSelection()

    def select_row(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        row = self.table.currentRow()
        for i, (col, _, _) in enumerate(self.fields):
            item = self.table.item(row, i + 1)
            if item:
                widget = self.inputs[col]
                val = item.text()
                if isinstance(widget, QLineEdit):
                    widget.setText(val)
                elif isinstance(widget, QTextEdit):
                    widget.setPlainText(val)
                elif isinstance(widget, QDateEdit):
                    d = QDate.fromString(val, "yyyy-MM-dd")
                    if d.isValid():
                        widget.setDate(d)

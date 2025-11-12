

import sqlite3

DB_FILE = "laundry_dika.db"


def get_conn():
    """Membuka koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Membuat tabel-tabel utama sesuai jurnal Laundry Dika."""
    conn = get_conn()
    c = conn.cursor()

    # Tabel admin (login)
    c.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        nama TEXT
    )
    """)

    # Tabel data jasa
    c.execute("""
    CREATE TABLE IF NOT EXISTS data_jasa (
        kode_jasa TEXT PRIMARY KEY,
        nama_jasa TEXT,
        jenis_jasa TEXT,
        harga_jasa REAL
    )
    """)

    # Tabel data barang masuk
    c.execute("""
    CREATE TABLE IF NOT EXISTS data_barang_masuk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kodetransaksi TEXT,
        nama TEXT,
        alamat TEXT,
        telepon TEXT,
        tgl_masuk TEXT,
        tgl_selesai TEXT,
        kodebarang TEXT,
        namabarang TEXT,
        jenis TEXT,
        harga REAL,
        jumlah INTEGER,
        subtotal REAL,
        total REAL,
        bayar REAL,
        kembalian REAL
    )
    """)

    # Tabel data ambil barang
    c.execute("""
    CREATE TABLE IF NOT EXISTS data_ambil_barang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kodetransaksi TEXT,
        nama TEXT,
        alamat TEXT,
        telepon TEXT,
        tgl_masuk TEXT,
        tgl_selesai TEXT,
        kodebarang TEXT,
        namabarang TEXT,
        jenis TEXT,
        jumlah INTEGER,
        subtotal REAL,
        total REAL,
        bayar REAL,
        kembalian REAL,
        status_pembayaran TEXT,
        tgl_pengambilan TEXT
    )
    """)

    # Tabel data pengantaran
    c.execute("""
    CREATE TABLE IF NOT EXISTS data_pengantaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kodetransaksi TEXT,
        nama TEXT,
        alamat TEXT,
        telepon TEXT,
        tgl_masuk TEXT,
        tgl_selesai TEXT,
        kodebarang TEXT,
        namabarang TEXT,
        jenis TEXT,
        jumlah INTEGER,
        subtotal REAL,
        total REAL,
        bayar REAL,
        kembalian REAL,
        status_pembayaran TEXT,
        tgl_pengambilan TEXT,
        nama_kurir TEXT,
        telepon_kurir TEXT
    )
    """)

    # Tabel data pengerjaan
    c.execute("""
    CREATE TABLE IF NOT EXISTS data_pengerjaan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kodetransaksi TEXT,
        nama TEXT,
        alamat TEXT,
        telepon TEXT,
        tgl_masuk TEXT,
        tgl_selesai TEXT,
        kodebarang TEXT,
        namabarang TEXT,
        jenis TEXT,
        jumlah INTEGER,
        tgl_pengerjaan TEXT,
        kode_pegawai TEXT,
        nama_pegawai TEXT,
        keterangan TEXT
    )
    """)

    # Tambahkan admin default jika belum ada
    c.execute("SELECT COUNT(*) as cnt FROM admin")
    if c.fetchone()["cnt"] == 0:
        c.execute(
            "INSERT INTO admin (username, password, nama) VALUES (?, ?, ?)",
            ("admin", "admin123", "Administrator")
        )

    conn.commit()
    conn.close()
    print("✅ Database berhasil diinisialisasi.")


if __name__ == "__main__":
    init_db()

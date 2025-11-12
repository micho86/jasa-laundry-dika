from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt


class LoginPage(QWidget):
    """
    Halaman Login Admin
    -------------------
    - Username: input teks
    - Password: input password tersembunyi
    - Tombol: Login & Keluar
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Judul
        title = QLabel("<h2>Login Admin - Laundry Dika</h2>")
        layout.addWidget(title)

        # Form input
        form = QGridLayout()
        form.addWidget(QLabel("Username:"), 0, 0)
        self.username_input = QLineEdit()
        form.addWidget(self.username_input, 0, 1)

        form.addWidget(QLabel("Password:"), 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addWidget(self.password_input, 1, 1)

        layout.addLayout(form)

        # Tombol
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Login")
        self.btn_quit = QPushButton("Keluar")
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_quit)

        layout.addLayout(btn_layout)

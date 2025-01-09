# login_window.py

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame
)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QSize

# Ajusta el import según la ruta real de tu base.py:
try:
    from app.db.base import validate_user
except ImportError:
    # Demo sin acceso a DB real
    def validate_user(username, password):
        if username == "admin" and password == "123":
            return (True, 1)
        return (False, None)

# Colores y estilos globales (puedes mover esto a un archivo de constants si deseas)
PRIMARY_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
TEXT_COLOR = "#ECF0F1"
BUTTON_COLOR = "#2980B9"
BUTTON_HOVER = "#1F6391"


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP - Iniciar Sesión")
        self.setFixedSize(400, 500)
        self.setWindowIcon(QIcon("resources/icon.png"))

        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        central_widget.setLayout(layout)

        # Ícono
        icon_label = QLabel()
        pix = QPixmap("resources/icon.png")
        pix = pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pix)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Título
        title_label = QLabel("Bienvenido al ERP")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {TEXT_COLOR};")
        font_title = QFont()
        font_title.setPointSize(18)
        font_title.setBold(True)
        title_label.setFont(font_title)
        layout.addWidget(title_label)

        # Separador
        line_sep = QFrame()
        line_sep.setFrameShape(QFrame.HLine)
        line_sep.setStyleSheet(f"color: {TEXT_COLOR};")
        layout.addWidget(line_sep)

        # Campos usuario/contraseña
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setFixedHeight(40)
        self.user_input.setStyleSheet(
            "QLineEdit {"
            "  background-color: white;"
            f"  border: 1px solid {ACCENT_COLOR};"
            "  border-radius: 5px;"
            "  padding: 8px;"
            "}"
            "QLineEdit:focus {"
            f"  border: 2px solid {BUTTON_COLOR};"
            "}"
        )

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(40)
        self.pass_input.setStyleSheet(
            "QLineEdit {"
            "  background-color: white;"
            f"  border: 1px solid {ACCENT_COLOR};"
            "  border-radius: 5px;"
            "  padding: 8px;"
            "}"
            "QLineEdit:focus {"
            f"  border: 2px solid {BUTTON_COLOR};"
            "}"
        )

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)

        # Botón
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setFixedHeight(45)
        self.login_button.setStyleSheet(
            f"QPushButton {{"
            f"  background-color: {BUTTON_COLOR};"
            f"  color: {TEXT_COLOR};"
            "  border-radius: 5px;"
            "  font-size: 16px;"
            "}"
            f"QPushButton:hover {{ background-color: {BUTTON_HOVER}; }}"
        )
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Label estado
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold;")
        layout.addWidget(self.status_label)

    def handle_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        ok, user_id = validate_user(username, password)
        if ok:
            self.status_label.setText("¡Acceso concedido!")
            self.goto_company_selection()
        else:
            self.status_label.setText("Credenciales inválidas.")
            self.pass_input.clear()

    def goto_company_selection(self):
        # Para evitar ImportError circular, importamos dentro del método:
        from frontend_local.company_window import CompanySelectionWindow

        self.close()
        self.company_window = CompanySelectionWindow()
        self.company_window.show()

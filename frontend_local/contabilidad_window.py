# contabilidad_window.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class ContabilidadWindow(QDialog):
    def __init__(self, empresa, parent=None):
        super().__init__(parent)
        self.empresa = empresa
        self.setWindowTitle(f"Contabilidad - {empresa['nombre_legal']}")
        self.resize(600, 400)  # o setFixedSize si prefieres

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("Módulo de Contabilidad")
        font_title = QFont()
        font_title.setPointSize(16)
        font_title.setBold(True)
        title_label.setFont(font_title)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        info_label = QLabel(f"Empresa: {empresa['nombre_legal']} (ID={empresa['id_empresa']})")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        btn_crear = QPushButton("Crear Comprobante")
        btn_crear.clicked.connect(self.handle_crear_comprobante)

        btn_consultar = QPushButton("Consultar Comprobantes")
        btn_consultar.clicked.connect(self.handle_consultar_comprobantes)

        layout.addWidget(btn_crear)
        layout.addWidget(btn_consultar)
        layout.addStretch(1)

    def handle_crear_comprobante(self):
        QMessageBox.information(self, "Crear Comprobante", "Aquí abrirías el formulario de creación de comprobante.")

    def handle_consultar_comprobantes(self):
        QMessageBox.information(self, "Consultar Comprobantes", "Aquí mostrarías la lista de comprobantes existentes.")

# company_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout,
    QPushButton, QFrame, QMessageBox, QSpacerItem, QSizePolicy,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

# IMPORTAMOS FUNCIONES DE LA BD
try:
    from app.db.base import list_companies, create_company
except ImportError:
    # Demo sin acceso a DB real
    def list_companies():
        return [
            {"id_empresa": 1, "nombre_legal": "Empresa Alfa", "rut": "1111-1"},
            {"id_empresa": 2, "nombre_legal": "Empresa Beta", "rut": "2222-2"},
        ]


    def create_company(nombre_legal, rut, direccion=None):
        print(f"[Simulado] Creando empresa: {nombre_legal}, {rut}, {direccion}")

# Colores / estilos
PRIMARY_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
TEXT_COLOR = "#ECF0F1"
BUTTON_COLOR = "#2980B9"
BUTTON_HOVER = "#1F6391"
CARD_BG = "#34495E"


class CompanySelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Empresa")
        self.setFixedSize(800, 400)
        self.setWindowIcon(QIcon("resources/icon.png"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Título
        title_label = QLabel("Selecciona o Administra una Empresa")
        font_title = QFont()
        font_title.setPointSize(16)
        font_title.setBold(True)
        title_label.setFont(font_title)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        container_widget = QWidget()
        container_layout = QHBoxLayout()
        container_widget.setLayout(container_layout)
        scroll_area.setWidget(container_widget)

        # Botones de crear
        btn_layout = QHBoxLayout()
        self.btn_crear = QPushButton("Crear Empresa")
        self.btn_crear.clicked.connect(self.handle_create_company)
        btn_layout.addWidget(self.btn_crear)

        main_layout.addLayout(btn_layout)

        # Cargar "cards" con empresas
        self.container_layout = container_layout
        self.load_companies()

    def load_companies(self):
        """
        Carga o recarga las tarjetas de empresas en self.container_layout.
        Se llama después de crear/eliminar/modificar.
        """
        # Limpiar layout anterior
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.container_layout.setSpacing(15)
        empresas = list_companies()

        for emp in empresas:
            card = self.create_company_card(emp)
            self.container_layout.addWidget(card)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container_layout.addSpacerItem(spacer)

    def create_company_card(self, emp):
        frame = QFrame()
        frame.setFixedSize(200, 200)
        frame.setStyleSheet(
            f"QFrame {{"
            f"  background-color: {CARD_BG};"
            "  border-radius: 8px;"
            "  padding: 10px;"
            "}"
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        name_label = QLabel(emp["nombre_legal"])
        name_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        name_label.setAlignment(Qt.AlignCenter)

        rut_label = QLabel(f"RUT: {emp['rut']}")
        rut_label.setStyleSheet("color: #BDC3C7; font-size: 12px;")
        rut_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(name_label)
        layout.addWidget(rut_label)

        # Botones
        btn_modificar = QPushButton("Modificar")
        btn_modificar.setStyleSheet(f"background-color: {ACCENT_COLOR}; color: white; border-radius: 5px;")
        btn_modificar.clicked.connect(lambda: self.handle_modify_company(emp))

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("background-color: #C0392B; color: white; border-radius: 5px;")
        btn_eliminar.clicked.connect(lambda: self.handle_delete_company(emp))

        btn_entrar = QPushButton("Entrar")
        btn_entrar.setStyleSheet(f"background-color: {BUTTON_COLOR}; color: white; border-radius: 5px;")
        btn_entrar.clicked.connect(lambda: self.handle_enter_company(emp))

        layout.addWidget(btn_modificar)
        layout.addWidget(btn_eliminar)
        layout.addWidget(btn_entrar)

        return frame

    def handle_create_company(self):
        """
        Muestra el diálogo para crear una empresa.
        Si el usuario da Aceptar, se llama create_company y se recarga la vista.
        """
        dialog = CreateCompanyDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            # Llamamos a create_company de la BD
            create_company(data["nombre_legal"], data["rut"], data["direccion"])
            # Recargar la lista
            self.load_companies()

    def handle_modify_company(self, emp):
        QMessageBox.information(self, "Modificar Empresa", f"Modificar {emp['nombre_legal']} (pendiente).")
        # Podrías abrir otro diálogo con los campos precargados, al estilo de CreateCompanyDialog

    def handle_delete_company(self, emp):
        confirm = QMessageBox.question(self, "Eliminar", f"¿Eliminar {emp['nombre_legal']}?")
        if confirm == QMessageBox.Yes:
            QMessageBox.information(self, "Eliminar", f"{emp['nombre_legal']} eliminada (demo).")
            # Aquí harías delete_company(emp["id_empresa"]) y self.load_companies()

    def handle_enter_company(self, emp):
        from frontend_local.main_window import MainWindow
        self.close()
        self.main_window = MainWindow(emp)
        self.main_window.show()


# ----------------------------------------------------------------
# DIALOGO PARA CREAR EMPRESA
# ----------------------------------------------------------------
class CreateCompanyDialog(QDialog):
    """
    Diálogo que muestra un formulario para ingresar
    nombre_legal, rut y dirección. Al dar Aceptar,
    retorna esos datos.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Empresa")
        self.setFixedSize(400, 250)

        layout = QFormLayout()
        self.setLayout(layout)

        # Campos
        self.input_nombre = QLineEdit()
        self.input_rut = QLineEdit()
        self.input_direccion = QLineEdit()

        layout.addRow("Nombre Legal:", self.input_nombre)
        layout.addRow("RUT:", self.input_rut)
        layout.addRow("Dirección:", self.input_direccion)

        # Botones Aceptar/Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_data(self):
        """
        Retorna un dict con los valores ingresados.
        Se llama después de exec(), si devuelves Accepted.
        """
        return {
            "nombre_legal": self.input_nombre.text().strip(),
            "rut": self.input_rut.text().strip(),
            "direccion": self.input_direccion.text().strip()
        }

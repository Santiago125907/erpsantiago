from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QStackedWidget, QFrame, QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QDateTime, QTimer
import sys


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QStackedWidget, QFrame, QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QDateTime, QTimer
import sys


class MainWindow(QMainWindow):
    def __init__(self, empresa=None):
        super().__init__()
        # Usar los campos correctos según la estructura de la base de datos
        self.empresa = empresa or {
            "nombre_legal": "Mi Empresa S.A.",
            "rut": "76.123.456-7",
            "direccion": "Dirección por defecto",
            "ciudad": "Ciudad por defecto",
            "pais": "País por defecto",
            "fecha_creacion": None,
            "id_empresa": None
        }

        self.setWindowTitle(f"ERP - {self.empresa.get('nombre_legal', 'Sin nombre')}")
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("""
            QMainWindow, QFrame#contentFrame {
                background-color: #F0F2F5;
            }
            QLabel#welcomeTitle {
                font-size: 28px;
                font-weight: bold;
                color: #2C3E50;
            }
            QLabel#welcomeSubtitle {
                font-size: 16px;
                color: #7F8C8D;
            }
            QPushButton#moduleCard {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 20px;
                font-size: 16px;
                text-align: center;
            }
            QPushButton#moduleCard:hover {
                background-color: #F8F9FA;
                border: 1px solid #3498DB;
            }
        """)

        # Widget y layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Crear elementos principales
        self.create_sidebar()
        self.create_content_area()

        # Timer para actualizar la hora
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Actualizar cada segundo

    def create_sidebar(self):
        """Crea el menú lateral simplificado"""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border: none;
            }
            QLabel {
                color: #ECF0F1;
            }
            QPushButton {
                background-color: transparent;
                color: #ECF0F1;
                border: none;
                padding: 15px;
                font-size: 14px;
                text-align: left;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton#selected {
                background-color: #34495E;
                border-left: 4px solid #3498DB;
            }
        """)
        sidebar.setFixedWidth(250)

        # Layout para el sidebar
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Información de la empresa y usuario
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #243342; padding: 20px;")
        info_layout = QVBoxLayout(info_frame)

        # Logo y nombre de la empresa
        empresa_label = QLabel(self.empresa.get('nombre_legal', 'Sin nombre'))
        empresa_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(empresa_label)

        rut_label = QLabel(f"RUT: {self.empresa.get('rut', 'Sin RUT')}")
        rut_label.setStyleSheet("font-size: 12px; color: #95A5A6;")
        info_layout.addWidget(rut_label)

        ciudad_label = QLabel(f"Ciudad: {self.empresa.get('ciudad', 'Sin ciudad')}")
        ciudad_label.setStyleSheet("font-size: 12px; color: #95A5A6;")
        info_layout.addWidget(ciudad_label)

        pais_label = QLabel(f"País: {self.empresa.get('pais', 'Sin país')}")
        pais_label.setStyleSheet("font-size: 12px; color: #95A5A6;")
        info_layout.addWidget(pais_label)

        # Fecha y hora
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet("font-size: 12px; color: #95A5A6;")
        info_layout.addWidget(self.datetime_label)
        self.update_datetime()

        sidebar_layout.addWidget(info_frame)

        # Botones de módulos
        modules = [
            ("Contabilidad", self.show_contabilidad),
            ("RRHH", self.show_rrhh),
            ("Inventarios", self.show_inventarios),
            ("Ventas", self.show_ventas),
            ("Compras", self.show_compras)
        ]

        self.module_buttons = {}
        for module_name, callback in modules:
            btn = QPushButton(module_name)
            btn.clicked.connect(lambda checked, m=module_name, c=callback: self.select_module(m, c))
            sidebar_layout.addWidget(btn)
            self.module_buttons[module_name] = btn

        sidebar_layout.addStretch()
        self.main_layout.addWidget(sidebar)

    # El resto del código permanece igual...
    # (Mantengo las funciones create_content_area, create_welcome_view, etc.)

    def create_content_area(self):
        """Crea el área de contenido principal"""
        self.content_area = QFrame()
        self.content_area.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Stack para diferentes vistas
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)

        # Agregar vistas
        self.create_welcome_view()
        self.create_contabilidad_view()

        self.main_layout.addWidget(self.content_area)

    def create_welcome_view(self):
        """Crea la vista de bienvenida"""
        welcome = QWidget()
        welcome_layout = QVBoxLayout(welcome)
        welcome_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Bienvenido al Sistema ERP")
        title.setObjectName("welcomeTitle")
        welcome_layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel("Por favor, seleccione un módulo del menú lateral para comenzar")
        subtitle.setObjectName("welcomeSubtitle")
        welcome_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        self.stack.addWidget(welcome)

    def create_contabilidad_view(self):
        """Crea la vista del módulo de contabilidad"""
        contabilidad = QWidget()
        layout = QVBoxLayout(contabilidad)

        # Título y descripción
        title = QLabel("Módulo de Contabilidad")
        title.setObjectName("welcomeTitle")
        layout.addWidget(title)

        desc = QLabel("Gestión de comprobantes, reportes financieros y más")
        desc.setObjectName("welcomeSubtitle")
        layout.addWidget(desc)

        # Grid de tarjetas
        grid = QGridLayout()
        grid.setSpacing(20)

        # Definir tarjetas
        cards = [
            ("Crear Comprobante", "Registra nuevas transacciones contables"),
            ("Consultar Comprobantes", "Busca y visualiza comprobantes existentes"),
            ("Estados Financieros", "Balance y Estado de Resultados"),
            ("Plan de Cuentas", "Gestiona el catálogo de cuentas contables"),
            ("Impuestos", "Gestión y reportes de impuestos"),
            ("Configuración", "Ajustes del módulo contable")
        ]

        # Crear tarjetas
        for i, (title, desc) in enumerate(cards):
            card = QPushButton()
            card.setObjectName("moduleCard")
            card_layout = QVBoxLayout()

            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("color: #666;")

            card_layout.addWidget(title_label)
            card_layout.addWidget(desc_label)
            card.setLayout(card_layout)

            grid.addWidget(card, i // 3, i % 3)

        layout.addLayout(grid)
        layout.addStretch()

        self.stack.addWidget(contabilidad)

    def select_module(self, module_name, callback):
        """Selecciona un módulo y actualiza la UI"""
        # Resetear todos los botones
        for btn in self.module_buttons.values():
            btn.setObjectName("")
            btn.setStyleSheet("")

        # Resaltar el botón seleccionado
        self.module_buttons[module_name].setObjectName("selected")

        # Llamar al callback del módulo
        callback()

    def update_datetime(self):
        """Actualiza la fecha y hora en el sidebar"""
        current = QDateTime.currentDateTime()
        self.datetime_label.setText(current.toString("dd/MM/yyyy HH:mm:ss"))

    def show_contabilidad(self):
        """Muestra la vista de contabilidad"""
        self.stack.setCurrentIndex(1)  # Índice de la vista de contabilidad

    def show_rrhh(self):
        """Placeholder para RRHH"""
        pass

    def show_inventarios(self):
        """Placeholder para Inventarios"""
        pass

    def show_ventas(self):
        """Placeholder para Ventas"""
        pass

    def show_compras(self):
        """Placeholder para Compras"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
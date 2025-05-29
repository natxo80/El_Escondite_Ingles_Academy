from PySide2.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QFileDialog,
                               QFrame, QGroupBox, QHBoxLayout)
from PySide2.QtGui import QFont, QPixmap, QIcon
from ui.manage_students_window import ManageStudentsWindow  # Importamos la nueva ventana para gestionar alumnos
from ui.login_window import LoginWindow
from ui.manage_levels_window import ManageLevelsWindow
from ui.manage_classes_window import ManageClassesWindow
from ui.manage_payments_window import ManagePaymentsWindow
from ui.manage_rewards_window import ManageRewardsWindow
from ui.manage_users_window import ManageUsersWindow
import shutil
import sys
import subprocess

class MainWindow(QMainWindow):
    def __init__(self, username=None, role="user"):
        super().__init__()
        self.username = username
        self.role = role
        self.setWindowTitle("Ventana Principal")  # Título de la ventana
        self.setWindowIcon(QIcon("resources/el_escondite_ingles.bmp"))
        self.setGeometry(100, 100, 800, 600)  # Tamaño y posición de la ventana
        self.init_ui()  # Inicializamos la interfaz gráfica

    def init_ui(self):
        # Creamos el layout y el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)  # Establecemos el widget central

        self.layout = QVBoxLayout(self.central_widget)  # Layout vertical para la ventana
        self.layout.setContentsMargins(30, 30, 30, 30)  # Márgenes exteriores
        self.layout.setSpacing(15)  # Espaciado entre secciones

        # Layout horizontal para imagen + título
        header_layout = QHBoxLayout()

        # Imagen de la academia (ajustar ruta según ubicación real)
        logo_label = QLabel()
        pixmap = QPixmap("resources/el_escondite_ingles.jpg").scaled(80, 80)  # Ajusta tamaño si es necesario
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(80, 80)

        # Añadimos un título para la ventana principal
        title = QLabel("Bienvenido a la gestión de 'El escondite Inglés Academy'")
        title.setFont(QFont("Arial", 24, QFont.Bold))

        header_layout.addWidget(logo_label) # Añadimos la imagen de la academia al layout
        header_layout.addWidget(title) # Añadimos el texto al layout

        # Agregar layout al layout principal
        self.layout.addLayout(header_layout)

        # Separador visual
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line1)

        # Grupo de gestión (alumnos, clases, niveles, etc.)
        gestion_group = QGroupBox("Gestión académica")
        gestion_layout = QVBoxLayout()

        self.students_button = QPushButton("Gestionar Alumnos")
        self.students_button.clicked.connect(self.manage_students)
        gestion_layout.addWidget(self.students_button)

        self.classes_button = QPushButton("Gestionar Clases")
        self.classes_button.clicked.connect(self.manage_classes)
        gestion_layout.addWidget(self.classes_button)

        self.manage_levels_button = QPushButton("Gestionar Niveles")
        self.manage_levels_button.clicked.connect(self.manage_levels)
        gestion_layout.addWidget(self.manage_levels_button)

        self.payments_button = QPushButton("Gestionar Pagos")
        self.payments_button.clicked.connect(self.manage_payments)
        gestion_layout.addWidget(self.payments_button)

        self.rewards_button = QPushButton("Gestionar Recompensas")
        self.rewards_button.clicked.connect(self.manage_rewards)
        gestion_layout.addWidget(self.rewards_button)

        gestion_group.setLayout(gestion_layout)
        self.layout.addWidget(gestion_group)

        # Separador visual
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line2)

        # Grupo de herramientas
        tools_group = QGroupBox("Herramientas")
        tools_layout = QVBoxLayout()

        self.backup_button = QPushButton("Hacer Backup de la BD")
        self.backup_button.clicked.connect(self.backup_database)
        tools_layout.addWidget(self.backup_button)

        self.restore_button = QPushButton("Restaurar BD desde Backup")
        self.restore_button.clicked.connect(self.restore_database)
        tools_layout.addWidget(self.restore_button)

        self.users_button = QPushButton("Gestionar Usuarios de la Aplicación")
        self.users_button.clicked.connect(self.manage_users)
        tools_layout.addWidget(self.users_button)

        tools_group.setLayout(tools_layout)
        self.layout.addWidget(tools_group)

        # Separador visual
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line3)

        # Botón de logout siempre visible
        self.logout_button = QPushButton("Cerrar sesión")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        # Ocultar tod excepto logout si el rol es 'user'
        if self.role == "user":
            gestion_group.hide()
            tools_group.hide()

    def manage_students(self):
        """Abre la ventana para gestionar los alumnos"""
        self.manage_students_window = ManageStudentsWindow()  # Abrimos la ventana para gestionar alumnos
        self.manage_students_window.show() # Mostramos la ventana de gestión de alumnos

    def manage_classes(self):
        """Abre la ventana para gestionar las clases"""
        self.manage_classes_window = ManageClassesWindow() # Abrimos la ventana para gestionar clases
        self.manage_classes_window.show() # Mostramos la ventana de gestión de clases

    def manage_levels(self):
        """Abre la ventana para gestionar los niveles"""
        self.manage_levels_window = ManageLevelsWindow()  # Creamos una instancia de la ventana de gestión de niveles
        self.manage_levels_window.show()  # Mostramos la ventana de gestión de niveles

    def manage_payments(self):
        """Abre la ventana para gestionar los pagos"""
        self.manage_payments_window = ManagePaymentsWindow() # Creamos una instancia de la ventana de gestión de pagos
        self.manage_payments_window.show() # Mostramos la ventana de gestión de pagos

    def manage_rewards(self):
        """Abre la ventana de gestión de recompensas"""
        self.manage_rewards_window = ManageRewardsWindow()
        self.manage_rewards_window.show()

    def backup_database(self):
        """Muestra un aviso y permite guardar una copia de la base de datos forzando la extensión .db"""
        confirm = QMessageBox.question(self, "Confirmar Backup", "¿Deseas guardar una copia de seguridad de la base de datos?",
            QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            path, _ = QFileDialog.getSaveFileName(self, "Guardar Backup", "", "Archivos de Base de Datos (*.db)")
            if path:
                # Forzar extensión .db si no está incluida
                if not path.lower().endswith(".db"):
                    path += ".db"

                try:
                    shutil.copyfile("db/el_escondite_ingles.db", path)
                    QMessageBox.information(self, "Backup creado", f"Backup guardado correctamente en:\n{path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo guardar el backup:\n{str(e)}")

    def restore_database(self):
        """Restaura la base de datos desde un archivo .db seleccionado por el usuario"""
        path, _ = QFileDialog.getOpenFileName(self, "Selecciona el archivo de backup", "",
                                              "Archivos de base de datos (*.db)")
        if not path:
            return  # Cancelado

        confirm = QMessageBox.question(
            self,
            "Confirmar Restauración",
            "Esto sobrescribirá la base de datos actual.\n¿Quieres continuar?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                shutil.copyfile(path, "db/el_escondite_ingles.db")
                QMessageBox.information(self, "Restauración Completa",
                                        "La base de datos fue restaurada correctamente.\nLa aplicación se reiniciará.")

                # Reiniciar aplicación
                python = sys.executable
                subprocess.Popen([python] + sys.argv)
                sys.exit(0)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo restaurar la base de datos:\n{str(e)}")

    def manage_users(self):
        """Abre la ventana para gestionar los usuarios"""
        self.manage_users_window = ManageUsersWindow()
        self.manage_users_window.show()

    def logout(self):
        """Se desloguea de la app"""
        self.close()  # Cerramos la ventana principal
        self.open_login_window()  # Llamamos a la función que abre la ventana de login

    def open_login_window(self):
        """Abre la ventana de login"""
        self.login_window = LoginWindow()  # Creamos la ventana de login
        self.login_window.show()  # Mostramos la ventana de login
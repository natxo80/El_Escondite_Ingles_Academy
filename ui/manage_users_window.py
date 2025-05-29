from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
                               QLineEdit, QMessageBox, QComboBox, QHeaderView, QAbstractScrollArea, QLabel)
from db.database import fetch_users, insert_user, delete_user, update_user

class ManageUsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionar Usuarios")
        self.setWindowIcon(QIcon("resources/el_escondite_ingles.bmp"))
        self.setGeometry(100, 100, 600, 800)
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz gráfica para la gestión de usuarios"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # ---------- CABECERA CON LOGO Y TÍTULO ----------
        header_layout = QHBoxLayout()

        self.logo = QLabel()
        self.logo.setPixmap("resources/el_escondite_ingles.jpg")
        self.logo.setFixedSize(60, 60)
        self.logo.setScaledContents(True)
        header_layout.addWidget(self.logo)

        title = QLabel("Gestión de Usuarios - El Escondite Inglés")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4B0082;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)
        # ------------------------------------------------

        # ---------- TABLA DE USUARIOS ----------
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Usuario", "Rol", "Contraseña"])
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        # ----------------------------------------

        # ---------- FORMULARIO DE ENTRADA ----------
        form_layout = QHBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)  # Opcional: oculta caracteres
        form_layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "user"])
        form_layout.addWidget(self.role_combo)

        self.layout.addLayout(form_layout)
        # ---------------------------------------------

        # ---------- BOTONES DE ACCIÓN ----------
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Añadir Usuario")
        self.add_button.clicked.connect(self.add_user)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Usuario")
        self.edit_button.clicked.connect(self.edit_user)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Eliminar Usuario")
        self.delete_button.clicked.connect(self.delete_user)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        # --------------------------------------

        self.setLayout(self.layout)
        self.load_users()

    def load_users(self):
        """Carga todos los usuarios desde la base de datos en la tabla"""
        self.table.setRowCount(0)
        users = fetch_users()
        for row, user in enumerate(users):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(user[1]))
            self.table.setItem(row, 1, QTableWidgetItem(user[3]))
            self.table.setItem(row, 2, QTableWidgetItem(user[2]))  # Mostrar contraseña en plano solo si es necesario

    def add_user(self):
        """Añade un nuevo usuario"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Usuario y contraseña son obligatorios.")
            return

        insert_user(username, password, role)
        self.load_users()
        self.username_input.clear()
        self.password_input.clear()
        self.role_combo.setCurrentIndex(0)

    def edit_user(self):
        """Edita un usuario seleccionado"""
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para editar.")
            return

        old_username = self.table.item(selected, 0).text()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Usuario y contraseña son obligatorios.")
            return

        update_user(old_username, username, password, role)
        self.load_users()
        self.username_input.clear()
        self.password_input.clear()
        self.role_combo.setCurrentIndex(0)

    def delete_user(self):
        """Elimina el usuario seleccionado"""
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un usuario para eliminar.")
            return

        username = self.table.item(selected, 0).text()
        confirm = QMessageBox.question(self, "Confirmar", f"¿Estás seguro de eliminar al usuario '{username}'?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            delete_user(username)
            self.load_users()